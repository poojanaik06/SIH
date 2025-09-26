import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Sprout, Mail, LogOut, BarChart3 } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { DashboardCharts } from "../components/dashboard-charts"
import { WeatherWidget } from "../components/weather-widget"
import { FieldStatus } from "../components/field-status"
import { AIInsights } from "../components/ai-insights"
import { PredictionCard } from "../components/prediction-card"
import { YieldChart } from "../components/yield-chart"

export default function Dashboard() {
  const [user, setUser] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    // Check if user is authenticated
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    } else {
      navigate('/login')
    }
  }, [navigate])

  const handleLogout = () => {
    localStorage.removeItem('user')
    navigate('/')
  }

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <motion.div
          className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
      </div>
    )
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
          className="bg-card/80 backdrop-blur-md border border-border/50 rounded-2xl p-6 mb-8"
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center">
                <Sprout className="h-8 w-8 text-primary" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  Welcome back, {user.firstName || user.email}!
                </h1>
                <p className="text-muted-foreground flex items-center space-x-2 mt-1">
                  <Mail className="h-4 w-4" />
                  <span>{user.email}</span>
                </p>
              </div>
            </div>
            
          </div>
        </motion.div>

        {/* Dashboard Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Main Charts Section */}
          <div className="lg:col-span-2 space-y-6">
            <DashboardCharts />
            <FieldStatus />
          </div>
          
          {/* Sidebar Widgets */}
          <div className="space-y-6">
            <WeatherWidget />
            <PredictionCard />
          </div>
        </div>

        {/* AI Insights and Analytics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <AIInsights />
          <YieldChart />
        </div>

        {/* Success Message */}
        <motion.div 
          className="mt-8 bg-green-50 border border-green-200 rounded-2xl p-6 text-center"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <div className="flex items-center justify-center space-x-2 text-green-700">
            <Sprout className="h-6 w-6" />
            <h2 className="text-xl font-semibold">Welcome to Your Dashboard!</h2>
          </div>
          <p className="text-green-600 mt-2">
            Access all your farming tools and insights through the navigation above.
          </p>
        </motion.div>
      </div>
    </motion.div>
  )
}