from crawl4ai import AsyncWebCrawler
from crawl4ai import LLMExtractionStrategy, CacheMode
import os
import asyncio
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

load_dotenv()
mower_data = [
{"id":"1290","slug":"ryobi-p1180","name":"P1180","page_url":"https://www.ryobitools.com/products/details/46396034571","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1291","slug":"ryobi-p1190","name":"P1190","page_url":"https://www.ryobitools.com/products/details/46396034588","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1301","slug":"ryobi-ry401220","name":"RY401220","page_url":"https://www.ryobitools.com/products/details/46396040718","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1292","slug":"ryobi-ry401140","name":"RY401140","page_url":"https://www.ryobitools.com/products/details/46396036995","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1296","slug":"ryobi-ry401101","name":"RY401101","page_url":"https://www.ryobitools.com/products/details/46396045607","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1298","slug":"ryobi-ry401210","name":"RY401210","page_url":"https://www.ryobitools.com/products/details/46396040244","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1299","slug":"ryobi-ry401170","name":"RY401170","page_url":"https://www.ryobitools.com/products/details/46396037169","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1300","slug":"ryobi-ry401180","name":"RY401180","page_url":"https://www.ryobitools.com/products/details/46396037176","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1302","slug":"ryobi-ry401260","name":"RY401260","page_url":"https://www.ryobitools.com/products/details/46396045386","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1304","slug":"ryobi-ryrm8010","name":"RYRM8010","page_url":"https://www.ryobitools.com/products/details/46396040886","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1307","slug":"ryobi-ryrm8060","name":"RYRM8060","page_url":"https://www.ryobitools.com/products/details/46396041845","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1308","slug":"ryobi-ryrm8070","name":"RYRM8070","page_url":"https://www.ryobitools.com/products/details/46396041852","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1293","slug":"ryobi-ry401150","name":"RY401150","page_url":"https://www.ryobitools.com/products/details/46396036711","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1294","slug":"ryobi-ry48ztr100","name":"RY48ZTR100","page_url":"https://www.ryobitools.com/products/details/46396025395","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1295","slug":"ryobi-ry48ztr75","name":"RY48ZTR75","page_url":"https://www.ryobitools.com/products/details/46396023971","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1297","slug":"ryobi-ry401100vnm","name":"RY401100VNM","page_url":"https://www.ryobitools.com/products/details/46396027726","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1303","slug":"ryobi-rypm8010","name":"RYPM8010","page_url":"https://www.ryobitools.com/products/details/46396046468","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1305","slug":"ryobi-ryrm8021","name":"RYRM8021","page_url":"https://www.ryobitools.com/products/details/46396040923","brand_name":"Ryobi","category_page_url":"","series_page_url":""},
{"id":"1306","slug":"ryobi-ryrm8034","name":"RYRM8034","page_url":"https://www.ryobitools.com/products/details/46396041029","brand_name":"Ryobi","category_page_url":"","series_page_url":""}
]


class ImageLink(BaseModel):
    link: str = Field(..., description="Source link of the image")
    alt: str = Field(..., description="Alt text of the image")


data = []
cache = {}


async def click_and_extract_images(
    url: str, model_name: str, brand_name: str, page_type: str
):
    browser_config = BrowserConfig(browser_type="chromium", headless=True)
    llm_strategy = LLMExtractionStrategy(
            provider="openai/gpt-4o",
            api_token=os.getenv("OPENAI_API_KEY"),
            extraction_type="schema",
            schema=ImageLink.model_json_schema(),
            instruction="""
        Extract all mower model image links from the page.
        """,
        )
    crawler_run_config = CrawlerRunConfig(
        wait_for_images=True, verbose=True, scan_full_page=True, scroll_delay=3,
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.DISABLED,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        if url not in cache:
            result = await crawler.arun(
                url=url,
                config=crawler_run_config,
            )
            cache[url] = result.extracted_content if result.extracted_content else "[]"
            extracted_content = (
                result.extracted_content if result.extracted_content else "[]"
            )
        else:
            extracted_content = cache[url]

        llm_strategy.show_usage()

        for content in json.loads(extracted_content):

            def remove_query_parameters(url: str) -> str:
                from urllib.parse import urlparse, urlunparse

                parsed_url = urlparse(url)
                cleaned_url = parsed_url._replace(query="")
                return urlunparse(cleaned_url)

            def add_https(url: str) -> str:
                if not url.startswith("https"):
                    return "https:" + url
                return url

            def add_domain(url: str, base_url: str) -> str:
                from urllib.parse import urlparse

                domain = f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}"
                if not url.startswith(domain):
                    return f"{domain}{url}"
                return url

            data.append(
                {
                    "file_name": "",
                    "Brand": brand_name,
                    "model_name": model_name,
                    "URL": content["link"],
                    "array_order": 99,
                    "alt": content["alt"],
                    "Tags": page_type,
                }
            )

    with open(f"{brand_name}_model_images.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == "__main__":
    for mower in mower_data:
        page_urls = {}
        if mower["page_url"]:
            page_urls["model"] = mower["page_url"]
        if mower["category_page_url"]:
            page_urls["category"] = mower["category_page_url"]
        if mower["series_page_url"]:
            page_urls["series"] = mower["series_page_url"]

        for page_type, page_url in page_urls.items():
            asyncio.run(
                click_and_extract_images(
                    url=page_url,
                    model_name=mower["name"],
                    brand_name=mower["brand_name"],
                    page_type=page_type,
                )
            )
    print(json.dumps(data, indent=4))
