from together import Together
import re
import json
from models.schemas import MarketAnalysis

client = Together(api_key="5d8cf27da8aaea81911f8a381a3feee5a89624aa2f3c25aecaec88d3a080a8a8")  # set your Together API key if needed

# Template to clean the response
def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(match.group(0)) if match else {}
    except Exception as e:
        print("❌ JSON parse error:", e)
        return {}


async def query_llm_cleaned(idea: str) -> dict:
    messy_prompt = f"""
You are a startup analyst.

Analyze the startup idea: "{idea}"

Return your findings in valid JSON using this exact structure:

{{
  "industry": "One-line name of the industry",
  "market_size": {{
    "TAM": "Total Addressable Market in USD/INR format",
    "SAM": "Serviceable Available Market in USD/INR format",
    "SOM": "Serviceable Obtainable Market in USD/INR format",
    "source": "short credible source or estimation method"
  }},
  "geographic_focus": "Region or country this idea focuses on",
  "customer_segments": ["Primary customer types like B2C, schools, hospitals"],
  "pricing_opportunity": "Short line about pricing strategy or revenue model",
  "market_opportunities": [
    "First opportunity or trend",
    "Second opportunity or trend"
  ],
  "recent_investments": [
    "Mention of any startup funding or public sector initiative related to the space",
    "Another one"
  ]
}}

Rules:
- Only return JSON. No explanation, headings, or markdown.
- Keep values short and informative.
- Do not use nested JSON beyond the market_size block.
"""

    # First step: get raw response
    raw_response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=[{"role": "user", "content": messy_prompt}]
    )
    raw = raw_response.choices[0].message.content
    return extract_json(raw)
    

def safe_list(input_list):
    return [str(x) for x in input_list if isinstance(x, str)][:2]
