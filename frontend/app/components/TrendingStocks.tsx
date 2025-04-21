import React, { useEffect, useState } from 'react';
import { TrendingUp, Loader2 } from 'lucide-react';

interface TrendingStock {
  symbol: string;
  company_name: string;
  trend_score: number;
}

const TrendingStocks: React.FC = () => {
  const [trendingStocks, setTrendingStocks] = useState<TrendingStock[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTrendingStocks = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/stocks/trending');
        
        if (!response.ok) {
          throw new Error(`Failed to fetch trending stocks: ${response.statusText}`);
        }
        
        const data = await response.json();
        setTrendingStocks(data);
      } catch (err) {
        console.error(err);
        setError('Failed to load trending stocks.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchTrendingStocks();
  }, []);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loader2 className="animate-spin text-blue-600 mr-2" size={24} />
        <span className="text-gray-600">Loading trending stocks...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center gap-2 mb-6">
        <TrendingUp className="text-blue-600" size={24} />
        <h2 className="text-2xl font-bold text-gray-800">Trending Stocks</h2>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {trendingStocks.map((stock) => (
          <div 
            key={stock.symbol} 
            className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow border border-gray-100"
          >
            <div className="flex justify-between items-center">
              <div>
                <h3 className="font-bold text-lg">{stock.symbol}</h3>
                <p className="text-gray-600 text-sm">{stock.company_name}</p>
              </div>
              <div className="bg-blue-50 text-blue-800 px-3 py-1 rounded-full text-sm font-medium flex items-center">
                <span>Score:</span>
                <span className="ml-1 text-blue-600 font-bold">{(stock.trend_score * 100).toFixed(0)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TrendingStocks; 