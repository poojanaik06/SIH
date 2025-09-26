"use client"

import { Sprout, Droplets, Bug, AlertTriangle } from "lucide-react"

const fields = [
  {
    id: 1,
    name: "North Field",
    crop: "Corn",
    area: "125 acres",
    health: 92,
    soilMoisture: 68,
    growthStage: "Tasseling",
    alerts: 0,
    status: "excellent",
  },
  {
    id: 2,
    name: "South Field",
    crop: "Soybeans",
    area: "89 acres",
    health: 87,
    soilMoisture: 45,
    growthStage: "Flowering",
    alerts: 1,
    status: "good",
  },
  {
    id: 3,
    name: "East Field",
    crop: "Wheat",
    area: "156 acres",
    health: 78,
    soilMoisture: 32,
    growthStage: "Grain Filling",
    alerts: 2,
    status: "warning",
  },
  {
    id: 4,
    name: "West Field",
    crop: "Cotton",
    area: "203 acres",
    health: 95,
    soilMoisture: 72,
    growthStage: "Boll Development",
    alerts: 0,
    status: "excellent",
  },
]

const getStatusColor = (status) => {
  switch (status) {
    case "excellent":
      return "bg-green-500/20 text-green-400 border-green-500/30"
    case "good":
      return "bg-blue-500/20 text-blue-400 border-blue-500/30"
    case "warning":
      return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
    case "critical":
      return "bg-red-500/20 text-red-400 border-red-500/30"
    default:
      return "bg-gray-500/20 text-gray-400 border-gray-500/30"
  }
}

export function FieldStatus() {
  return (
    <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
      <div className="p-6">
        <h3 className="text-foreground text-lg font-semibold">Field Status Overview</h3>
        <p className="text-muted-foreground text-sm">Real-time monitoring of all your fields</p>
      </div>
      <div className="p-6 pt-0">
        <div className="space-y-6">
          {fields.map((field) => (
            <div key={field.id} className="p-4 bg-accent/30 rounded-lg">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h4 className="font-semibold text-foreground">{field.name}</h4>
                  <p className="text-sm text-muted-foreground">
                    {field.crop} • {field.area}
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(field.status)}`}>{field.status}</span>
                  {field.alerts > 0 && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-500/20 text-red-400 border-red-500/30 space-x-1">
                      <AlertTriangle className="h-3 w-3" />
                      <span>{field.alerts}</span>
                    </span>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <Sprout className="h-4 w-4 text-primary" />
                    <span className="text-sm text-muted-foreground">Crop Health</span>
                  </div>
                  <div className="w-full bg-secondary rounded-full h-2">
                    <div className="bg-primary h-2 rounded-full" style={{ width: `${field.health}%` }}></div>
                  </div>
                  <span className="text-xs text-muted-foreground">{field.health}%</span>
                </div>

                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <Droplets className="h-4 w-4 text-blue-400" />
                    <span className="text-sm text-muted-foreground">Soil Moisture</span>
                  </div>
                  <div className="w-full bg-secondary rounded-full h-2">
                    <div className="bg-blue-400 h-2 rounded-full" style={{ width: `${field.soilMoisture}%` }}></div>
                  </div>
                  <span className="text-xs text-muted-foreground">{field.soilMoisture}%</span>
                </div>

                <div>
                  <div className="flex items-center space-x-2 mb-2">
                    <Bug className="h-4 w-4 text-yellow-400" />
                    <span className="text-sm text-muted-foreground">Growth Stage</span>
                  </div>
                  <span className="text-sm text-foreground font-medium">{field.growthStage}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}