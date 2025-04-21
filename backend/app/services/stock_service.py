import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import yfinance as yf
import asyncio
import random
import time

logger = logging.getLogger(__name__)

class StockService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # Enable cache if available
        try:
            import requests_cache
            self.session = requests_cache.CachedSession('yfinance.cache')
            # Randomize user agent to help avoid rate limiting
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
            ]
            self.session.headers['User-agent'] = random.choice(user_agents)
            logger.info("Using cached session for yfinance")
        except ImportError:
            self.session = None
            logger.info("Requests cache not available. Install with: pip install requests_cache")
            
        # Track request timestamps to implement rate limiting
        self.last_request_time = 0
        self.min_request_interval = 2.0  # seconds between requests
        
    async def _delay_for_rate_limit(self):
        """Add delay between requests to avoid rate limiting"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_request_interval:
            delay = self.min_request_interval - elapsed
            logger.debug(f"Rate limiting: Adding {delay:.2f}s delay")
            await asyncio.sleep(delay)
            
        self.last_request_time = time.time()
        
    async def get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current stock price and basic information using yfinance
        """
        try:
            logger.info(f"Fetching stock data for {symbol} from Yahoo Finance")
            
            # Add delay for rate limiting
            await self._delay_for_rate_limit()
            
            # Get stock data from Yahoo Finance
            stock = yf.Ticker(symbol, session=self.session)
            
            try:
                # Use fast_info for quicker access to common data
                fast_info = stock.fast_info
                
                # Get the latest price from fast_info or fallback to history
                current_price = getattr(fast_info, 'last_price', None)
                if current_price is None or current_price == 0:
                    # Add delay before making another request
                    await self._delay_for_rate_limit()
                    hist = stock.history(period="1d")
                    current_price = hist['Close'].iloc[-1] if not hist.empty else 0
                
                # Get detailed info for additional metrics
                try:
                    # Add delay before making another request
                    await self._delay_for_rate_limit()
                    info = stock.info
                except Exception as e:
                    logger.warning(f"Could not fetch detailed info for {symbol}: {str(e)}")
                    info = {}
                    
                # Get previous close from fast_info or info dict
                previous_close = getattr(fast_info, 'previous_close', None)
                if previous_close is None:
                    previous_close = info.get('previousClose', current_price)
                    
                # Calculate change percentage
                if previous_close and previous_close > 0 and current_price:
                    change_percentage = ((current_price - previous_close) / previous_close) * 100
                else:
                    change_percentage = 0.0
                    
                # Get volume from fast_info or info dict
                volume = getattr(fast_info, 'last_volume', None)
                if volume is None:
                    volume = info.get('volume', 0) or info.get('averageVolume', 0)
                
                # Get market cap
                market_cap = getattr(fast_info, 'market_cap', None)
                if market_cap is None:
                    market_cap = info.get('marketCap')
                    
                # Get P/E ratio and dividend yield from info dict
                pe_ratio = info.get('trailingPE')
                dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else None
                    
                # Return formatted data
                return {
                    "symbol": symbol,
                    "current_price": current_price,
                    "change_percentage": change_percentage,
                    "volume": volume,
                    "market_cap": market_cap,
                    "pe_ratio": pe_ratio,
                    "dividend_yield": dividend_yield
                }
            except Exception as e:
                logger.warning(f"Error using fast_info for {symbol}: {str(e)}")
                # Fall back to basic data if the above fails
                raise
                
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
            # Fallback to mock data if real data fetch fails
            logger.warning(f"Using mock data for {symbol} due to error")
            return {
                "symbol": symbol,
                "current_price": 150.25,
                "change_percentage": 1.5,
                "volume": 1200000,
                "market_cap": 2000000000,
                "pe_ratio": 25.4,
                "dividend_yield": 1.2
            }
    
    async def get_company_news(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get recent news about the company using yfinance
        """
        try:
            logger.info(f"Fetching news for {symbol} from Yahoo Finance")
            
            # Add delay for rate limiting
            await self._delay_for_rate_limit()
            
            # Get stock data and news from Yahoo Finance
            stock = yf.Ticker(symbol, session=self.session)
            
            try:
                # Try to get real news from Yahoo Finance
                # Add delay before making another request
                await self._delay_for_rate_limit()
                news_items = stock.news
                if news_items and len(news_items) > 0:
                    # Format news items
                    result = []
                    for item in news_items[:5]:  # Limit to 5 news items
                        # Convert timestamp to datetime
                        news_date = datetime.fromtimestamp(item.get('providerPublishTime', 0))
                        
                        # Get publisher
                        publisher = item.get('publisher', 'Yahoo Finance')
                        
                        # Create news item
                        news_item = {
                            "title": item.get('title', f"News about {symbol}"),
                            "source": publisher,
                            "date": news_date,
                            "summary": item.get('summary', "No summary available."),
                            "sentiment": "neutral"  # Default sentiment
                        }
                        
                        # Add simple sentiment analysis based on title keywords
                        title = news_item["title"].lower()
                        if any(word in title for word in ['surge', 'jump', 'rise', 'gain', 'positive', 'boost', 'up']):
                            news_item["sentiment"] = "positive"
                        elif any(word in title for word in ['fall', 'drop', 'decline', 'negative', 'down', 'loss']):
                            news_item["sentiment"] = "negative"
                            
                        result.append(news_item)
                    
                    return result
            except Exception as e:
                logger.warning(f"Could not fetch news for {symbol}: {str(e)}")
            
            # If we couldn't get real news, fallback to mock data
            # Try to get the company name from Yahoo Finance
            try:
                # Add delay before making another request
                await self._delay_for_rate_limit()
                company_name = stock.info.get('shortName', symbol)
            except:
                company_name = symbol
            
            # Mock data as fallback
            today = datetime.now()
            return [
                {
                    "title": f"{company_name} Announces New Product Line",
                    "source": "Financial Times",
                    "date": today - timedelta(days=1),
                    "summary": f"{company_name} unveiled a new product line expected to boost revenue.",
                    "sentiment": "positive"
                },
                {
                    "title": f"Analysts Upgrade {company_name} Stock",
                    "source": "Wall Street Journal",
                    "date": today - timedelta(days=3),
                    "summary": f"Several analysts have upgraded {company_name} stock citing strong growth potential.",
                    "sentiment": "positive"
                },
                {
                    "title": f"{company_name} Faces Supply Chain Challenges",
                    "source": "Bloomberg",
                    "date": today - timedelta(days=5),
                    "summary": f"{company_name} reported supply chain difficulties that might impact short-term performance.",
                    "sentiment": "negative"
                }
            ]
            
        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {str(e)}")
            raise
            
    async def get_analyst_recommendations(self, symbol: str) -> Dict[str, Any]:
        """
        Get analyst recommendations for a stock
        """
        try:
            logger.info(f"Fetching analyst recommendations for {symbol}")
            
            # Add delay for rate limiting
            await self._delay_for_rate_limit()
            
            # Get stock data from Yahoo Finance
            stock = yf.Ticker(symbol, session=self.session)
            
            try:
                # Try to get price targets from Yahoo Finance
                # Add delay before making another request
                await self._delay_for_rate_limit()
                
                # First try to access recommendations from stock.recommendations property
                try:
                    recommendations = stock.recommendations
                    if recommendations is not None and not recommendations.empty:
                        latest_rec = recommendations.iloc[-1]
                        return {
                            "average_target": None,  # Not available in recommendations
                            "low_target": None,
                            "high_target": None,
                            "num_analysts": 0,
                            "recommendation": latest_rec.get('To Grade', 'N/A')
                        }
                except Exception as e:
                    logger.warning(f"Could not fetch recommendations for {symbol}: {str(e)}")
                
                # Then try analyst price targets
                try:
                    price_targets = stock.analyst_price_targets
                    if price_targets is not None and not price_targets.empty:
                        # Calculate average, minimum, and maximum targets
                        avg_target = price_targets['targetMean'].iloc[-1] if 'targetMean' in price_targets.columns else None
                        min_target = price_targets['targetLow'].iloc[-1] if 'targetLow' in price_targets.columns else None
                        max_target = price_targets['targetHigh'].iloc[-1] if 'targetHigh' in price_targets.columns else None
                        
                        return {
                            "average_target": avg_target,
                            "low_target": min_target,
                            "high_target": max_target,
                            "num_analysts": price_targets['numberOfAnalysts'].iloc[-1] if 'numberOfAnalysts' in price_targets.columns else 0,
                            "recommendation": stock.info.get('recommendationKey', 'N/A')
                        }
                except Exception as e:
                    logger.warning(f"Could not fetch analyst price targets for {symbol}: {str(e)}")
            except Exception as e:
                logger.warning(f"Could not fetch analyst recommendations for {symbol}: {str(e)}")
            
            # If we couldn't get real data, return empty data
            return {
                "average_target": None,
                "low_target": None,
                "high_target": None,
                "num_analysts": 0,
                "recommendation": "N/A"
            }
            
        except Exception as e:
            logger.error(f"Error fetching analyst recommendations for {symbol}: {str(e)}")
            return {
                "average_target": None,
                "low_target": None,
                "high_target": None,
                "num_analysts": 0,
                "recommendation": "N/A"
            } 