from nova_parts.m1_llm import query_llm_cleaned
from nova_parts.cache import save_cache, store_to_cache, get_from_cache
import json



def estimate_market_from_sources(idea):
    if "telemedicine" in idea.lower():
        return {
            "TAM": "USD 130 Billion / INR 10.8 Lakh Crore",
            "SAM": "USD 5 Billion / INR 41,500 Crore",
            "SOM": "USD 0.5 Billion / INR 4,150 Crore",
            "source": "Industry Reports (IBEF, EY, Statista)"
        }
    return None


def estimate_market_via_llm(idea, region, segment):
    prompt = f"""
    Estimate the TAM, SAM, and SOM for the following startup idea in {region} ({segment} market). Format your output as JSON with keys 'TAM', 'SAM', 'SOM', and a short 'source'.

    Idea: {idea}
    """
    response = query_llm_cleaned(prompt)
    return json.loads(response)  # or parse using regex if needed




def estimate_market_sizes(idea, region="India", segment="B2C"):
    idea_key = f"{idea.lower().strip()}_{region}_{segment}"

    # Check cache first
    cached = get_from_cache(idea_key)
    if cached:
        print("⚡ Cache hit.")
        return cached

    # Check known scraped values
    scraped = estimate_market_from_sources(idea)
    if scraped:
        print("🛰️ Using scraped/static values.")
        store_to_cache(idea_key, scraped)
        return scraped

    # Use LLM fallback
    print("🔮 Using LLM fallback.")
    try:
        estimated = estimate_market_via_llm(idea, region, segment)
        store_to_cache(idea_key, estimated)
        return estimated
    except Exception as e:
        print(f"⚠️ LLM failed: {e}")
        return {
            "TAM": "Unknown",
            "SAM": "Unknown",
            "SOM": "Unknown",
            "source": "LLM Error"
        }
