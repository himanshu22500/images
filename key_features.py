import asyncio
import json
import os

from dotenv import load_dotenv

load_dotenv()
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig, BrowserConfig

from pydantic import BaseModel, Field
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from models import KeyFeatures as KeyFeaturesModel


class KeyFeature(BaseModel):
    feature: str = Field(..., description="Feature name")
    present: str = Field(
        ...,
        description="Whether feature is present or not or optionally present [YES, NO, OPTIONAL]",
    )
    explanation: str = Field(..., description="Explanation of feature presence")


async def extract_key_features(url: str):
    browser_config = BrowserConfig(browser_type="chromium", headless=True)
    llm_strategy = LLMExtractionStrategy(
        provider="openai/gpt-4o",
        api_token=os.getenv("OPENAI_API_KEY"),
        extraction_type="schema",
        schema=KeyFeature.model_json_schema(),
        instruction="""
Determine whether any feature from the list are mentioned on web page.

Instructions:

1. Feature Verification:
    - Analyze the text to identify whether feature term is:
        - Explicitly Present: The feature is clearly mentioned or implied.
        - Partially/Optionally Present: The feature is present but only in part, or it's implied as an optional feature.
        - Not Present: The feature is not mentioned or implied at all.

2. Response Format:
    - Your answer must be a JSON array of objects, with each object containing:
        - "feature": The feature name provided.
        - "present": "YES" if the feature is fully present, "OPTIONAL" if it's optionally or partially present, otherwise "NO".
        - "explanation": A brief explanation of your decision, including relevant quotes if applicable.

3. Be thorough but concise in your explanations.
4. If multiple synonyms are found, mention all of them in the explanation.
5. Pay attention to context to avoid false positives.

features_synonyms_list :

Cutting Height Adjustment ['Height Control', 'Mowing Height Selector', 'Grass Length Adjustment']
Mulching Capability ['Mulch Kit', 'Grass Recycling', 'Clipping Reprocessing']
Bagging Capability ['Grass Collector', 'Clipping Bag', 'Catcher System']
Side Discharge ['Lateral Discharge', 'Side Ejection', 'Grass Ejector']
Rear Discharge ['Back Discharge', 'Rear Chute']
Safety Interlock Switches ['Interlock System', 'Safety Override', 'Mower Safety Switches']
Operator Presence System ['Operator Sensor', 'Presence Control', 'Safety Seat Switch']
Anti-Scalp Wheels ['Turf Wheels', 'Deck Wheels', 'Ground Following Wheels']
Cruise Control ['Speed Control', 'Automatic Speed Adjustment', 'Cruise Control']
4WD ['Four-Wheel Drive', 'All-Wheel Drive', 'Full-Time 4WD']
Seat Suspension ['Shock-Absorbing Seat', 'Comfort Seat', 'Vibration Dampening Seat']
Adjustable Seat ['Seat Adjustment', 'Customizable Seating', 'Ergonomic Seat']
Armrest ['Arm Supports', 'Operator Armrests', 'Ergonomic Arm Pads']
Platform Suspension ['']
Adjustable Steering ['Adjustable Steering Wheel', 'Steering Column Adjustment', 'Tilt Control']
Hour Meter ['Usage Meter', 'Operation Timer', 'Run Time Meter']
Fuel Gauge ['Fuel Indicator', 'Gas Gauge', 'Fuel Level Display']
LED Display Panel ['Digital Screen', 'Display Console', 'Instrument Panel']
Power Steering ['Steering Assist', 'Hydraulic Steering', 'Assisted Steering']
Speed Settings ['Adjustable Speed', 'Multi-Speed', 'Variable Speed']
Cup Holder ['Beverage Holder', 'Drink Holder', 'Refreshment Holder']
Rear Hitch Capability ['Rear Attachment', 'Hitch System', 'Tow Hitch']
Electric PTO ['Electric Clutch', 'PTO Engagement', 'Power Take-Off Control']
Park Brake ['Parking Brake', 'Brake Lock', 'Emergency Brake']
Backlapping ['Reel Sharpening', 'Blade Maintenance', 'Reel Grinding']
Headlights ['Work Lights', 'LED Lighting', 'Night Vision Lights']
Towing Capability ['Tow Capacity', 'Trailer Support', 'Hitch Capability']
Weather Protection ['Weather Enclosure', 'Weatherproof Cover', 'Protective Canopy']
Hydraulic Deck Lift ['Hydraulic Lift System', 'Powered Deck Lift', 'Hydraulic Adjustment']
Foot Pedal Deck Lift ['Pedal Lift System', 'Foot-Controlled Lift', 'Deck Pedal Adjustment']
Adjustable Steering Levers ['Steering Adjustments', 'Lever Control', 'Handlebar Customization']
Manual Deck Lift ['Manual Height Control', 'Lever Deck Lift', 'Manual Deck Adjustment']
Obstacle Detection System ['Collision Avoidance', 'Object Detection', 'Navigation Safety']
Turf-Friendly Tires ['Lawn Tires', 'Grass-Safe Tires', 'Non-Damaging Tires']
Rain Sensor ['Moisture Sensor', 'Rain Detection', 'Automatic Stop']
Battery Level Indicator ['Battery Status', 'Charge Level Indicator', 'Battery Gauge']
GPS Guidance ['GPS Tracking', 'Automated Navigation', 'Precision Guidance']
Low Emissions ['Eco-Friendly', 'Emission-Controlled', 'Low Carbon']
Remote Control ['Wireless Control', 'App Operated', 'Remote Operation']
Foldable ROPS ['Collapsible ROPS', 'Folding Roll Bar', 'Retractable ROPS']
Foot Assisted Deck Lift ['Deck Pedal Lift', 'Foot Deck Control', 'Pedal Lifting System']
12V Charging Port ['Power Outlet', 'Charging Socket', 'Auxiliary Power Port']
Rear Hitch ['Tow Hitch', 'Trailer Hitch', 'Rear Coupler']
Blade Brake Clutch ['Blade Disengagement', 'Clutch System', 'Blade Safety Mechanism']
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
        llm_strategy.show_usage()
        return result.extracted_content


if __name__ == "__main__":
    models_data = [
{"id":"193","name":"ZXS54","brand_name":"Kioti","page_url":"https://www.kioti.com/products/zero-turn-mowers/zxs/zxs54"},
# {"id":"627","name":"Kohler EFI ECV740 with 52-in UltraCut Series 4 Deck","brand_name":"Exmark","page_url":"https://www.exmark.com/mowers/stand-on/vertex/vertex-s-series/vxs740ekc52400"},
# {"id":"58","name":"6700A E-Cut Hybrid","brand_name":"John Deere","page_url":"https://www.deere.com/en/mowers/fairway-mowers/6700a-e-cut-hybrid-fairway-mower/"},
# {"id":"661","name":"Revolt, 36-in deck","brand_name":"Bad Boy","page_url":"https://badboycountry.com/mowers/revolt"},
# {"id":"192","name":"ZXS48","brand_name":"Kioti","page_url":"https://www.kioti.com/products/zero-turn-mowers/zxs/zxs48"}
]

    for model in models_data:
        extracted_content = asyncio.run(
            extract_key_features(
                url=model["page_url"]
            )
        )
        if extracted_content:
            extracted_content = json.loads(extracted_content)
        KeyFeaturesModel.add_key_features_entry(
            model_id=model["id"],model_name=model["name"], brand_name=model["brand_name"], key_features=extracted_content
        )
