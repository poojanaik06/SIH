import { motion } from "framer-motion"
import { useInView } from "framer-motion"
import { useRef } from "react"
import { Brain, Satellite, BarChart3, Droplets, Sun, Bug, Leaf, Target } from "lucide-react"

const features = [
  {
    icon: Brain,
    title: "AI-Powered Predictions",
    description:
      "Advanced machine learning models analyze soil, weather, and crop data to predict optimal yields with 99.9% accuracy.",
  },
  {
    icon: Satellite,
    title: "Satellite Monitoring",
    description:
      "Real-time NDVI and satellite imagery provide comprehensive field monitoring and crop health assessment.",
  },
  {
    icon: BarChart3,
    title: "Data Analytics",
    description:
      "Comprehensive dashboards with actionable insights, trend analysis, and performance metrics for informed decisions.",
  },
  {
    icon: Droplets,
    title: "Smart Irrigation",
    description:
      "Optimize water usage with AI-driven irrigation recommendations based on soil moisture and weather forecasts.",
  },
  {
    icon: Sun,
    title: "Weather Integration",
    description:
      "Hyperlocal weather data and forecasting help you plan planting, harvesting, and field operations perfectly.",
  },
  {
    icon: Bug,
    title: "Pest & Disease Detection",
    description:
      "Early detection of pests and diseases using computer vision and predictive modeling to prevent crop loss.",
  },
  {
    icon: Leaf,
    title: "Sustainability Tracking",
    description:
      "Monitor and improve your environmental impact with carbon footprint tracking and sustainable farming practices.",
  },
  {
    icon: Target,
    title: "Precision Agriculture",
    description:
      "Variable rate application maps and precision farming techniques to maximize efficiency and minimize waste.",
  },
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
}

const itemVariants = {
  hidden: { y: 50, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.6,
      ease: "easeOut"
    }
  }
}

export function Features() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, margin: "-100px" })

  return (
    <section className="py-16 sm:py-24 bg-background" ref={ref}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div 
          className="text-center mb-12 sm:mb-16"
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-foreground mb-4 sm:mb-6 text-balance leading-tight">
            Powerful features for modern farming
          </h2>
          <p className="text-lg sm:text-xl text-muted-foreground max-w-3xl mx-auto text-balance leading-relaxed">
            Our comprehensive AI platform provides everything you need to optimize crop production, reduce costs, and
            increase sustainability.
          </p>
        </motion.div>

        <motion.div 
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6"
          variants={containerVariants}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="group feature-gradient border-border hover:border-primary/50 transition-all duration-300 p-6 rounded-xl border hover:shadow-lg hover:shadow-primary/10 backdrop-blur-sm"
              variants={itemVariants}
              whileHover={{ 
                scale: 1.02, 
                y: -5,
                transition: { duration: 0.2 }
              }}
              whileTap={{ scale: 0.98 }}
            >
              <motion.div 
                className="mb-4"
                whileHover={{ scale: 1.1, rotate: 5 }}
                transition={{ duration: 0.3 }}
              >
                <feature.icon className="h-10 w-10 sm:h-12 sm:w-12 text-primary group-hover:text-primary/80 transition-colors duration-300" />
              </motion.div>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: index * 0.1 + 0.3 }}
              >
                <h3 className="text-foreground font-semibold text-lg sm:text-xl mb-3 group-hover:text-primary transition-colors duration-300">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed text-sm sm:text-base group-hover:text-foreground/90 transition-colors duration-300">
                  {feature.description}
                </p>
              </motion.div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}