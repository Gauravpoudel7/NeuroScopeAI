🧠 NeuroScope AI — Multi-Agent Generative AI Research System








🚀 Overview

NeuroScope AI is a multi-agent Generative AI system that autonomously performs research, reads web content, generates structured reports, and critiques its own output.

It simulates a real AI research team using multiple specialized agents:

🔍 Search Agent → finds real-time information from the web
📄 Reader Agent → extracts and cleans webpage content
✍️ Writer Agent → generates structured research reports
🧐 Critic Agent → evaluates and improves the final output
🧠 Key Features
🌐 Real-time web search using Tavily API
📄 Web scraping and content extraction
🤖 Hugging Face LLM (Qwen2.5-7B-Instruct)
🧩 Multi-agent architecture (Search → Read → Write → Critique)
🖥️ Interactive Streamlit UI
📊 Automated structured report generation
🧠 AI-generated feedback and scoring system
⚙️ Architecture
User Input (Topic)
        ↓
🔍 Search Agent (Tavily Web Search)
        ↓
📄 Reader Agent (Web Scraping & Cleaning)
        ↓
✍️ Writer Chain (LLM Report Generation)
        ↓
🧐 Critic Chain (Quality Evaluation)
        ↓
📊 Final Structured Report
🛠️ Tech Stack
Python 3.10+
LangChain (Agents + Prompt Engineering)
Hugging Face (Qwen2.5-7B-Instruct)
Tavily API (Web Search)
BeautifulSoup (Web Scraping)
Streamlit (Frontend UI)
dotenv (Environment Variables)
📁 Project Structure
manyAgents/
│
├── app.py              # Streamlit frontend
├── agents.py          # Multi-agent system logic
├── tools.py           # Web search & scraping tools
├── .env               # API keys (not pushed to GitHub)
└── README.md
🔑 Environment Variables

Create a .env file in the root directory:

HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
TAVILY_API_KEY=your_tavily_api_key
📦 Installation

Clone the repository:

git clone https://github.com/gauravpoudel7/neuroscope-ai.git
cd neuroscope-ai

Install dependencies:

pip install -r requirements.txt

Or manually install:

pip install streamlit langchain langchain-huggingface huggingface_hub
pip install tavily-python beautifulsoup4 requests python-dotenv
▶️ Run the Project

Start the Streamlit app:

streamlit run app.py

Then open:

http://localhost:8501
💡 Example Usage
Input:
Future of Artificial Intelligence
Output:
🔍 Web search results
📄 Cleaned research content
✍️ Structured AI report
🧐 Critic evaluation with score
📊 Sample Output
Score: 8.5/10

Strengths:
- Well-structured report
- Good synthesis of information
- Clear explanations

Areas to Improve:
- Add more statistical data
- Include recent citations

Verdict:
Strong research output with minor improvements needed.
🔥 Highlights
Fully autonomous AI research pipeline
Multi-agent collaboration system
Real-time web augmentation
Structured reasoning + evaluation loop
Beginner-friendly LangChain implementation
🚀 Future Improvements
🔗 Add vector database (FAISS / Chroma) for RAG
🧠 Add memory to agents
⚡ Streamed responses (real-time typing effect)
📊 Visual workflow graph (LangGraph style)
🤖 Upgrade to GPT-4o / DeepSeek for stronger reasoning
🧾 Export reports as PDF
👨‍💻 Author

Gaurav Poudel

Focused on:

Generative AI 🤖
LLM Agents 🧠
Machine Learning & Deep Learning 📊
⭐ If you like this project

Give it a ⭐ on GitHub and follow for more AI projects.
