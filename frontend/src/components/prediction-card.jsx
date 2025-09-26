"use client"

import { TrendingUp, TrendingDown, Minus, AlertCircle } from "lucide-react"

export function PredictionCard({ result }) {
  // Show empty state if no result
  if (!result) {
    return (
      <div className="w-full max-w-2xl mx-auto bg-gray-100 border border-gray-300 rounded-xl shadow-lg">
        <div className="p-6 text-center">
          <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-600 mb-2">No Prediction Yet</h3>
          <p className="text-sm text-gray-500">
            Fill out the form on the left and click "Get Yield Prediction" to see your results here.
          </p>
          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-700">
              🌾 Make sure to fill in all required fields for accurate predictions
            </p>
          </div>
        </div>
      </div>
    )
  }

  // Show error state if prediction failed
  if (!result.success) {
    return (
      <div className="w-full max-w-2xl mx-auto bg-red-50 border border-red-300 rounded-xl shadow-lg">
        <div className="p-6 text-center">
          <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-red-600 mb-2">Prediction Failed</h3>
          <p className="text-sm text-red-500 mb-4">
            {result.error || "Unable to generate prediction. Please check your inputs and try again."}
          </p>
          {result.requiredFields && (
            <div className="text-left bg-white p-4 rounded-lg border">
              <p className="text-sm font-medium text-gray-700 mb-2">Required fields:</p>
              <ul className="text-sm text-gray-600 space-y-1">
                {result.requiredFields.map((field, index) => (
                  <li key={index} className="flex items-center gap-2">
                    <span className="text-red-500">•</span>
                    {field}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    )
  }

  // Show successful prediction result
  const displayResult = result
  const confidence = displayResult.confidence === 'high' ? 85 : displayResult.confidence === 'medium' ? 65 : 45

  const getTrendIcon = () => {
    if (displayResult.predictedYield > 50) {
      return <TrendingUp className="h-4 w-4 text-green-500" />
    } else if (displayResult.predictedYield < 30) {
      return <TrendingDown className="h-4 w-4 text-red-500" />
    } else {
      return <Minus className="h-4 w-4 text-yellow-500" />
    }
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return "bg-green-500"
    if (confidence >= 60) return "bg-yellow-500"
    return "bg-red-500"
  }

  return (
    <div className="w-full max-w-2xl mx-auto bg-green-50 border border-green-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
      <div className="p-6">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold flex items-center gap-2 text-green-800">
            ✅ Prediction Successful
            {getTrendIcon()}
          </h3>
          <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium text-white ${getConfidenceColor(confidence)}`}>
            {displayResult.confidence} Confidence
          </span>
        </div>
        <p className="text-sm text-green-600">AI-powered crop yield analysis based on your inputs</p>
      </div>
      <div className="p-6 pt-0 space-y-6">
        <div className="text-center bg-white p-4 rounded-lg border">
          <div className="text-3xl font-bold text-green-600">
            {typeof displayResult.predictedYield === 'number' ? 
              displayResult.predictedYield.toFixed(1) : 
              parseFloat(displayResult.predictedYield).toFixed(1)
            } {displayResult.unit || 'hg/ha'}
          </div>
          <p className="text-sm text-gray-600">Predicted Yield</p>
          {displayResult.input_data_used && (
            <div className="mt-3 text-xs text-gray-500">
              <p>Based on: {displayResult.input_data_used.area}, {displayResult.input_data_used.crop}, {displayResult.input_data_used.year}</p>
            </div>
          )}
        </div>

        {displayResult.factors && (
          <div className="space-y-3">
            <h4 className="font-semibold text-gray-800">Key Factors</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {displayResult.factors.map((factor, index) => (
                <div key={index} className="flex items-center justify-between p-2 rounded-lg bg-white border">
                  <span className="text-sm">{factor.name}</span>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    factor.impact === "positive"
                      ? "bg-green-100 text-green-700"
                      : factor.impact === "negative"
                        ? "bg-red-100 text-red-700"
                        : "bg-gray-100 text-gray-700"
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
            <h4 className="font-semibold text-gray-800">Recommendations</h4>
            <ul className="space-y-2">
              {displayResult.recommendations.map((rec, index) => (
                <li key={index} className="text-sm text-gray-700 flex items-start gap-2 bg-white p-2 rounded border">
                  <span className="text-green-500 mt-1">•</span>
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        )}

        {displayResult.model_info && (
          <div className="bg-gray-50 p-3 rounded-lg border text-xs text-gray-600">
            <p><strong>Model:</strong> {displayResult.model_info.model_type}</p>
            {displayResult.model_info.is_fallback && (
              <p className="text-orange-600"><strong>Note:</strong> Using fallback model</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}