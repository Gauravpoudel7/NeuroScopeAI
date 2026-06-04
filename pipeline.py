from dotenv import load_dotenv

from langchain.agents import create_agent

from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

# =========================
# HUGGING FACE LLM
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
# WRITER CHAIN
# =========================
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert research writer. Write clear, structured and insightful reports."
        ),
        (
            "human",
            """
Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Structure the report as:

- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.
"""
        ),
    ]
)

writer_chain = writer_prompt | llm | StrOutputParser()

# =========================
# CRITIC CHAIN
# =========================
critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a sharp and constructive research critic. Be honest and specific."
        ),
        (
            "human",
            """
Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...
"""
        ),
    ]
)

critic_chain = critic_prompt | llm | StrOutputParser()

# =========================
# TEST
# =========================
if __name__ == "__main__":

    response = llm.invoke(
        "Explain Artificial Intelligence in 3 sentences."
    )

    print(response.content)