class StambleError(Exception):
    """Base exception for all Stamble application errors"""
    pass


class WebSearchError(StambleError):
    """Error occurred during web search operations"""
    pass


class AIAgentError(StambleError):
    """Error occurred in AI agent processing"""
    pass


class StockDataError(StambleError):
    """Error retrieving or processing stock data"""
    pass


class ConfigurationError(StambleError):
    """Missing or invalid configuration"""
    pass 