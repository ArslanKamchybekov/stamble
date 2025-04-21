import React from 'react';
import { ArrowUpCircle, ArrowDownCircle, MinusCircle, TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';

interface StockNewsItem {
  title: string;
  source: string;
  date: string;
  summary: string;
  sentiment: string;
}

interface StockPerformance {
  symbol: string;
  current_price: number;
  change_percentage: number;
  volume: number;
  market_cap?: number;
  pe_ratio?: number;
  dividend_yield?: number;
}

interface SentimentAnalysis {
  symbol: string;
  sentiment_score: number;
  sentiment_category: string;
  analyzed_articles?: number;
  key_factors?: string[];
  summary: string;
  timestamp: string;
}

interface RecommendationProps {
  recommendation: {
    symbol: string;
    company_name: string;
    current_price: number;
    recommendation: 'buy' | 'sell' | 'hold';
    confidence_score: number;
    rationale: string;
    news: StockNewsItem[];
    performance: StockPerformance;
    timestamp: string;
    sentiment?: SentimentAnalysis;
  };
}

const StockRecommendation: React.FC<RecommendationProps> = ({ recommendation }) => {
  // Helper function to format numbers
  const formatNumber = (num: number, isCurrency = false) => {
    if (num > 1000000000) {
      return `${isCurrency ? '$' : ''}${(num / 1000000000).toFixed(2)}B`;
    } else if (num > 1000000) {
      return `${isCurrency ? '$' : ''}${(num / 1000000).toFixed(2)}M`;
    } else if (num > 1000) {
      return `${isCurrency ? '$' : ''}${(num / 1000).toFixed(2)}K`;
    }
    return `${isCurrency ? '$' : ''}${num.toFixed(2)}`;
  };

  // Color and icon based on recommendation
  const getRecommendationDisplay = () => {
    switch (recommendation.recommendation) {
      case 'buy':
        return {
          color: 'bg-emerald-50 text-emerald-700 border-emerald-200',
          icon: <ArrowUpCircle className="text-emerald-500" size={24} />,
          text: 'BUY',
          gradientFrom: 'from-emerald-500',
          gradientTo: 'to-teal-400'
        };
      case 'sell':
        return {
          color: 'bg-rose-50 text-rose-700 border-rose-200',
          icon: <ArrowDownCircle className="text-rose-500" size={24} />,
          text: 'SELL',
          gradientFrom: 'from-rose-500',
          gradientTo: 'to-pink-400'
        };
      case 'hold':
        return {
          color: 'bg-amber-50 text-amber-700 border-amber-200',
          icon: <MinusCircle className="text-amber-500" size={24} />,
          text: 'HOLD',
          gradientFrom: 'from-amber-400',
          gradientTo: 'to-yellow-300'
        };
      default:
        return {
          color: 'bg-slate-50 text-slate-700 border-slate-200',
          icon: <MinusCircle className="text-slate-500" size={24} />,
          text: 'UNKNOWN',
          gradientFrom: 'from-slate-400',
          gradientTo: 'to-gray-300'
        };
    }
  };

  const recommendationDisplay = getRecommendationDisplay();

  // Get sentiment color
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return {
          bg: 'bg-emerald-50', 
          text: 'text-emerald-700',
          border: 'border-emerald-200',
          badge: 'bg-gradient-to-r from-emerald-500 to-teal-400'
        };
      case 'negative':
        return {
          bg: 'bg-rose-50', 
          text: 'text-rose-700',
          border: 'border-rose-200',
          badge: 'bg-gradient-to-r from-rose-500 to-pink-400'
        };
      default:
        return {
          bg: 'bg-slate-50', 
          text: 'text-slate-700',
          border: 'border-slate-200',
          badge: 'bg-gradient-to-r from-slate-400 to-gray-300'
        };
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-md overflow-hidden border border-slate-100 transition-all duration-300 hover:shadow-lg">
      <div className="p-8">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8 pb-6 border-b border-slate-100">
          <div className="flex items-center gap-4">
            <div className={`p-3 rounded-xl ${recommendationDisplay.color} border`}>
              {recommendationDisplay.icon}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-3xl font-bold text-slate-800">{recommendation.symbol}</h2>
                <div className={`px-3 py-1 rounded-full text-xs font-medium ${recommendationDisplay.color} border`}>
                  {recommendationDisplay.text}
                </div>
              </div>
              <p className="text-slate-500 mt-1">{recommendation.company_name}</p>
            </div>
          </div>
          <div className="flex flex-col items-end">
            <p className="text-3xl font-bold text-slate-800">${recommendation.current_price.toFixed(2)}</p>
            <div className="flex items-center gap-1 mt-1">
              {recommendation.performance.change_percentage >= 0 
                ? <TrendingUp size={16} className="text-emerald-500" /> 
                : <TrendingDown size={16} className="text-rose-500" />
              }
              <p className={`text-sm font-medium ${
                recommendation.performance.change_percentage >= 0 
                  ? "text-emerald-500" 
                  : "text-rose-500"
              }`}>
                {recommendation.performance.change_percentage >= 0 ? "+" : ""}
                {recommendation.performance.change_percentage.toFixed(2)}%
              </p>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Performance Metrics */}
          <div className="lg:col-span-1">
            <div className="bg-slate-50 p-5 rounded-xl border border-slate-100 h-full">
              <h3 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <BarChart3 size={18} className="text-slate-600" />
                Performance Metrics
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-slate-500">Volume</span>
                  <span className="font-medium text-slate-800">{formatNumber(recommendation.performance.volume)}</span>
                </div>
                {recommendation.performance.market_cap && (
                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Market Cap</span>
                    <span className="font-medium text-slate-800">{formatNumber(recommendation.performance.market_cap, true)}</span>
                  </div>
                )}
                {recommendation.performance.pe_ratio && (
                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">P/E Ratio</span>
                    <span className="font-medium text-slate-800">{recommendation.performance.pe_ratio.toFixed(2)}</span>
                  </div>
                )}
                {recommendation.performance.dividend_yield && (
                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Dividend Yield</span>
                    <span className="font-medium text-slate-800">{recommendation.performance.dividend_yield.toFixed(2)}%</span>
                  </div>
                )}
              </div>

              {/* Confidence Score */}
              <div className="mt-6 pt-6 border-t border-slate-200">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-slate-500">Confidence</span>
                  <span className="font-medium text-slate-800">{(recommendation.confidence_score * 100).toFixed(0)}%</span>
                </div>
                <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                  <div 
                    className={`h-full bg-gradient-to-r ${recommendationDisplay.gradientFrom} ${recommendationDisplay.gradientTo}`}
                    style={{ width: `${recommendation.confidence_score * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Middle Column: Recommendation and Sentiment */}
          <div className="lg:col-span-1">
            <div className="space-y-6">
              {/* Recommendation */}
              <div className="bg-slate-50 p-5 rounded-xl border border-slate-100">
                <h3 className="text-lg font-semibold text-slate-800 mb-3">Our Recommendation</h3>
                <p className="text-slate-700 text-sm leading-relaxed">{recommendation.rationale}</p>
              </div>

              {/* Sentiment Analysis */}
              {recommendation.sentiment && (
                <div className="bg-slate-50 p-5 rounded-xl border border-slate-100">
                  <h3 className="text-lg font-semibold text-slate-800 mb-3 flex items-center gap-2">
                    Market Sentiment
                  </h3>
                  
                  <div className="mb-4">
                    {/* Sentiment Score Visualization */}
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-slate-500 text-sm">Negative</span>
                      <span className="text-slate-500 text-sm">Positive</span>
                    </div>
                    <div className="h-2 bg-slate-200 rounded-full overflow-hidden relative mb-1">
                      <div className="absolute inset-0 flex">
                        <div className="w-1/2 h-full bg-gradient-to-r from-rose-500 to-rose-300 opacity-40"></div>
                        <div className="w-1/2 h-full bg-gradient-to-r from-emerald-300 to-emerald-500 opacity-40"></div>
                      </div>
                      <div 
                        className="h-full bg-indigo-500 w-3 rounded-full absolute top-0 transition-all duration-500"
                        style={{ 
                          left: `calc(${(recommendation.sentiment.sentiment_score + 1) / 2 * 100}% - 6px)` 
                        }}
                      ></div>
                    </div>
                    
                    <div className="flex items-center gap-2 mt-4">
                      <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                        getSentimentColor(recommendation.sentiment.sentiment_category).badge
                      } text-white`}>
                        {recommendation.sentiment.sentiment_category}
                      </div>
                      {recommendation.sentiment.analyzed_articles && (
                        <span className="text-xs text-slate-500">
                          Based on {recommendation.sentiment.analyzed_articles} articles
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <p className="text-slate-700 text-sm">{recommendation.sentiment.summary}</p>
                  
                  {recommendation.sentiment.key_factors && recommendation.sentiment.key_factors.length > 0 && (
                    <div className="mt-3">
                      <span className="text-slate-600 text-xs block mb-2">Key Factors:</span>
                      <div className="flex flex-wrap gap-1">
                        {recommendation.sentiment.key_factors.map((factor, index) => (
                          <span key={index} className="bg-white text-slate-700 px-2 py-1 rounded-full text-xs border border-slate-200">
                            {factor}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
          
          {/* Right Column: News */}
          <div className="lg:col-span-1">
            <div className="bg-slate-50 p-5 rounded-xl border border-slate-100 h-full">
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Recent News</h3>
              <div className="space-y-4 max-h-[700px] overflow-y-auto pr-2 custom-scrollbar">
                {recommendation.news.map((item, index) => {
                  const sentimentColors = getSentimentColor(item.sentiment);
                  return (
                    <div 
                      key={index} 
                      className="bg-white rounded-lg p-3 border border-slate-100 shadow-sm hover:shadow-md transition-all duration-300"
                    >
                      <h4 className="font-medium text-slate-800 text-sm">{item.title}</h4>
                      <div className="flex justify-between text-xs text-slate-500 mt-2 mb-2">
                        <span>{item.source}</span>
                        <span className={`px-2 py-0.5 rounded-full ${sentimentColors.bg} ${sentimentColors.text} border ${sentimentColors.border}`}>
                          {item.sentiment}
                        </span>
                      </div>
                      <p className="text-slate-600 text-xs">{item.summary}</p>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-slate-50 px-8 py-3 text-xs text-slate-500 border-t border-slate-100">
        Analysis generated on {new Date(recommendation.timestamp).toLocaleString()}
      </div>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #f1f5f9;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #cbd5e1;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #94a3b8;
        }
      `}</style>
    </div>
  );
};

export default StockRecommendation; 