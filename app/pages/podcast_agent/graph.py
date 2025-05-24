import operator
import random
import xml.etree.ElementTree as ET
from typing import Annotated, TypedDict

import requests
from crawl4ai import AsyncWebCrawler
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph
from langgraph.types import Send

from app.pages.podcast_agent.constants import (
    NEWS_ARTICLE_SCRAPPER_SYSTEM_PROMPT,
    STREAMER_SYSTEM_PROMPT,
    NewsArticle,
)


def build_graph(model: BaseChatModel):
    class OverallState(TypedDict):
        limit: int
        topic: str
        news_min: list[NewsArticle]
        news: Annotated[list[NewsArticle], operator.add]
        podcast_script: str

    def fetch_news_headlines(state: OverallState):
        rss_reponse = requests.post(
            url=f"https://eluniverso.opennemas.com/rss/{state["topic"]}/",
        )
        root = ET.fromstring(rss_reponse.content)
        channel = root.find("channel")

        if channel is None:
            return

        news_headlines = []

        for news_headline in channel.findall("item"):
            news_headlines.append(
                {
                    "headline": news_headline.find("title").text,
                    "url": news_headline.find("link").text,
                }
            )

        return {
            "news_min": news_headlines,
        }

    async def fetch_news_article_content(news_article: NewsArticle):
        async with AsyncWebCrawler() as crawler:
            response = await crawler.arun(
                url=news_article["url"],
            )

            article_scrapper_response = await model.ainvoke(
                [
                    SystemMessage(NEWS_ARTICLE_SCRAPPER_SYSTEM_PROMPT),
                    HumanMessage(response.markdown),
                ]
            )

            news_article["content"] = str(article_scrapper_response.content)

            return {"news": [news_article]}

    def generate_podcast_script(state: OverallState):
        response = model.invoke(
            [
                SystemMessage(STREAMER_SYSTEM_PROMPT),
                HumanMessage(
                    str(
                        state["news"],
                    )
                ),
            ]
        )

        return {
            "podcast_script": str(response.content),
        }

    def continue_to_fetch_news_article_content(state: OverallState) -> list[Send]:
        news_min = state["news_min"]
        limit = state["limit"]
        random_indexs = random.sample(range(len(news_min)), limit)
        news_data = [news_min[i] for i in random_indexs]

        return [
            Send("fetch_news_article_content", NewsArticle(news)) for news in news_data
        ]

    # Graph
    workflow = StateGraph(OverallState)

    # Add nodes
    workflow.add_node("fetch_news_headlines", fetch_news_headlines)
    workflow.add_node("fetch_news_article_content", fetch_news_article_content)
    workflow.add_node("generate_podcast_script", generate_podcast_script)

    # Add edges
    workflow.set_entry_point("fetch_news_headlines")
    workflow.add_conditional_edges(
        "fetch_news_headlines",
        continue_to_fetch_news_article_content,
        ["fetch_news_article_content"],
    )
    workflow.add_edge("fetch_news_article_content", "generate_podcast_script")
    workflow.set_finish_point("generate_podcast_script")

    return workflow.compile(name="podcast_agent")
