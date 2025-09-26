// API service functions for making HTTP requests
export class ApiService {
  static baseUrl = import.meta.env.VITE_API_URL || "/api"

  // Crop prediction API
  static async predictYield(data) {
    try {
      const response = await fetch(`${this.baseUrl}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
      return response.json()
    } catch (error) {
      console.error("Prediction API error:", error)
      // Return mock data for demo
      return {
        predictedYield: Math.random() * 50 + 70,
        confidence: Math.random() * 30 + 70,
        factors: [
          { name: "Soil Quality", impact: "positive", value: "Good" },
          { name: "Weather", impact: "positive", value: "Favorable" },
          { name: "Irrigation", impact: "neutral", value: "Adequate" }
        ],
        recommendations: [
          "Continue current irrigation schedule",
          "Apply nitrogen fertilizer in 2 weeks",
          "Monitor for pest activity"
        ]
      }
    }
  }

  // Weather data API
  static async getWeatherData(location) {
    try {
      const response = await fetch(`${this.baseUrl}/weather?location=${location}`)
      return response.json()
    } catch (error) {
      console.error("Weather API error:", error)
      return null
    }
  }

  // Field monitoring API
  static async getFieldData(fieldId) {
    try {
      const response = await fetch(`${this.baseUrl}/fields/${fieldId}`)
      return response.json()
    } catch (error) {
      console.error("Field data API error:", error)
      return null
    }
  }

  // User management API
  static async getUsers() {
    try {
      const response = await fetch(`${this.baseUrl}/users`)
      return response.json()
    } catch (error) {
      console.error("Users API error:", error)
      return []
    }
  }

  // Analytics API
  static async getAnalytics() {
    try {
      const response = await fetch(`${this.baseUrl}/analytics`)
      return response.json()
    } catch (error) {
      console.error("Analytics API error:", error)
      return null
    }
  }
}