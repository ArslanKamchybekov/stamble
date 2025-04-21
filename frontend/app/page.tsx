"use client";

import { useState } from "react";
import { SearchIcon } from "lucide-react";
import StockRecommendation from "./components/StockRecommendation";
// import TrendingStocks from "./components/TrendingStocks";

export default function Home() {
  const [stockSymbol, setStockSymbol] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [recommendation, setRecommendation] = useState(null);
  const [error, setError] = useState("");

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!stockSymbol) {
      setError("Please enter a stock symbol");
      return;
    }
    
    setIsLoading(true);
    setError("");
    
    try {
      const response = await fetch(`http://localhost:8000/api/stocks/${stockSymbol}/recommendation`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch recommendation: ${response.statusText}`);
      }
      
      const data = await response.json();
      setRecommendation(data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch recommendation. Please try again.");
      setRecommendation(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-4">
          <h1 className="text-5xl font-bold text-blue-900 mb-4">Stamble</h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered stock recommendations based on news analysis and performance data
          </p>
        </div>
        
        <div className="max-w-xl mx-auto mb-8">
          <form onSubmit={handleSearch} className="flex gap-2">
            <div className="flex-1 relative text-black">
              <input
                type="text"
                value={stockSymbol}
                onChange={(e) => setStockSymbol(e.target.value.toUpperCase())}
                placeholder="Enter stock symbol (e.g. AAPL)"
                className="w-full px-4 py-3 text-lg rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {error && <p className="text-red-500 mt-2">{error}</p>}
            </div>
            <button
              type="submit"
              disabled={isLoading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 transition-colors disabled:bg-gray-400"
            >
              {isLoading ? (
                <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
              ) : (
                <>
                  <SearchIcon size={20} />
                  <span>Analyze</span>
                </>
              )}
            </button>
          </form>
        </div>
        
        {recommendation && (
          <StockRecommendation recommendation={recommendation} />
        )}
{/*         
        <div className="mt-16">
          <TrendingStocks />
        </div> */}
      </div>
    </main>
  );
}
