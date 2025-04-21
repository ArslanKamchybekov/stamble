from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StockNews(BaseModel):
    title: str
    source: str
    date: datetime
    summary: str
    sentiment: str  # positive, negative, neutral


class StockPerformance(BaseModel):
    symbol: str
    current_price: float
    change_percentage: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None


class SentimentAnalysis(BaseModel):
    symbol: str
    sentiment_score: float
    sentiment_category: str
    analyzed_articles: Optional[int] = None
    key_factors: Optional[List[str]] = None
    summary: str
    timestamp: datetime = datetime.now()


class StockRecommendation(BaseModel):
    symbol: str
    company_name: str
    current_price: float
    recommendation: str  # buy, sell, hold
    confidence_score: float  # 0 to 1
    rationale: str
    news: List[StockNews]
    performance: StockPerformance
    sentiment: Optional[SentimentAnalysis] = None
    timestamp: datetime = datetime.now() 