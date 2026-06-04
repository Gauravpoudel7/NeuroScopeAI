from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup

from dotenv import load_dotenv

import requests
import os

# ====================================
# LOAD ENV VARIABLES
# ====================================
load_dotenv()

# ====================================
# TAVILY CLIENT
# ====================================
tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

# ====================================
# WEB SEARCH TOOL
# ====================================
@tool
def web_search(query: str) -> str:
    """
    Search the web for reliable and recent information.
    Returns titles, URLs and snippets.
    """

    try:

        results = tavily.search(
            query=query,
            max_results=5,
            search_depth="advanced"
        )

        formatted_results = []

        for item in results["results"]:

            formatted_results.append(
                f"""
Title: {item.get('title', '')}

URL: {item.get('url', '')}

Snippet:
{item.get('content', '')}

{'=' * 60}
"""
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Search Error: {str(e)}"


# ====================================
# SCRAPE URL TOOL
# ====================================
@tool
def scrape_url(url: str) -> str:
    """
    Scrape a webpage and return clean text.
    """

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/125.0 Safari/537.36"
                )
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unwanted tags
        for tag in soup(
            [
                "script",
                "style",
                "header",
                "footer",
                "nav",
                "aside",
                "noscript",
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:5000]

    except Exception as e:
        return f"Scraping Error: {str(e)}"


# ====================================
# TEST
# ====================================
if __name__ == "__main__":

    print(
        web_search.invoke(
            "Latest developments in Generative AI"
        )
    )