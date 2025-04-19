

from pydantic import BaseModel
from typing import List, Dict, Optional


class IdeaInput(BaseModel):
    idea: str

class MarketAnalysis(BaseModel):
    industry: str
    geographic_focus: str
    market_size: str
    customer_segments: List[str]
    pricing_opportunity: str
    market_opportunities: List[str]
    recent_investments: List[str]
    trends: List[str]
    risks: List[str]
    external_trends: Dict[str, str] = {}
    market_estimate: Dict[str, str]