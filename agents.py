from dotenv import load_dotenv

from langchain.agents import create_agent

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# HUGGING FACE MODEL
# =========================
hf_llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    temperature=0,
    max_new_tokens=2048,
)

llm = ChatHuggingFace(llm=hf_llm)

# =========================
# SEARCH AGENT
# =========================
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

# =========================
# READER AGENT
# =========================
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

# =========================
# WRITER
# =========================
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer."),
    ("human",
     "Write a report on:\n{topic}\n\nResearch:\n{research}")
])

writer_chain = writer_prompt | llm | StrOutputParser()

# =========================
# CRITIC
# =========================
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strict critic."),
    ("human",
     "Review this report:\n{report}")
])

critic_chain = critic_prompt | llm | StrOutputParser()

# =========================
# TEST
# =========================
if __name__ == "__main__":
    print(llm.invoke("Hello!").content)