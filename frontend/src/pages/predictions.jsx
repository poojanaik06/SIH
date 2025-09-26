import { useState } from "react"
import { motion } from "framer-motion"
import { InputForm } from "../components/input-form"
import { PredictionCard } from "../components/prediction-card"
import { ArrowLeft } from "lucide-react"
import { Link } from "react-router-dom"

export default function PredictionsPage() {
  const [predictionResult, setPredictionResult] = useState(null)

  const handlePrediction = (result) => {
    setPredictionResult(result)
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
          className="mb-8"
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Link 
            to="/dashboard"
            className="inline-flex items-center space-x-2 text-muted-foreground hover:text-primary transition-colors mb-4"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Back to Dashboard</span>
          </Link>
          <h1 className="text-3xl font-bold text-foreground mb-2">Crop Yield Predictions</h1>
          <p className="text-muted-foreground">
            Use AI-powered analysis to predict crop yields based on environmental and field conditions
          </p>
        </motion.div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <motion.div
            initial={{ x: -30, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <InputForm onPrediction={handlePrediction} />
          </motion.div>

          {/* Prediction Results */}
          <motion.div
            initial={{ x: 30, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <PredictionCard result={predictionResult} />
          </motion.div>
        </div>

        {/* Tips Section */}
        <motion.div 
          className="mt-12 bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-6"
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <h3 className="text-xl font-semibold text-foreground mb-4">Tips for Accurate Predictions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              {
                title: "Recent Data",
                description: "Use the most recent field measurements for better accuracy"
              },
              {
                title: "Local Weather",
                description: "Consider local weather patterns and seasonal variations"
              },
              {
                title: "Soil Testing",
                description: "Regular soil testing provides more accurate soil type data"
              },
              {
                title: "NDVI Values",
                description: "NDVI values between 0.2-0.9 indicate healthy vegetation"
              },
              {
                title: "Historical Trends",
                description: "Compare with previous years' data for better insights"
              },
              {
                title: "Field Variability",
                description: "Account for variations across different areas of your field"
              }
            ].map((tip, index) => (
              <motion.div
                key={index}
                className="p-4 bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300"
                whileHover={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              >
                <h4 className="font-semibold text-foreground mb-2">{tip.title}</h4>
                <p className="text-sm text-muted-foreground">{tip.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}