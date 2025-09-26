"use client"

import { TrendingUp, TrendingDown, Minus } from "lucide-react"

export function PredictionCard({ result }) {
  // Default data if no result is provided
  const defaultResult = {
    predictedYield: 8.7,
    confidence: 89,
    trend: "up",
    factors: [
      { name: "Soil Quality", value: "Excellent", impact: "positive" },
      { name: "Weather", value: "Favorable", impact: "positive" },
      { name: "Pest Risk", value: "Low", impact: "positive" },
      { name: "Irrigation", value: "Optimal", impact: "positive" }
    ],
    recommendations: [
      "Continue current irrigation schedule",
      "Monitor for pest activity in next 2 weeks",
      "Consider nitrogen supplementation in 3 weeks"
    ]
  }
  
  const displayResult = result || defaultResult

  const getTrendIcon = () => {
    switch (displayResult.trend) {
      case "up":
        return <TrendingUp className="h-4 w-4 text-green-500" />
      case "down":
        return <TrendingDown className="h-4 w-4 text-red-500" />
      default:
        return <Minus className="h-4 w-4 text-yellow-500" />
    }
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return "bg-green-500"
    if (confidence >= 60) return "bg-yellow-500"
    return "bg-red-500"
  }

  return (
    <div className="w-full max-w-2xl mx-auto bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
      <div className="p-6">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            Yield Prediction
            {getTrendIcon()}
          </h3>
          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium text-white ${getConfidenceColor(displayResult.confidence)}`}>
            {displayResult.confidence}% Confidence
          </span>
        </div>
        <p className="text-sm text-muted-foreground">AI-powered crop yield analysis</p>
      </div>
      <div className="p-6 pt-0 space-y-6">
        <div className="text-center">
          <div className="text-3xl font-bold text-green-600">{displayResult.predictedYield.toFixed(1)} tons/hectare</div>
          <p className="text-sm text-muted-foreground">Predicted Yield</p>
        </div>

        {displayResult.factors && (
          <div className="space-y-3">
            <h4 className="font-semibold">Key Factors</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {displayResult.factors.map((factor, index) => (
                <div key={index} className="flex items-center justify-between p-2 rounded-lg bg-muted">
                  <span className="text-sm">{factor.name}</span>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    factor.impact === "positive"
                      ? "bg-green-500/20 text-green-400"
                      : factor.impact === "negative"
                        ? "bg-red-500/20 text-red-400"
                        : "bg-gray-500/20 text-gray-400"
                  }`}>
                    {factor.value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {displayResult.recommendations && (
          <div className="space-y-3">
            <h4 className="font-semibold">Recommendations</h4>
            <ul className="space-y-2">
              {displayResult.recommendations.map((rec, index) => (
                <li key={index} className="text-sm text-muted-foreground flex items-start gap-2">
                  <span className="text-green-500 mt-1">•</span>
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}