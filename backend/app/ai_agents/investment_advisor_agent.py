import os
import logging
from typing import Dict, List, Any
import json
from datetime import datetime
import asyncio

import openai
from pydantic import BaseModel

from ..utils.exceptions import AIAgentError
from ..models.stock import StockRecommendation, StockNews, StockPerformance, SentimentAnalysis
from .web_search_agent import WebSearchAgent
from ..services.stock_service import StockService

logger = logging.getLogger(__name__)

class InvestmentAdvisorAgent:
    """
    Main AI agent that analyzes stock data and provides investment recommendations.
    Uses OpenAI SDK to make decisions based on financial data and news.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = openai.Client(api_key=self.api_key)
        self.web_search_agent = WebSearchAgent(api_key=self.api_key)
        self.stock_service = StockService()
        
    async def get_recommendation(self, symbol: str) -> StockRecommendation:
        """
        Get a comprehensive investment recommendation for a stock
        """
        try:
            logger.info(f"Generating investment recommendation for {symbol}")
            
            # First, gather all the necessary data
            stock_data_task = asyncio.create_task(self.stock_service.get_stock_price(symbol))
            news_task = asyncio.create_task(self.web_search_agent.search_company_news(symbol))
            sentiment_task = asyncio.create_task(self.web_search_agent.search_stock_sentiment(symbol))
            analyst_task = asyncio.create_task(self.stock_service.get_analyst_recommendations(symbol))
            
            # Wait for all async tasks to complete
            stock_data = await stock_data_task
            news_data = await news_task
            sentiment = await sentiment_task
            analyst_recommendations = await analyst_task
            
            # Format the data for the AI model
            prompt = self._create_analysis_prompt(symbol, stock_data, news_data, sentiment, analyst_recommendations)
            
            # Get AI recommendation
            completion = await self._get_ai_recommendation(prompt)
            
            # Parse the recommendation
            recommendation_data = json.loads(completion)
            
            # Create the StockNews objects
            news_items = []
            for news_item in news_data:
                # Handle datetime objects that may already be datetime objects from web_search_agent
                news_date = news_item["date"]
                if not isinstance(news_date, datetime):
                    # Try to parse various date formats if still a string
                    if isinstance(news_date, str):
                        try:
                            from dateutil import parser
                            news_date = parser.parse(news_date)
                        except:
                            news_date = datetime.now()
                
                news_items.append(StockNews(
                    title=news_item["title"],
                    source=news_item["source"],
                    date=news_date,
                    summary=news_item["summary"],
                    sentiment=news_item.get("sentiment", "neutral")
                ))
            
            # Create the StockPerformance object
            performance = StockPerformance(
                symbol=symbol,
                current_price=stock_data["current_price"],
                change_percentage=stock_data["change_percentage"],
                volume=stock_data["volume"],
                market_cap=stock_data.get("market_cap"),
                pe_ratio=stock_data.get("pe_ratio"),
                dividend_yield=stock_data.get("dividend_yield")
            )
            
            # Create the SentimentAnalysis object
            sentiment_analysis = SentimentAnalysis(
                symbol=symbol,
                sentiment_score=sentiment.get("sentiment_score", 0.0),
                sentiment_category=sentiment.get("sentiment_category", "neutral"),
                analyzed_articles=sentiment.get("analyzed_articles"),
                key_factors=sentiment.get("key_factors"),
                summary=sentiment.get("summary", f"Overall market sentiment for {symbol}"),
                timestamp=sentiment.get("timestamp", datetime.now())
            )
            
            # Create the final recommendation
            return StockRecommendation(
                symbol=symbol,
                company_name=recommendation_data["company_name"],
                current_price=stock_data["current_price"],
                recommendation=recommendation_data["recommendation"],
                confidence_score=recommendation_data["confidence_score"],
                rationale=recommendation_data["rationale"],
                news=news_items,
                performance=performance,
                sentiment=sentiment_analysis
            )
            
        except Exception as e:
            logger.error(f"Error generating recommendation for {symbol}: {str(e)}")
            raise AIAgentError(f"Failed to generate investment recommendation: {str(e)}")
            
    def _create_analysis_prompt(self, symbol: str, stock_data: Dict[str, Any], 
                                news_data: List[Dict[str, Any]], sentiment: Dict[str, Any],
                                analyst_recommendations: Dict[str, Any] = None) -> str:
        """
        Create a prompt for the AI model to generate an investment recommendation
        """
        # Convert the data to a string format for the prompt
        stock_data_str = json.dumps(stock_data, default=str)
        news_data_str = json.dumps(news_data, default=str)
        sentiment_str = json.dumps(sentiment, default=str)
        analyst_str = json.dumps(analyst_recommendations or {}, default=str)
        
        # Create the prompt
        return f"""
        You are an expert financial advisor. Based on the following data about {symbol}, 
        provide an investment recommendation (buy, sell, or hold).
        
        STOCK DATA:
        {stock_data_str}
        
        RECENT NEWS:
        {news_data_str}
        
        MARKET SENTIMENT:
        {sentiment_str}
        
        ANALYST RECOMMENDATIONS:
        {analyst_str}
        
        Analyze this information and provide your recommendation in JSON format with these fields:
        - company_name: The full company name
        - recommendation: "buy", "sell", or "hold"
        - confidence_score: A value from 0 to 1 indicating confidence level
        - rationale: A clear explanation of your recommendation
        
        Your response should be valid JSON only.
        """
    
    async def _get_ai_recommendation(self, prompt: str) -> str:
        """
        Get a recommendation from the OpenAI model
        """
        try:
            # Create completion with proper async handling
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a financial expert AI assistant that provides stock investment recommendations based on data analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for more consistent responses
                response_format={"type": "json_object"}
            )
            
            # Extract content from response
            content = response.choices[0].message.content
            return content
            
        except Exception as e:
            logger.error(f"Error getting AI recommendation: {str(e)}")
            raise AIAgentError(f"Failed to get AI recommendation: {str(e)}") 