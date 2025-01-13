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
{"id":"726","slug":"dixie-chopper-zee-2-2348kw","name":"Zee 2 2348KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/residential/zee-2/"},
{"id":"727","slug":"dixie-chopper-zee-2-2354kw","name":"Zee 2 2354KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/residential/zee-2/"},
{"id":"730","slug":"dixie-chopper-blackhawk-2454kw","name":"BlackHawk 2454KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/blackhawk/"},
{"id":"731","slug":"dixie-chopper-blackhawk-2460kw","name":"BlackHawk 2460KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/blackhawk/"},
{"id":"732","slug":"dixie-chopper-blackhawk-hp-2448kw","name":"BlackHawk HP 2448KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/blackhawk-hp/"},
{"id":"733","slug":"dixie-chopper-blackhawk-hp-2454kw","name":"BlackHawk HP 2454KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/blackhawk-hp/"},
{"id":"728","slug":"dixie-chopper-talon-r-c-2844vge","name":"Talon R/C 2844VGE","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/remote-control/talon-rc/"},
{"id":"725","slug":"dixie-chopper-zee-2-2342kw","name":"Zee 2 2342KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/residential/zee-2/"},
{"id":"729","slug":"dixie-chopper-blackhawk-2448kw","name":"BlackHawk 2448KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/blackhawk/"},
{"id":"739","slug":"dixie-chopper-classic-4072vge","name":"Classic 4072VGE","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/industrial/classic/"},
{"id":"740","slug":"dixie-chopper-eagle-2754kw","name":"Eagle 2754KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/eagle/"},
{"id":"734","slug":"dixie-chopper-blackhawk-hp-2460kw","name":"BlackHawk HP 2460KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/blackhawk-hp/"},
{"id":"735","slug":"dixie-chopper-classic-2760kw","name":"Classic 2760KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/industrial/classic/"},
{"id":"736","slug":"dixie-chopper-classic-3560kw","name":"Classic 3560KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/industrial/classic/"},
{"id":"738","slug":"dixie-chopper-classic-3572kw","name":"Classic 3572KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/industrial/classic/"},
{"id":"737","slug":"dixie-chopper-classic-4060vge","name":"Classic 4060VGE","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/industrial/classic/"},
{"id":"742","slug":"dixie-chopper-eagle-hp-3560kw","name":"Eagle HP 3560KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/eagle-hp/"},
{"id":"744","slug":"dixie-chopper-eagle-hp-3572kw","name":"Eagle HP 3572KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/eagle-hp/"},
{"id":"745","slug":"dixie-chopper-eagle-hp-4072vge","name":"Eagle HP 4072VGE","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/eagle-hp/"},
{"id":"743","slug":"dixie-chopper-eagle-hp-4060vge","name":"Eagle HP 4060VGE","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/eagle-hp/"},
{"id":"756","slug":"dixie-chopper-falcon-hp-2448kw","name":"Falcon HP 2448KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/residential/falcon-hp/"},
{"id":"750","slug":"dixie-chopper-xcaliber-3566kw","name":"Xcaliber 3566KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/industrial/xcaliber/"},
{"id":"752","slug":"dixie-chopper-xcaliber-3574kw","name":"Xcaliber 3574KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/industrial/xcaliber/"},
{"id":"751","slug":"dixie-chopper-xcaliber-4066vge","name":"Xcaliber 4066VGE","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/industrial/xcaliber/"},
{"id":"741","slug":"dixie-chopper-eagle-2760kw","name":"Eagle 2760KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/eagle/"},
{"id":"753","slug":"dixie-chopper-xcaliber-4074vge","name":"Xcaliber 4074VGE","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/industrial/xcaliber/"},
{"id":"754","slug":"dixie-chopper-zee-2-hp-series-2448kw","name":"Zee 2 HP Series 2448KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/residential/zee-2-hp/"},
{"id":"755","slug":"dixie-chopper-zee-2-hp-series-2454kw","name":"Zee 2 HP Series 2454KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/residential/zee-2-hp/"},
{"id":"757","slug":"dixie-chopper-falcon-hp-2454kw","name":"Falcon HP 2454KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/residential/falcon-hp/"},
{"id":"746","slug":"dixie-chopper-falcon-hpx-2448kw","name":"Falcon HPX 2448KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/falcon-hpx/"},
{"id":"747","slug":"dixie-chopper-falcon-hpx-2454kw","name":"Falcon HPX 2454KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/falcon-hpx/"},
{"id":"758","slug":"dixie-chopper-falcon-hp-2460kw","name":"Falcon HP 2460KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/residential/falcon-hp/"},
{"id":"748","slug":"dixie-chopper-falcon-hpx-2460kw","name":"Falcon HPX 2460KW","brand_name":"Dixie Chopper","page_url":"","category_page_url":"","series_page_url":"https://www.dixiechopper.com/product-category/commercial/falcon-hpx/"}
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
