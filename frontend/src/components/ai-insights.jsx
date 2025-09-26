"use client"

import { Brain, TrendingUp, AlertCircle, CheckCircle, Clock, ArrowRight } from "lucide-react"

const insights = [
  {
    id: 1,
    type: "recommendation",
    priority: "high",
    title: "Optimize Irrigation Schedule",
    description:
      "North Field soil moisture is optimal. Reduce irrigation by 15% to save water while maintaining yield.",
    impact: "+$2,400 savings",
    confidence: 94,
    action: "Adjust Schedule",
    icon: TrendingUp,
  },
  {
    id: 2,
    type: "alert",
    priority: "medium",
    title: "Pest Risk Detected",
    description: "Weather conditions favor corn borer development. Consider preventive treatment in the next 3-5 days.",
    impact: "Prevent 8-12% yield loss",
    confidence: 87,
    action: "View Details",
    icon: AlertCircle,
  },
  {
    id: 3,
    type: "prediction",
    priority: "low",
    title: "Harvest Window Forecast",
    description:
      "Optimal harvest window for South Field soybeans predicted for September 15-22 based on weather patterns.",
    impact: "Maximize quality",
    confidence: 91,
    action: "Plan Harvest",
    icon: Clock,
  },
  {
    id: 4,
    type: "success",
    priority: "info",
    title: "Fertilizer Application Success",
    description: "Recent nitrogen application in West Field showing excellent uptake. Crop health improved by 12%.",
    impact: "+8% yield potential",
    confidence: 96,
    action: "View Report",
    icon: CheckCircle,
  },
]

const getPriorityColor = (priority) => {
  switch (priority) {
    case "high":
      return "bg-red-500/20 text-red-400 border-red-500/30"
    case "medium":
      return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
    case "low":
      return "bg-blue-500/20 text-blue-400 border-blue-500/30"
    case "info":
      return "bg-green-500/20 text-green-400 border-green-500/30"
    default:
      return "bg-gray-500/20 text-gray-400 border-gray-500/30"
  }
}

const getTypeIcon = (type) => {
  switch (type) {
    case "recommendation":
      return TrendingUp
    case "alert":
      return AlertCircle
    case "prediction":
      return Clock
    case "success":
      return CheckCircle
    default:
      return Brain
  }
}

export function AIInsights() {
  return (
    <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
      <div className="p-6">
        <h3 className="text-foreground flex items-center text-lg font-semibold">
          <Brain className="h-5 w-5 mr-2 text-primary" />
          AI-Powered Insights
        </h3>
        <p className="text-muted-foreground text-sm mt-1">
          Personalized recommendations based on your farm data
        </p>
      </div>
      <div className="p-6 pt-0">
        <div className="space-y-4">
          {insights.map((insight) => {
            const IconComponent = getTypeIcon(insight.type)
            return (
              <div key={insight.id} className="p-4 bg-accent/30 rounded-lg">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-primary/20 rounded-lg">
                      <IconComponent className="h-4 w-4 text-primary" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-foreground">{insight.title}</h4>
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getPriorityColor(insight.priority)}`}>
                        {insight.priority}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-primary font-medium">{insight.impact}</div>
                    <div className="text-xs text-muted-foreground">{insight.confidence}% confidence</div>
                  </div>
                </div>

                <p className="text-muted-foreground text-sm mb-4 leading-relaxed">{insight.description}</p>

                <div className="flex items-center justify-between">
                  <div className="text-xs text-muted-foreground">AI Analysis • Just now</div>
                  <button className="px-3 py-1 text-sm border border-input bg-transparent hover:bg-accent hover:text-accent-foreground rounded-md transition-colors flex items-center">
                    {insight.action}
                    <ArrowRight className="h-3 w-3 ml-1" />
                  </button>
                </div>
              </div>
            )
          })}
        </div>

        <div className="mt-6 pt-4 border-t border-border">
          <button className="w-full px-4 py-2 border border-input bg-transparent hover:bg-accent hover:text-accent-foreground rounded-md transition-colors flex items-center justify-center">
            View All Insights
            <ArrowRight className="h-4 w-4 ml-2" />
          </button>
        </div>
      </div>
    </div>
  )
}