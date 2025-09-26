"use client"

import { useState } from "react"
import { ApiService } from "../lib/api"

export function InputForm({ onPrediction }) {
  const [formData, setFormData] = useState({
    area: "",
    crop: "",
    year: new Date().getFullYear(),
    temperature: "",
    rainfall: "",
    pesticides: ""
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    // Validate required fields
    const requiredFields = ['area', 'crop', 'temperature', 'rainfall', 'pesticides']
    const missingFields = requiredFields.filter(field => !formData[field] || formData[field] === "")
    
    if (missingFields.length > 0) {
      setError(`Please fill in all required fields: ${missingFields.join(', ')}`)
      setLoading(false)
      return
    }

    try {
      // Call the actual backend API
      const result = await ApiService.predictYield({
        area: formData.area,
        crop: formData.crop,
        year: formData.year,
        temperature: parseFloat(formData.temperature),
        rainfall: parseFloat(formData.rainfall),
        pesticides: parseFloat(formData.pesticides)
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
        <h3 className="text-lg font-semibold">Crop Yield Prediction</h3>
        <p className="text-sm text-muted-foreground">Enter your field data to get AI-powered yield predictions</p>
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}
      </div>
      <div className="p-6 pt-0">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label htmlFor="area" className="text-sm font-medium">Area/Location *</label>
              <select 
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={formData.area}
                onChange={(e) => handleInputChange("area", e.target.value)}
                required
              >
                <option value="">Select area</option>
                <option value="India">India</option>
                <option value="China">China</option>
                <option value="USA">USA</option>
                <option value="Brazil">Brazil</option>
                <option value="Argentina">Argentina</option>
              </select>
            </div>

            <div className="space-y-2">
              <label htmlFor="crop" className="text-sm font-medium">Crop Type *</label>
              <select 
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                value={formData.crop}
                onChange={(e) => handleInputChange("crop", e.target.value)}
                required
              >
                <option value="">Select crop type</option>
                <option value="Wheat">Wheat</option>
                <option value="Rice">Rice</option>
                <option value="Maize">Maize</option>
                <option value="Soybean">Soybean</option>
                <option value="Cotton">Cotton</option>
              </select>
            </div>

            <div className="space-y-2">
              <label htmlFor="year" className="text-sm font-medium">Year</label>
              <input
                id="year"
                type="number"
                min="2020"
                max="2030"
                value={formData.year}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("year", e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="temperature" className="text-sm font-medium">Average Temperature (°C) *</label>
              <input
                id="temperature"
                type="number"
                step="0.1"
                placeholder="25.5"
                value={formData.temperature}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("temperature", e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="rainfall" className="text-sm font-medium">Rainfall (mm/year) *</label>
              <input
                id="rainfall"
                type="number"
                step="0.1"
                placeholder="800"
                value={formData.rainfall}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("rainfall", e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="pesticides" className="text-sm font-medium">Pesticides (tonnes) *</label>
              <input
                id="pesticides"
                type="number"
                step="0.1"
                placeholder="120"
                value={formData.pesticides}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("pesticides", e.target.value)}
                required
              />
            </div>
          </div>

          <div className="text-sm text-muted-foreground">
            * Required fields
          </div>

          <button 
            type="submit" 
            className="w-full h-10 px-4 py-2 bg-primary text-primary-foreground hover:bg-primary/90 rounded-md font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed" 
            disabled={loading}
          >
            {loading ? "Predicting..." : "Get Yield Prediction"}
          </button>
        </form>
      </div>
    </div>
  )
}