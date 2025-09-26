"use client"

import { useState } from "react"
import { ApiService } from "../lib/api"

export function InputForm({ onPrediction }) {
  const [formData, setFormData] = useState({
    location: "",
    crop: "",
    year: new Date().getFullYear(),
    // Advanced optional fields
    nitrogen: "",
    phosphorus: "",
    potassium: "",
    soil_ph: "",
    humidity: "",
    ndvi_avg: "",
    organic_matter: ""
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    // Validate required fields
    const requiredFields = ['location', 'crop']
    const missingFields = requiredFields.filter(field => !formData[field] || formData[field] === "")
    
    if (missingFields.length > 0) {
      setError(`Please fill in all required fields: ${missingFields.join(', ')}`)
      setLoading(false)
      return
    }

    try {
      // Call the farmer-friendly backend API
      const result = await ApiService.predictYieldFarmerFriendly({
        location: formData.location,
        crop_name: formData.crop,
        year: formData.year || new Date().getFullYear(),
        // Include optional advanced parameters if provided
        nitrogen: formData.nitrogen ? parseFloat(formData.nitrogen) : null,
        phosphorus: formData.phosphorus ? parseFloat(formData.phosphorus) : null,
        potassium: formData.potassium ? parseFloat(formData.potassium) : null,
        soil_ph: formData.soil_ph ? parseFloat(formData.soil_ph) : null,
        humidity: formData.humidity ? parseFloat(formData.humidity) : null,
        ndvi_avg: formData.ndvi_avg ? parseFloat(formData.ndvi_avg) : null,
        organic_matter: formData.organic_matter ? parseFloat(formData.organic_matter) : null
      })

      if (result.success) {
        onPrediction && onPrediction(result)
      } else {
        setError(result.error || "Prediction failed. Please check your inputs and try again.")
      }
    } catch (error) {
      console.error("Prediction failed:", error)
      setError("Network error. Please check your connection and try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (error) setError(null)
  }

  return (
    <div className="w-full max-w-2xl mx-auto border rounded-lg bg-card">
      <div className="p-6">
        <h3 className="text-lg font-semibold">🌾 Smart Crop Yield Prediction</h3>
        <p className="text-sm text-muted-foreground">Enter your location and crop type. Our AI will automatically fetch weather data and apply regional defaults for accurate predictions!</p>
        <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-md">
          <p className="text-xs text-blue-700">
            💡 <strong>How it works:</strong> Just enter any location (e.g., "Karnataka, India" or "California, USA") and we'll automatically:
            <br />• 🌤️ Fetch real weather data from satellites
            <br />• 📍 Get precise coordinates for your location
            <br />• 🌱 Apply regional soil and climate defaults
            <br />• ⚡ Generate accurate yield predictions
          </p>
        </div>
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}
      </div>
      <div className="p-6 pt-0">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Required Fields */}
          <div className="bg-green-50 p-4 rounded-lg border border-green-200">
            <h4 className="text-sm font-semibold text-green-800 mb-3">🌱 Required Information</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label htmlFor="location" className="text-sm font-medium">📍 Location *</label>
                <input
                  id="location"
                  type="text"
                  placeholder="e.g., Karnataka, India or California, USA"
                  value={formData.location}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  onChange={(e) => handleInputChange("location", e.target.value)}
                  required
                />
                <p className="text-xs text-gray-500">Enter any location - we'll automatically get coordinates and weather data</p>
              </div>

              <div className="space-y-2">
                <label htmlFor="crop" className="text-sm font-medium">🌾 Crop Type *</label>
                <select 
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={formData.crop}
                  onChange={(e) => handleInputChange("crop", e.target.value)}
                  required
                >
                  <option value="">Select crop type</option>
                  <option value="Wheat">Wheat</option>
                  <option value="Rice">Rice</option>
                  <option value="Maize">Maize (Corn)</option>
                  <option value="Soybean">Soybean</option>
                  <option value="Cotton">Cotton</option>
                  <option value="Barley">Barley</option>
                  <option value="Sugarcane">Sugarcane</option>
                  <option value="Potato">Potato</option>
                </select>
              </div>
            </div>
          </div>

          {/* Optional Year */}
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <h4 className="text-sm font-semibold text-blue-800 mb-3">📅 Optional: Prediction Year</h4>
            <div className="space-y-2">
              <label htmlFor="year" className="text-sm font-medium">Year (optional)</label>
              <input
                id="year"
                type="number"
                min="2020"
                max="2030"
                value={formData.year}
                className="flex h-10 w-full max-w-32 rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("year", e.target.value)}
              />
              <p className="text-xs text-gray-500">Leave as current year for best accuracy</p>
            </div>
          </div>

          {/* Advanced Optional Fields */}
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <h4 className="text-sm font-semibold text-gray-800 mb-3">🧪 Advanced Options (Optional)</h4>
            <p className="text-xs text-gray-600 mb-3">These fields are optional. If left empty, our system will use regional defaults based on your location.</p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <label htmlFor="nitrogen" className="text-sm font-medium">Nitrogen (kg/ha)</label>
                <input
                  id="nitrogen"
                  type="number"
                  step="0.1"
                  placeholder="Auto (regional default)"
                  value={formData.nitrogen}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  onChange={(e) => handleInputChange("nitrogen", e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="phosphorus" className="text-sm font-medium">Phosphorus (kg/ha)</label>
                <input
                  id="phosphorus"
                  type="number"
                  step="0.1"
                  placeholder="Auto (regional default)"
                  value={formData.phosphorus}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  onChange={(e) => handleInputChange("phosphorus", e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="potassium" className="text-sm font-medium">Potassium (kg/ha)</label>
                <input
                  id="potassium"
                  type="number"
                  step="0.1"
                  placeholder="Auto (regional default)"
                  value={formData.potassium}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  onChange={(e) => handleInputChange("potassium", e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="soil_ph" className="text-sm font-medium">Soil pH</label>
                <input
                  id="soil_ph"
                  type="number"
                  step="0.1"
                  min="0"
                  max="14"
                  placeholder="Auto (regional default)"
                  value={formData.soil_ph}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  onChange={(e) => handleInputChange("soil_ph", e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="humidity" className="text-sm font-medium">Humidity (%)</label>
                <input
                  id="humidity"
                  type="number"
                  step="0.1"
                  min="0"
                  max="100"
                  placeholder="Auto (weather API)"
                  value={formData.humidity}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  onChange={(e) => handleInputChange("humidity", e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="organic_matter" className="text-sm font-medium">Organic Matter (%)</label>
                <input
                  id="organic_matter"
                  type="number"
                  step="0.1"
                  placeholder="Auto (regional default)"
                  value={formData.organic_matter}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  onChange={(e) => handleInputChange("organic_matter", e.target.value)}
                />
              </div>
            </div>
          </div>

          <div className="text-sm text-muted-foreground bg-yellow-50 p-3 rounded-lg border border-yellow-200">
            🌟 <strong>Smart Predictions:</strong> Our AI automatically fetches real weather data, calculates coordinates, and applies regional agricultural defaults. Just provide location and crop type for accurate results!
          </div>

          <button 
            type="submit" 
            className="w-full h-12 px-4 py-2 bg-primary text-primary-foreground hover:bg-primary/90 rounded-md font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2" 
            disabled={loading}
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Analyzing Location & Fetching Weather Data...
              </>
            ) : (
              <>
                🚀 Get Smart Yield Prediction
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  )
}