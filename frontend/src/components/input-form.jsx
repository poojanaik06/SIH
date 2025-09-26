"use client"

import { useState } from "react"

export function InputForm({ onPrediction }) {
  const [formData, setFormData] = useState({
    soilType: "",
    temperature: 0,
    humidity: 0,
    rainfall: 0,
    ndvi: 0,
    cropType: "",
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // Simulate API call
      const result = {
        predictedYield: Math.random() * 100 + 50,
        confidence: Math.random() * 30 + 70,
        recommendations: ["Increase irrigation", "Apply fertilizer", "Monitor pest activity"]
      }
      onPrediction && onPrediction(result)
    } catch (error) {
      console.error("Prediction failed:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <div className="w-full max-w-2xl mx-auto border rounded-lg bg-card">
      <div className="p-6">
        <h3 className="text-lg font-semibold">Crop Yield Prediction</h3>
        <p className="text-sm text-muted-foreground">Enter your field data to get AI-powered yield predictions</p>
      </div>
      <div className="p-6 pt-0">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label htmlFor="cropType" className="text-sm font-medium">Crop Type</label>
              <select 
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("cropType", e.target.value)}
              >
                <option value="">Select crop type</option>
                <option value="wheat">Wheat</option>
                <option value="corn">Corn</option>
                <option value="rice">Rice</option>
                <option value="soybean">Soybean</option>
                <option value="cotton">Cotton</option>
              </select>
            </div>

            <div className="space-y-2">
              <label htmlFor="soilType" className="text-sm font-medium">Soil Type</label>
              <select 
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("soilType", e.target.value)}
              >
                <option value="">Select soil type</option>
                <option value="clay">Clay</option>
                <option value="sandy">Sandy</option>
                <option value="loamy">Loamy</option>
                <option value="silty">Silty</option>
              </select>
            </div>

            <div className="space-y-2">
              <label htmlFor="temperature" className="text-sm font-medium">Temperature (°C)</label>
              <input
                id="temperature"
                type="number"
                placeholder="25"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("temperature", parseFloat(e.target.value))}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="humidity" className="text-sm font-medium">Humidity (%)</label>
              <input
                id="humidity"
                type="number"
                placeholder="65"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("humidity", parseFloat(e.target.value))}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="rainfall" className="text-sm font-medium">Rainfall (mm)</label>
              <input
                id="rainfall"
                type="number"
                placeholder="150"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("rainfall", parseFloat(e.target.value))}
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="ndvi" className="text-sm font-medium">NDVI Value</label>
              <input
                id="ndvi"
                type="number"
                step="0.01"
                placeholder="0.75"
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                onChange={(e) => handleInputChange("ndvi", parseFloat(e.target.value))}
              />
            </div>
          </div>

          <button 
            type="submit" 
            className="w-full h-10 px-4 py-2 bg-primary text-primary-foreground hover:bg-primary/90 rounded-md font-medium transition-colors" 
            disabled={loading}
          >
            {loading ? "Predicting..." : "Get Yield Prediction"}
          </button>
        </form>
      </div>
    </div>
  )
}