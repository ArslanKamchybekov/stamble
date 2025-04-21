# Stamble Backend

The backend for Stamble, an AI-powered stock investment recommendation system using OpenAI agents.

## Features

- Python-based FastAPI backend
- AI agent system for stock analysis and recommendations
- Web searching for recent company news
- Stock performance data integration
- Investment advice based on data analysis

## Setup

1. Create a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables by copying the example file:

```bash
cp .env.example .env
```

4. Edit the `.env` file and add your OpenAI API key.

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

- `GET /api/stocks/{symbol}/recommendation` - Get an investment recommendation for a specific stock
- `GET /api/stocks/trending` - Get a list of trending stocks

## Architecture

The backend follows a modular design with the following components:

- **AI Agents**: Classes implementing the AI recommendation logic
- **Models**: Pydantic data models for request/response validation
- **Services**: External data providers and business logic
- **Utils**: Configuration, exceptions, and helper functions 