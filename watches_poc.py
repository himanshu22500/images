from crawl4ai import AsyncWebCrawler
from crawl4ai import LLMExtractionStrategy, CacheMode
import os
import asyncio
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

load_dotenv()

class ImageLink(BaseModel):
    link: str = Field(..., description="Source link of the image")
    alt: str = Field(..., description="Alt text of the image")

class WatchModel(BaseModel):
    model_name: str = Field(..., description="Name of the model")
    model_images: list[ImageLink] = Field(..., description="List of images")


async def click_and_extract_images(
    url: str
):
    browser_config = BrowserConfig(browser_type="chromium", headless=True)
    llm_strategy = LLMExtractionStrategy(
            provider="openai/gpt-4o",
            api_token=os.getenv("OPENAI_API_KEY"),
            extraction_type="schema",
            schema=WatchModel.model_json_schema(),
            instruction="""
            Extract all the different watches model name and images from the page. 
            consider watches with different dials as different models.
            
        """,
        )
    crawler_run_config = CrawlerRunConfig(
        wait_for_images=True, verbose=True, scan_full_page=True, scroll_delay=3,
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.DISABLED,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=url,
            config=crawler_run_config,
        )
        print(result.extracted_content)

        llm_strategy.show_usage()

if __name__ == "__main__":
    asyncio.run(click_and_extract_images(url=''))
