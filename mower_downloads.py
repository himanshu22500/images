import asyncio
import json
import os

from dotenv import load_dotenv

load_dotenv()
from crawl4ai import AsyncWebCrawler, CacheMode

from pydantic import BaseModel, Field
from crawl4ai.extraction_strategy import LLMExtractionStrategy

mower_data = [
    {
        "id": "941",
        "slug": "snapper-7800982b",
        "name": "7800982B",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/hi-vac-lawn-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/hi-vac-lawn-mower.html",
        "series_page_url": "",
    },
    {
        "id": "942",
        "slug": "snapper-7800981b",
        "name": "7800981B",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/ninja-push-mowers.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/ninja-push-mowers.html",
        "series_page_url": "",
    },
    {
        "id": "943",
        "slug": "snapper-7800849b",
        "name": "7800849B",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/commercial-walk-mowers.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/commercial-walk-mowers.html",
        "series_page_url": "",
    },
    {
        "id": "947",
        "slug": "snapper-2691499",
        "name": "2691499",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-zero-turn-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-zero-turn-mower.html",
        "series_page_url": "",
    },
    {
        "id": "948",
        "slug": "snapper-2691651",
        "name": "2691651",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-zero-turn-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-zero-turn-mower.html",
        "series_page_url": "",
    },
    {
        "id": "949",
        "slug": "snapper-2691827",
        "name": "2691827",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-zero-turn-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-zero-turn-mower.html",
        "series_page_url": "",
    },
    {
        "id": "950",
        "slug": "snapper-2691829",
        "name": "2691829",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-zero-turn-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-zero-turn-mower.html",
        "series_page_url": "",
    },
    {
        "id": "940",
        "slug": "snapper-7800980b",
        "name": "7800980B",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/hi-vac-lawn-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/hi-vac-lawn-mower.html",
        "series_page_url": "",
    },
    {
        "id": "944",
        "slug": "snapper-7800968b",
        "name": "7800968B",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/commercial-walk-mowers.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/push-mowers/commercial-walk-mowers.html",
        "series_page_url": "",
    },
    {
        "id": "945",
        "slug": "snapper-2691663",
        "name": "2691663",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/riding-mowers/spx-riding-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/riding-mowers/spx-riding-mower.html",
        "series_page_url": "",
    },
    {
        "id": "946",
        "slug": "snapper-2691664",
        "name": "2691664",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/riding-mowers/spx-riding-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/riding-mowers/spx-riding-mower.html",
        "series_page_url": "",
    },
    {
        "id": "951",
        "slug": "snapper-2691816",
        "name": "2691816",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-xt-zero-turn-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-xt-zero-turn-mower.html",
        "series_page_url": "",
    },
    {
        "id": "953",
        "slug": "snapper-5901862",
        "name": "5901862",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s120.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s120.html",
        "series_page_url": "",
    },
    {
        "id": "952",
        "slug": "snapper-2691817",
        "name": "2691817",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-xt-zero-turn-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/zero-turn-mowers/360z-xt-zero-turn-mower.html",
        "series_page_url": "",
    },
    {
        "id": "954",
        "slug": "snapper-5901865",
        "name": "5901865",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s120.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s120.html",
        "series_page_url": "",
    },
    {
        "id": "955",
        "slug": "snapper-5901867",
        "name": "5901867",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s120.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s120.html",
        "series_page_url": "",
    },
    {
        "id": "956",
        "slug": "snapper-5901868",
        "name": "5901868",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s120.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s120.html",
        "series_page_url": "",
    },
    {
        "id": "957",
        "slug": "snapper-5901280",
        "name": "5901280",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "series_page_url": "",
    },
    {
        "id": "958",
        "slug": "snapper-5901664",
        "name": "5901664",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "series_page_url": "",
    },
    {
        "id": "959",
        "slug": "snapper-5901665",
        "name": "5901665",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "series_page_url": "",
    },
    {
        "id": "963",
        "slug": "snapper-82v-max-cordless-self-propelled-walk-mower",
        "name": "82V MAX CORDLESS SELF-PROPELLED WALK MOWER",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/electric-products/mowers/snapper-xd-82v-max-electric-cordless-self-propelled-walk-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/electric-products/mowers/snapper-xd-82v-max-electric-cordless-self-propelled-walk-mower.html",
        "series_page_url": "",
    },
    {
        "id": "964",
        "slug": "snapper-82v-max-stepsense-cordless-lawn-mower",
        "name": "82V MAX STEPSENSE CORDLESS LAWN MOWER",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/electric-products/mowers/snapper-xd-82v-max-stepsense-automatic-drive-electric-lawn-mower.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/electric-products/mowers/snapper-xd-82v-max-stepsense-automatic-drive-electric-lawn-mower.html",
        "series_page_url": "",
    },
    {
        "id": "960",
        "slug": "snapper-5901666",
        "name": "5901666",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "series_page_url": "",
    },
    {
        "id": "961",
        "slug": "snapper-5901667",
        "name": "5901667",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/pro/zero-turn-mowers/s200xt.html",
        "series_page_url": "",
    },
    {
        "id": "962",
        "slug": "snapper-82v-max-cordless-walk-mowers",
        "name": "82V MAX CORDLESS WALK MOWERS",
        "brand_name": "Snapper",
        "page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/electric-products/mowers/82volt-max_-lithiumion-cordless-walk-mowers.html",
        "category_page_url": "https://www.snapper.com/na/en_us/product-catalog/residential/electric-products/mowers/82volt-max_-lithiumion-cordless-walk-mowers.html",
        "series_page_url": "",
    },
]


class ImageLink(BaseModel):
    link: str = Field(..., description="Source link of image on page")
    alt: str = Field(..., description="alt text of image on page")


data = []
cache = {}


async def extract_all_image_links_from_website(
    url: str, model_name: str, brand_name: str, page_type: str
) -> str:
    async with AsyncWebCrawler() as crawler:
        if url not in cache:
            result = await crawler.arun(
                url=url,
                extraction_strategy=LLMExtractionStrategy(
                    provider="openai/gpt-4o",
                    api_token=os.getenv("OPENAI_API_KEY"),
                    extraction_type="schema",
                    schema=ImageLink.model_json_schema(),
                    instruction="""
                    Extract all mower model image links from the page.
                    """,
                ),
                cache_mode=CacheMode.BYPASS,
            )
            cache[url] = result.extracted_content
            extracted_content = result.extracted_content
        else:
            extracted_content = cache[url]

        for content in json.loads(extracted_content):
            data.append(
                {
                    "file_name": "",
                    "Brand": brand_name,
                    "model_name": model_name,
                    "URL": 'https://www.snapper.com' + content["link"],
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
                extract_all_image_links_from_website(
                    url=page_url,
                    model_name=mower["name"],
                    brand_name=mower["brand_name"],
                    page_type=page_type,
                )
            )
    print(json.dumps(data, indent=4))
