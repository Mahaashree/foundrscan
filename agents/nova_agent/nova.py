# nova.py
from fastapi import FastAPI
from models.schemas import IdeaInput, MarketAnalysis
from nova_parts.m1_llm import query_llm_cleaned, safe_list
from nova_parts.m3_trends import get_trend_insights
from nova_parts.market_size import estimate_market_sizes
from nova_parts.cache import store_to_cache


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running. Use /docs to test the analyze endpoint."}

@app.get("/analyze")
def fallback():
    return {"message": "Use POST /analyze with a JSON body: { 'idea': 'your startup idea' }"}

@app.post("/analyze", response_model=MarketAnalysis)
async def analyze_idea(input: IdeaInput):
    # Phase 1: Extract basic insights using LLM
    llm_data = await query_llm_cleaned(input.idea)

    # Phase 2: Extract keyword-based trends
    keywords = input.idea.lower().replace("for", "").split()[:2]
    trend_data = get_trend_insights(keywords)

    market_size_data = estimate_market_sizes(input.idea)
    print("🔍 Estimated Market:", market_size_data)

    # Build the full response
    output = {
        "industry": llm_data.get("industry", input.idea),
        "geographic_focus": llm_data.get("geographic_focus", input.idea),
        "market_size": llm_data.get("market_size_summary", "TAM: $13B, SAM: $600M, SOM: $200M"),  # String format
        "customer_segments": llm_data.get("customer_segments", [input.idea]),
        "pricing_opportunity": llm_data.get("pricing_opportunity", "Not Available"),
        "market_opportunities": llm_data.get("market_opportunities", []),
        "recent_investments": llm_data.get("recent_investments", []),
        "trends": llm_data.get("trends", ["AI adoption", "Mobile-first users"]),
        "risks": llm_data.get("risks", ["Regulatory issues", "Tech literacy gaps"]),
        "external_trends": llm_data.get("external_trends", {}),  # Optional scrape fallback
        "market_estimate": llm_data.get("market_estimate", {
            "summary": "Estimated market growth in the next 5 years is 20% CAGR.",
            "confidence": "medium"
        })
    }
    
    store_to_cache(input.idea, output)
    

    return output


