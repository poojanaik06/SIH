import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { 
  Sprout, 
  Satellite, 
  Droplets, 
  Thermometer, 
  Sun, 
  Bug, 
  Zap, 
  Calendar, 
  MapPin, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  Plus,
  Edit,
  Trash2,
  Eye
} from "lucide-react"
import { Link, useNavigate } from "react-router-dom"

export default function FieldManagementPage() {
  const [fields, setFields] = useState([])
  const [selectedField, setSelectedField] = useState(null)
  const [showAddField, setShowAddField] = useState(false)
  const navigate = useNavigate()

  // Sample field data
  useEffect(() => {
    const sampleFields = [
      {
        id: 1,
        name: "North Field",
        crop: "Corn",
        area: "125 acres",
        planted: "2024-04-15",
        status: "excellent",
        health: 94,
        soilMoisture: 68,
        temperature: 24,
        ph: 6.8,
        nitrogen: 85,
        phosphorus: 70,
        potassium: 92,
        growthStage: "Tasseling",
        irrigation: "Active",
        lastWatered: "2024-09-20",
        pests: "None detected",
        diseases: "Healthy",
        expectedHarvest: "2024-10-15",
        location: { lat: 40.7128, lng: -74.0060 }
      },
      {
        id: 2,
        name: "South Field",
        crop: "Soybeans",
        area: "89 acres",
        planted: "2024-05-01",
        status: "good",
        health: 87,
        soilMoisture: 45,
        temperature: 26,
        ph: 7.1,
        nitrogen: 78,
        phosphorus: 65,
        potassium: 88,
        growthStage: "Flowering",
        irrigation: "Scheduled",
        lastWatered: "2024-09-18",
        pests: "Low aphid count",
        diseases: "Healthy",
        expectedHarvest: "2024-11-01",
        location: { lat: 40.7589, lng: -73.9851 }
      },
      {
        id: 3,
        name: "East Field",
        crop: "Wheat",
        area: "156 acres",
        planted: "2024-03-20",
        status: "warning",
        health: 78,
        soilMoisture: 32,
        temperature: 22,
        ph: 6.5,
        nitrogen: 62,
        phosphorus: 58,
        potassium: 75,
        growthStage: "Grain Filling",
        irrigation: "Needs attention",
        lastWatered: "2024-09-15",
        pests: "Rust detected",
        diseases: "Minor fungal infection",
        expectedHarvest: "2024-09-30",
        location: { lat: 40.6892, lng: -74.0445 }
      }
    ]
    setFields(sampleFields)
  }, [])

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

  const getStatusIcon = (status) => {
    switch (status) {
      case "excellent":
        return <CheckCircle className="h-4 w-4" />
      case "good":
        return <CheckCircle className="h-4 w-4" />
      case "warning":
        return <AlertTriangle className="h-4 w-4" />
      case "critical":
        return <AlertTriangle className="h-4 w-4" />
      default:
        return <CheckCircle className="h-4 w-4" />
    }
  }

  return (
    <motion.div 
      className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 pt-20 pb-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div 
          className="mb-8 flex justify-between items-center"
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div>
            <h1 className="text-3xl font-bold text-foreground mb-2">Field Management</h1>
            <p className="text-muted-foreground">
              Monitor and manage all your agricultural fields in one place
            </p>
          </div>
          <motion.button
            onClick={() => setShowAddField(true)}
            className="inline-flex items-center space-x-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Plus className="h-4 w-4" />
            <span>Add Field</span>
          </motion.button>
        </motion.div>

        {/* Fields Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-8">
          {fields.map((field, index) => (
            <motion.div
              key={field.id}
              className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-6"
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.4 + index * 0.1 }}
              whileHover={{ scale: 1.02, y: -5 }}
            >
              {/* Field Header */}
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-foreground">{field.name}</h3>
                  <p className="text-sm text-muted-foreground">{field.crop} • {field.area}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(field.status)} space-x-1`}>
                    {getStatusIcon(field.status)}
                    <span>{field.status}</span>
                  </span>
                </div>
              </div>

              {/* Key Metrics */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-green-500/20 rounded-lg">
                    <Sprout className="h-4 w-4 text-green-500" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Health</p>
                    <p className="font-semibold text-foreground">{field.health}%</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-500/20 rounded-lg">
                    <Droplets className="h-4 w-4 text-blue-500" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Moisture</p>
                    <p className="font-semibold text-foreground">{field.soilMoisture}%</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-orange-500/20 rounded-lg">
                    <Thermometer className="h-4 w-4 text-orange-500" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Temp</p>
                    <p className="font-semibold text-foreground">{field.temperature}°C</p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-purple-500/20 rounded-lg">
                    <Calendar className="h-4 w-4 text-purple-500" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Stage</p>
                    <p className="font-semibold text-foreground text-xs">{field.growthStage}</p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex space-x-2">
                <motion.button
                  onClick={() => setSelectedField(field)}
                  className="flex-1 flex items-center justify-center space-x-2 px-3 py-2 bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Eye className="h-4 w-4" />
                  <span>Details</span>
                </motion.button>
                
                <motion.button
                  className="px-3 py-2 bg-secondary text-secondary-foreground rounded-lg hover:bg-secondary/80 transition-colors"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Edit className="h-4 w-4" />
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Field Details Modal */}
        {selectedField && (
          <motion.div 
            className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            onClick={() => setSelectedField(null)}
          >
            <motion.div 
              className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto"
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-foreground">{selectedField.name}</h2>
                  <p className="text-muted-foreground">{selectedField.crop} Field - {selectedField.area}</p>
                </div>
                <button
                  onClick={() => setSelectedField(null)}
                  className="p-2 hover:bg-accent rounded-lg transition-colors"
                >
                  ✕
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Soil Analysis */}
                <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-4">
                  <h3 className="font-semibold text-foreground mb-3 flex items-center space-x-2">
                    <div className="p-1 bg-brown-500/20 rounded">
                      <div className="w-4 h-4 bg-amber-600 rounded"></div>
                    </div>
                    <span>Soil Analysis</span>
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">pH Level</span>
                      <span className="font-medium">{selectedField.ph}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Nitrogen</span>
                      <span className="font-medium">{selectedField.nitrogen}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Phosphorus</span>
                      <span className="font-medium">{selectedField.phosphorus}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Potassium</span>
                      <span className="font-medium">{selectedField.potassium}%</span>
                    </div>
                  </div>
                </div>

                {/* Irrigation Status */}
                <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-4">
                  <h3 className="font-semibold text-foreground mb-3 flex items-center space-x-2">
                    <Droplets className="h-4 w-4 text-blue-500" />
                    <span>Irrigation</span>
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Status</span>
                      <span className="font-medium">{selectedField.irrigation}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Last Watered</span>
                      <span className="font-medium">{selectedField.lastWatered}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Soil Moisture</span>
                      <span className="font-medium">{selectedField.soilMoisture}%</span>
                    </div>
                  </div>
                </div>

                {/* Health & Pests */}
                <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-4">
                  <h3 className="font-semibold text-foreground mb-3 flex items-center space-x-2">
                    <Bug className="h-4 w-4 text-yellow-500" />
                    <span>Health & Pests</span>
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Overall Health</span>
                      <span className="font-medium">{selectedField.health}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Pests</span>
                      <span className="font-medium text-xs">{selectedField.pests}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Diseases</span>
                      <span className="font-medium text-xs">{selectedField.diseases}</span>
                    </div>
                  </div>
                </div>

                {/* Planting Info */}
                <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-4">
                  <h3 className="font-semibold text-foreground mb-3 flex items-center space-x-2">
                    <Calendar className="h-4 w-4 text-green-500" />
                    <span>Timeline</span>
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Planted</span>
                      <span className="font-medium">{selectedField.planted}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Growth Stage</span>
                      <span className="font-medium text-xs">{selectedField.growthStage}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Expected Harvest</span>
                      <span className="font-medium">{selectedField.expectedHarvest}</span>
                    </div>
                  </div>
                </div>

                {/* Location */}
                <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-4">
                  <h3 className="font-semibold text-foreground mb-3 flex items-center space-x-2">
                    <MapPin className="h-4 w-4 text-red-500" />
                    <span>Location</span>
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Latitude</span>
                      <span className="font-medium">{selectedField.location.lat}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Longitude</span>
                      <span className="font-medium">{selectedField.location.lng}</span>
                    </div>
                    <motion.button
                      className="w-full px-3 py-2 bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors"
                      whileHover={{ scale: 1.02 }}
                    >
                      View on Map
                    </motion.button>
                  </div>
                </div>

                {/* Actions */}
                <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-4">
                  <h3 className="font-semibold text-foreground mb-3 flex items-center space-x-2">
                    <Zap className="h-4 w-4 text-purple-500" />
                    <span>Quick Actions</span>
                  </h3>
                  <div className="space-y-2">
                    <motion.button
                      className="w-full px-3 py-2 bg-blue-500/10 text-blue-500 rounded-lg hover:bg-blue-500/20 transition-colors text-sm"
                      whileHover={{ scale: 1.02 }}
                    >
                      Schedule Irrigation
                    </motion.button>
                    <motion.button
                      className="w-full px-3 py-2 bg-green-500/10 text-green-500 rounded-lg hover:bg-green-500/20 transition-colors text-sm"
                      whileHover={{ scale: 1.02 }}
                    >
                      Apply Fertilizer
                    </motion.button>
                    <motion.button
                      className="w-full px-3 py-2 bg-yellow-500/10 text-yellow-500 rounded-lg hover:bg-yellow-500/20 transition-colors text-sm"
                      whileHover={{ scale: 1.02 }}
                    >
                      Pest Treatment
                    </motion.button>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}

        {/* Quick Stats */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          {[
            {
              title: "Total Fields",
              value: fields.length.toString(),
              icon: Satellite,
              color: "bg-blue-500",
              change: "+2 this month"
            },
            {
              title: "Total Area",
              value: `${fields.reduce((sum, field) => sum + parseInt(field.area), 0)} acres`,
              icon: MapPin,
              color: "bg-green-500",
              change: "+45 acres"
            },
            {
              title: "Avg Health",
              value: `${Math.round(fields.reduce((sum, field) => sum + field.health, 0) / fields.length)}%`,
              icon: TrendingUp,
              color: "bg-purple-500",
              change: "+5% this week"
            },
            {
              title: "Active Alerts",
              value: fields.filter(f => f.status === 'warning' || f.status === 'critical').length.toString(),
              icon: AlertTriangle,
              color: "bg-orange-500",
              change: "-2 resolved"
            }
          ].map((stat, index) => (
            <motion.div
              key={index}
              className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-6"
              whileHover={{ scale: 1.02, y: -2 }}
              transition={{ duration: 0.2 }}
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 ${stat.color} rounded-xl flex items-center justify-center`}>
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
              </div>
              <div>
                <h3 className="text-2xl font-bold text-foreground mb-1">{stat.value}</h3>
                <p className="text-muted-foreground text-sm mb-2">{stat.title}</p>
                <p className="text-xs text-green-500">{stat.change}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </motion.div>
  )
}