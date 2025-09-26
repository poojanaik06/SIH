// API service functions for making HTTP requests
export class ApiService {
  static baseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000"
  static token = localStorage.getItem('auth_token')

  // Helper method to get headers with authentication
  static getHeaders() {
    const headers = {
      "Content-Type": "application/json",
    }
    
    // Only add auth header if token exists
    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`
    }
    
    return headers
  }

  // Authentication methods
  static async login(email, password) {
    try {
      const response = await fetch(`${this.baseUrl}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: email,
          password: password
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        this.token = data.access_token
        localStorage.setItem('auth_token', this.token)
        return { success: true, data }
      } else {
        const error = await response.json()
        return { success: false, error }
      }
    } catch (error) {
      console.error("Login error:", error)
      return { success: false, error: "Network error" }
    }
  }

  static async register(email, password) {
    try {
      const response = await fetch(`${this.baseUrl}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password })
      })
      
      if (response.ok) {
        const data = await response.json()
        return { success: true, data }
      } else {
        const error = await response.json()
        return { success: false, error }
      }
    } catch (error) {
      console.error("Registration error:", error)
      return { success: false, error: "Network error" }
    }
  }

  static logout() {
    this.token = null
    localStorage.removeItem('auth_token')
  }

  // Crop prediction API - Updated to use integrated backend
  static async predictYield(data) {
    try {
      // Validate required fields before sending
      const requiredFields = ['area', 'crop', 'year', 'temperature', 'rainfall', 'pesticides'];
      const missingFields = [];
      
      requiredFields.forEach(field => {
        const altNames = {
          'area': ['area_name'],
          'crop': ['crop_name'],
          'temperature': ['avg_temp'],
          'rainfall': ['rainfall_mm'],
          'pesticides': ['pesticide_tonnes']
        };
        
        let hasValue = data[field] !== undefined && data[field] !== null && data[field] !== '';
        
        if (!hasValue && altNames[field]) {
          hasValue = altNames[field].some(alt => 
            data[alt] !== undefined && data[alt] !== null && data[alt] !== ''
          );
        }
        
        if (!hasValue) {
          missingFields.push(field);
        }
      });
      
      if (missingFields.length > 0) {
        return {
          success: false,
          error: `Please provide all required fields: ${missingFields.join(', ')}`,
          predictedYield: null,
          requiredFields: requiredFields
        };
      }
      
      const response = await fetch(`${this.baseUrl}/predict/`, {
        method: "POST",
        headers: this.getHeaders(),
        body: JSON.stringify({
          area_name: data.area || data.area_name,
          crop_name: data.crop || data.crop_name,
          year: data.year,
          avg_temp: data.temperature || data.avg_temp,
          rainfall_mm: data.rainfall || data.rainfall_mm,
          pesticide_tonnes: data.pesticides || data.pesticide_tonnes
        }),
      })
      
      if (response.ok) {
        const result = await response.json()
        return {
          success: true,
          predictedYield: result.predicted_yield,
          confidence: result.confidence || 'high',
          unit: result.unit || 'hg/ha',
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
      } else {
        const error = await response.json()
        throw new Error(error.detail || 'Prediction failed')
      }
    } catch (error) {
      console.error("Prediction API error:", error)
      // Return error instead of mock data
      return {
        success: false,
        error: error.message || "Network error - unable to connect to prediction service",
        predictedYield: null
      }
    }
  }

  // Batch prediction API
  static async predictYieldBatch(dataArray) {
    try {
      const response = await fetch(`${this.baseUrl}/predict/batch`, {
        method: "POST",
        headers: this.getHeaders(),
        body: JSON.stringify(dataArray.map(data => ({
          area_name: data.area || data.area_name,
          crop_name: data.crop || data.crop_name,
          year: data.year || new Date().getFullYear(),
          avg_temp: data.temperature || data.avg_temp || 22,
          rainfall_mm: data.rainfall || data.rainfall_mm || 800,
          pesticide_tonnes: data.pesticides || data.pesticide_tonnes || 100
        }))),
      })
      
      if (response.ok) {
        return await response.json()
      } else {
        const error = await response.json()
        throw new Error(error.detail || 'Batch prediction failed')
      }
    } catch (error) {
      console.error("Batch prediction API error:", error)
      return { success: false, error: error.message }
    }
  }

  // Model info API
  static async getModelInfo() {
    try {
      const response = await fetch(`${this.baseUrl}/predict/model-info`, {
        method: "GET",
        headers: this.getHeaders(),
      })
      
      if (response.ok) {
        return await response.json()
      } else {
        return { error: 'Failed to get model info' }
      }
    } catch (error) {
      console.error("Model info API error:", error)
      return { error: error.message }
    }
  }

  // Health check API
  static async healthCheck() {
    try {
      const response = await fetch(`${this.baseUrl}/predict/health`)
      return await response.json()
    } catch (error) {
      console.error("Health check error:", error)
      return { status: 'error', error: error.message }
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