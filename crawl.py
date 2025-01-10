import asyncio
import json
import os

from dotenv import load_dotenv

load_dotenv()
from crawl4ai import AsyncWebCrawler, CacheMode

from pydantic import BaseModel, Field
from crawl4ai.extraction_strategy import LLMExtractionStrategy


class KnowledgeGraph(BaseModel):
    entities: list[dict]
    relationships: list[dict]


strategy = LLMExtractionStrategy(
    provider="OpenAI/gpt-4o-mini",  # or "huggingface/...", "ollama/..."
    api_token=os.getenv("OPENAI_API_KEY"),
    schema=KnowledgeGraph.model_json_schema(),
    instruction="Extract entities and relationships from the content"
)


class ModelSpecification(BaseModel):
    specification_name: str = Field(..., description="Name of the specification.")
    specification_value: str = Field(..., description="Value of the specification without unit.")
    specification_unit: str = Field(..., description="Unit of the specification.")


class UserReview(BaseModel):
    title: str = Field(..., description="Title of the review.")
    rating: int = Field(..., description="Rating of out of 5")
    review_content: str = Field(..., description="Content of the review.")

class PDFLink(BaseModel):
    link: str = Field(..., description="Link to the PDF file.")
    name: str = Field(..., description="Name of the PDF file.")


class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the Tractor model.")
    model_price: str = Field(..., description="Price of the Tractor model.")
    model_specification: list[ModelSpecification] = Field(..., description="Specification of the Tractor model.")
    user_reviews: list[UserReview] = Field(..., description="User reviews")
    pdf_links: list[PDFLink] = Field(..., description="PDF links")


async def extract_openai_pricing():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.ryobitools.com/products/details/46396034588",
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4o",
                api_token=os.getenv("OPENAI_API_KEY"),
                schema=PDFLink.model_json_schema(),
                extraction_type="schema",
                instruction="""
                Extract the model name and all specification of the tractor from the content
                Extract all user reviews from the content.
                """
            ),
            cache_mode=CacheMode.BYPASS
        )
        print(result.extracted_content)
        # print(result.media)


if __name__ == "__main__":
    asyncio.run(extract_openai_pricing())
