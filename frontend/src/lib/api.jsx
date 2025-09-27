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
      const response = await fetch(`${this.baseUrl}/auth/token`, {
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
        return { success: false, error: error.detail || "Login failed" }
      }
    } catch (error) {
      console.error("Login error:", error)
      return { success: false, error: "Network error" }
    }
  }

  static async register(userData) {
    try {
      const response = await fetch(`${this.baseUrl}/auth/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: userData.email,
          password: userData.password,
          first_name: userData.firstName,
          last_name: userData.lastName,
          farm_size: userData.farmSize
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        return { success: true, data }
      } else {
        const error = await response.json()
        return { success: false, error: error.detail || "Registration failed" }
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

  // Get current user profile
  static async getCurrentUser() {
    try {
      const response = await fetch(`${this.baseUrl}/auth/me`, {
        method: "GET",
        headers: this.getHeaders(),
      })
      
      if (response.ok) {
        const data = await response.json()
        return { success: true, data }
      } else {
        const error = await response.json()
        return { success: false, error: error.detail || "Failed to get user info" }
      }
    } catch (error) {
      console.error("Get user error:", error)
      return { success: false, error: "Network error" }
    }
  }

  // Farmer-friendly Crop prediction API - Integrated with farmer_predict.py logic
  static async predictYieldFarmerFriendly(data) {
    try {
      // Validate required fields before sending
      const requiredFields = ['location', 'crop_name'];
      const missingFields = [];
      
      requiredFields.forEach(field => {
        if (!data[field] || data[field] === '') {
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
      
      const response = await fetch(`${this.baseUrl}/predict/farmer-friendly`, {
        method: "POST",
        headers: this.getHeaders(),
        body: JSON.stringify({
          location: data.location,
          crop_name: data.crop_name,
          year: data.year,
          // Optional advanced parameters
          nitrogen: data.nitrogen,
          phosphorus: data.phosphorus,
          potassium: data.potassium,
          soil_ph: data.soil_ph,
          humidity: data.humidity,
          ndvi_avg: data.ndvi_avg,
          organic_matter: data.organic_matter,
          avg_temp: data.avg_temp,
          rainfall_mm: data.rainfall_mm,
          pesticide_tonnes: data.pesticide_tonnes
        }),
      })
      
      if (response.ok) {
        const result = await response.json()
        const modelInfo = result.model_info || {}
        
        return {
          success: true,
          predictedYield: result.predicted_yield,
          confidence: result.confidence || 'high',
          unit: result.unit || 'hg/ha',
          // Enhanced farmer-friendly information
          yieldTonnesPerHectare: modelInfo.yield_tonnes_per_hectare,
          yieldBushelsPerAcre: modelInfo.yield_bushels_per_acre,
          weatherDataSource: modelInfo.weather_data_source,
          locationGeocoded: modelInfo.location_geocoded,
          weatherFetched: modelInfo.weather_fetched,
          defaultedParameters: modelInfo.defaulted_parameters || [],
          autoFetchedWeather: modelInfo.auto_fetched_weather || [],
          regionalDefaults: modelInfo.regional_defaults_used || {},
          factors: [
            { name: "Weather Data", impact: "positive", value: modelInfo.weather_fetched ? "Auto-Fetched" : "Regional Default" },
            { name: "Soil Parameters", impact: "neutral", value: `${modelInfo.defaulted_parameters?.length || 0} defaults applied` },
            { name: "Location", impact: "positive", value: "Successfully Geocoded" }
          ],
          recommendations: [
            "🌤️ Weather data automatically retrieved from satellite",
            "🌍 Regional soil parameters applied based on your location", 
            "📊 Prediction optimized for your specific agricultural region",
            ...(modelInfo.defaulted_parameters?.length > 0 ? [
              `⚙️ ${modelInfo.defaulted_parameters.length} parameters used regional defaults`
            ] : []),
            ...(modelInfo.auto_fetched_weather?.length > 0 ? [
              `🌦️ ${modelInfo.auto_fetched_weather.length} weather parameters fetched automatically`
            ] : [])
          ]
        }
      } else {
        const error = await response.json()
        
        // Handle structured validation errors
        if (response.status === 400 && error.detail && typeof error.detail === 'object') {
          const errorDetail = error.detail
          let errorMessage = errorDetail.error || 'Validation failed'
          
          // Add suggestions if available
          if (errorDetail.suggested_crops && errorDetail.suggested_crops.length > 0) {
            errorMessage += `\n\n💡 Suggested crops for ${errorDetail.location}: ${errorDetail.suggested_crops.slice(0, 3).join(', ')}`
          }
          
          // Add climate information if available
          if (errorDetail.climate_data) {
            const climate = errorDetail.climate_data
            if (climate.temperature !== undefined || climate.rainfall !== undefined) {
              errorMessage += `\n\n🌤️ Current conditions: ${climate.temperature}°C, ${climate.rainfall}mm rainfall`
            }
          }
          
          return {
            success: false,
            error: errorMessage,
            errorType: 'validation',
            suggestedCrops: errorDetail.suggested_crops || [],
            climateData: errorDetail.climate_data || {},
            location: errorDetail.location,
            crop: errorDetail.crop
          }
        }
        
        // Handle simple string errors (legacy format)
        throw new Error(error.detail || 'Farmer-friendly prediction failed')
      }
    } catch (error) {
      console.error("Farmer-friendly Prediction API error:", error)
      return {
        success: false,
        error: error.message || "Network error - unable to connect to farmer prediction service",
        predictedYield: null
      }
    }
  }
  static async predictYieldEnhanced(data) {
    try {
      // Validate required fields before sending
      const requiredFields = ['location', 'crop_name'];
      const missingFields = [];
      
      requiredFields.forEach(field => {
        if (!data[field] || data[field] === '') {
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
      
      const response = await fetch(`${this.baseUrl}/predict/enhanced`, {
        method: "POST",
        headers: this.getHeaders(),
        body: JSON.stringify({
          location: data.location,
          crop_name: data.crop_name,
          year: data.year,
          // Optional advanced parameters
          nitrogen: data.nitrogen,
          phosphorus: data.phosphorus,
          potassium: data.potassium,
          soil_ph: data.soil_ph,
          humidity: data.humidity,
          ndvi_avg: data.ndvi_avg,
          organic_matter: data.organic_matter
        }),
      })
      
      if (response.ok) {
        const result = await response.json()
        return {
          success: true,
          predictedYield: result.predicted_yield,
          confidence: result.confidence || 'high',
          unit: result.unit || 'hg/ha',
          weatherDataSource: result.model_info?.weather_data_source || 'Weather API',
          locationGeocoded: result.model_info?.location_geocoded,
          weatherFetched: result.model_info?.weather_fetched,
          factors: [
            { name: "Weather Data", impact: "positive", value: "Automatically Fetched" },
            { name: "Location", impact: "positive", value: "Geocoded Successfully" },
            { name: "Regional Defaults", impact: "neutral", value: "Applied" }
          ],
          recommendations: [
            "Weather data automatically fetched from satellite",
            "Regional soil parameters applied based on location",
            "Prediction optimized for your specific area"
          ]
        }
      } else {
        const error = await response.json()
        throw new Error(error.detail || 'Enhanced prediction failed')
      }
    } catch (error) {
      console.error("Enhanced Prediction API error:", error)
      return {
        success: false,
        error: error.message || "Network error - unable to connect to enhanced prediction service",
        predictedYield: null
      }
    }
  }
  // Legacy Crop prediction API - Updated to use enhanced endpoint for backwards compatibility
  static async predictYield(data) {
    // Convert legacy format to enhanced format
    const enhancedData = {
      location: data.area || data.area_name || data.location,
      crop_name: data.crop || data.crop_name,
      year: data.year,
      // Map legacy fields to optional enhanced fields
      avg_temp: data.temperature || data.avg_temp,
      rainfall_mm: data.rainfall || data.rainfall_mm,
      pesticide_tonnes: data.pesticides || data.pesticide_tonnes
    };
    
    // Use the enhanced prediction method
    return this.predictYieldEnhanced(enhancedData);
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