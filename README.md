# Stamble - AI-Powered Stock Investment Recommendations

Stamble is an MVP application that uses an AI agent system to analyze stock data and provide investment recommendations based on recent news and performance metrics.

## Features

- Real-time web search for the latest company news using OpenAI Agents SDK
- Analysis of stock performance data
- AI-powered investment recommendations (Buy/Sell/Hold)
- Confidence scoring for investment advice
- Sentiment analysis of recent news
- Display of news and sentiment analysis on the frontend
- Clean, responsive user interface

## Project Structure

This project consists of two main components:

- **Frontend**: A Next.js application providing the user interface
- **Backend**: A Python FastAPI application with AI agents for analysis

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
5. Edit the `.env` file and add your OpenAI API key

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## How It Works

1. User enters a stock symbol in the frontend
2. Backend AI agents gather data from multiple sources:
   - Stock performance data
   - Recent company news (using OpenAI Agents SDK's WebSearchTool)
   - Market sentiment analysis (using OpenAI Agents SDK's WebSearchTool)
3. The OpenAI-powered investment advisor agent analyzes all data
4. A comprehensive recommendation is generated and displayed to the user, including:
   - Buy/Sell/Hold recommendation
   - Stock performance metrics
   - Recent news articles
   - Sentiment analysis with score and key factors

## Technologies Used

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

### Backend
- Python 3.10+
- FastAPI
- OpenAI API
- OpenAI Agents SDK (WebSearchTool)
- Pydantic

## Limitations (MVP Version)

- Limited to basic stock analysis
- Potential rate limiting on web searches
- No user accounts or saved preferences

## Future Enhancements

- Integration with additional financial data APIs
- Portfolio management and tracking
- News feed customization
- User accounts and preferences
- Mobile application
- Email/SMS notifications for stock alerts
