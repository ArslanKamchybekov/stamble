# Stamble Frontend

A minimalist Next.js frontend for the Stamble AI stock recommendation system.

## Features

- Clean, responsive UI built with Next.js and Tailwind CSS
- Real-time stock recommendation analysis
- Display of trending stocks
- Detailed stock performance and news analysis

## Getting Started

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## Backend Connection

The frontend connects to the Stamble backend at `http://localhost:8000`. Make sure the backend is running before using the application.

## Usage

1. Enter a stock symbol (e.g., AAPL, MSFT, GOOGL) in the search box
2. Click "Analyze" to get an AI-generated recommendation
3. View stock details, performance metrics, and relevant news
4. Scroll down to see trending stocks

## Build for Production

To build the application for production:

```bash
npm run build
```

Then, start the production server:

```bash
npm start
```

## Technologies Used

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Lucide React for icons
