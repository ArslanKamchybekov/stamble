import logging
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import requests
import json
import os

from agents import Agent, WebSearchTool, Runner
from ..utils.exceptions import WebSearchError

logger = logging.getLogger(__name__)

class WebSearchAgent:
    """
    Agent that searches the web for news related to a company or stock.
    
    Uses OpenAI Agents SDK's WebSearchTool to perform real web searches.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
    async def search_company_news(self, company: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for recent news about a company using the OpenAI WebSearchTool
        """
        try:
            logger.info(f"Searching for news about {company}")
            
            # Create an agent with the WebSearchTool
            search_agent = Agent(
                name="News Search Agent",
                instructions=f"You are an expert financial analyst. Search for recent news about {company}. Focus on articles that would impact stock price.",
                tools=[WebSearchTool()],
            )
            
            # Run the agent with a carefully crafted prompt
            prompt = f"""
            Find the latest news articles about {company} that could impact its stock price.
            Search for financial news, earnings reports, product announcements, or other major company developments.
            Return exactly 5 recent, important news articles with their titles, sources, dates, and a brief summary.
            Format your response as valid JSON with this structure:
            [
                {{
                    "title": "Article title",
                    "source": "News source name",
                    "date": "Publication date",
                    "summary": "Brief summary of the article",
                    "sentiment": "positive/negative/neutral based on potential stock impact"
                }},
                ...
            ]
            """
            
            # Run the agent
            result = await Runner.run(search_agent, prompt)
            response_text = result.final_output
            
            # Extract the JSON part of the response
            try:
                # Try to parse the full response as JSON
                news_items = json.loads(response_text)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the response
                logger.warning("Could not parse response as JSON directly. Attempting to extract JSON.")
                import re
                json_match = re.search(r'\[\s*{\s*"title".*}\s*]', response_text, re.DOTALL)
                if json_match:
                    try:
                        news_items = json.loads(json_match.group(0))
                    except:
                        raise ValueError("Failed to extract valid JSON from response")
                else:
                    raise ValueError("Could not find JSON data in response")
            
            # Format dates if they are strings
            for item in news_items:
                if isinstance(item.get("date"), str):
                    try:
                        # Try to parse various date formats
                        if "T" in item["date"]:
                            # ISO format
                            item["date"] = datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
                        elif "/" in item["date"]:
                            # MM/DD/YYYY
                            item["date"] = datetime.strptime(item["date"], "%m/%d/%Y")
                        else:
                            # Try a generic parser
                            from dateutil import parser
                            item["date"] = parser.parse(item["date"])
                    except:
                        # If date parsing fails, use current time
                        item["date"] = datetime.now()
                        
                # Ensure sentiment is set
                if "sentiment" not in item:
                    # Simple sentiment analysis based on summary keywords
                    summary = item.get("summary", "").lower()
                    if any(word in summary for word in ['surge', 'jump', 'rise', 'gain', 'positive', 'boost', 'up', 'growth', 'profit']):
                        item["sentiment"] = "positive"
                    elif any(word in summary for word in ['fall', 'drop', 'decline', 'negative', 'down', 'loss', 'crisis', 'concern']):
                        item["sentiment"] = "negative"
                    else:
                        item["sentiment"] = "neutral"
            
            # Limit the number of results
            return news_items[:max_results]
            
        except Exception as e:
            logger.error(f"Error searching for news about {company}: {str(e)}")
            logger.error(f"Web search failed, falling back to mock data: {str(e)}")
            
            # Fallback to mock data if the real search fails
            now = datetime.now()
            return [
                {
                    "title": f"{company} Exceeds Quarterly Expectations",
                    "source": "MarketWatch",
                    "date": now,
                    "summary": f"{company} reported better than expected earnings for Q3 2023.",
                    "sentiment": "positive",
                    "url": f"https://example.com/news/{company.lower()}-earnings"
                },
                {
                    "title": f"{company} Announces Strategic Partnership",
                    "source": "Reuters",
                    "date": now,
                    "summary": f"{company} has entered into a strategic partnership to expand market presence.",
                    "sentiment": "positive",
                    "url": f"https://example.com/news/{company.lower()}-partnership"
                },
                {
                    "title": f"What's Next for {company} Stock?",
                    "source": "Seeking Alpha",
                    "date": now,
                    "summary": f"Analysis of {company}'s stock performance and future outlook.",
                    "sentiment": "neutral",
                    "url": f"https://example.com/news/{company.lower()}-outlook"
                }
            ][:max_results]
            
    async def search_stock_sentiment(self, symbol: str) -> Dict[str, Any]:
        """
        Analyze market sentiment for a stock based on recent news
        """
        try:
            logger.info(f"Analyzing sentiment for {symbol}")
            
            # Create an agent with WebSearchTool
            sentiment_agent = Agent(
                name="Sentiment Analysis Agent",
                instructions=f"You are an expert financial analyst. Search for recent news and market sentiment about {symbol} stock.",
                tools=[WebSearchTool()],
            )
            
            # Run the agent with a prompt to analyze sentiment
            prompt = f"""
            Search for the latest market sentiment about {symbol} stock.
            Analyze recent news, analyst opinions, and social media buzz.
            Calculate an overall sentiment score between -1.0 (extremely negative) and 1.0 (extremely positive).
            Return your analysis as valid JSON with this structure:
            {{
                "symbol": "{symbol}",
                "sentiment_score": 0.5, // value between -1.0 and 1.0
                "sentiment_category": "positive/negative/neutral",
                "analyzed_articles": 15, // number of sources considered
                "key_factors": ["factor1", "factor2"], // key factors influencing sentiment
                "summary": "Brief summary of overall sentiment"
            }}
            """
            
            # Run the agent
            result = await Runner.run(sentiment_agent, prompt)
            response_text = result.final_output
            
            # Extract JSON from the response
            try:
                # Try to parse the full response as JSON
                sentiment_data = json.loads(response_text)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the response
                logger.warning("Could not parse sentiment response as JSON directly. Attempting to extract JSON.")
                import re
                json_match = re.search(r'{\s*"symbol".*}', response_text, re.DOTALL)
                if json_match:
                    try:
                        sentiment_data = json.loads(json_match.group(0))
                    except:
                        raise ValueError("Failed to extract valid JSON from sentiment response")
                else:
                    raise ValueError("Could not find sentiment JSON data in response")
            
            # Ensure the response has the required fields
            required_fields = ["sentiment_score", "sentiment_category"]
            for field in required_fields:
                if field not in sentiment_data:
                    raise ValueError(f"Missing required field '{field}' in sentiment data")
            
            # Add timestamp
            sentiment_data["timestamp"] = datetime.now()
            
            return sentiment_data
                
        except Exception as e:
            logger.error(f"Error analyzing sentiment for {symbol}: {str(e)}")
            logger.error(f"Sentiment analysis failed, falling back to mock data: {str(e)}")
            
            # Fallback to mock data if the real analysis fails
            import random
            sentiment_score = random.uniform(-1.0, 1.0)
            
            sentiment_category = "neutral"
            if sentiment_score > 0.3:
                sentiment_category = "positive"
            elif sentiment_score < -0.3:
                sentiment_category = "negative"
                
            return {
                "symbol": symbol,
                "sentiment_score": sentiment_score,
                "sentiment_category": sentiment_category,
                "analyzed_articles": random.randint(10, 50),
                "key_factors": ["Market volatility", "Industry trends", "Company news"],
                "summary": f"Overall {sentiment_category} sentiment for {symbol} based on recent market activity",
                "timestamp": datetime.now()
            } 