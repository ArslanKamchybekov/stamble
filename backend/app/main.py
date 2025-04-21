import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import asyncio
import time

from .utils.config import Config
from .utils.exceptions import StambleError, ConfigurationError, AIAgentError
from .models.stock import StockRecommendation
from .ai_agents.investment_advisor_agent import InvestmentAdvisorAgent

# Setup logging
Config.setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Stamble API",
    description="AI-Powered Stock Investment Recommendation API",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the investment advisor agent
async def get_investment_advisor():
    try:
        # Validate configuration
        Config.validate()
        return InvestmentAdvisorAgent(api_key=Config.OPENAI_API_KEY)
    except ConfigurationError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server configuration error: {str(e)}")

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Simple rate limiting based on client IP
    client_ip = request.client.host
    # In a real app, you'd use Redis or another store to track request counts
    response = await call_next(request)
    return response

# Error handler
@app.exception_handler(StambleError)
async def stamble_exception_handler(request: Request, exc: StambleError):
    if isinstance(exc, AIAgentError):
        status_code = 503  # Service Unavailable
    else:
        status_code = 500  # Internal Server Error
    
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to Stamble API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": time.time(),
        "config": Config.as_dict()
    }

@app.get("/api/stocks/{symbol}/recommendation", response_model=StockRecommendation)
async def get_stock_recommendation(
    symbol: str, 
    advisor: InvestmentAdvisorAgent = Depends(get_investment_advisor)
):
    """
    Get investment recommendation for a specific stock symbol
    """
    try:
        logger.info(f"Received recommendation request for {symbol}")
        recommendation = await advisor.get_recommendation(symbol)
        return recommendation
    except Exception as e:
        logger.error(f"Error processing recommendation for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")

@app.get("/api/stocks/trending", response_model=List[Dict[str, Any]])
async def get_trending_stocks():
    """
    Get a list of trending stocks based on recent news and performance
    """
    # For MVP, return hardcoded data
    return [
        {"symbol": "AAPL", "company_name": "Apple Inc.", "trend_score": 0.92},
        {"symbol": "MSFT", "company_name": "Microsoft Corporation", "trend_score": 0.89},
        {"symbol": "GOOGL", "company_name": "Alphabet Inc.", "trend_score": 0.87},
        {"symbol": "AMZN", "company_name": "Amazon.com, Inc.", "trend_score": 0.85},
        {"symbol": "TSLA", "company_name": "Tesla, Inc.", "trend_score": 0.82},
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=Config.PORT, reload=Config.DEBUG) 