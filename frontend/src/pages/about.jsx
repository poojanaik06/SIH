import { motion } from "framer-motion"
import { Target, Eye, Users, Award, TrendingUp, Leaf } from "lucide-react"

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.2,
      delayChildren: 0.1
    }
  }
}

const itemVariants = {
  hidden: { y: 30, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.6,
      ease: "easeOut"
    }
  }
}

const impactStats = [
  { icon: TrendingUp, value: "35%", label: "Average yield increase", color: "text-green-500" },
  { icon: Leaf, value: "25%", label: "Water usage reduction", color: "text-blue-500" },
  { icon: Users, value: "1000+", label: "Farmers served", color: "text-purple-500" },
  { icon: Award, value: "99.9%", label: "Prediction accuracy", color: "text-yellow-500" }
]

export default function AboutPage() {
  return (
    <motion.main 
      className="pt-20 pb-8 min-h-screen bg-gradient-to-br from-background via-background to-primary/5"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div 
          className="text-center mb-12 sm:mb-16"
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-foreground mb-4 sm:mb-6">
            About CropAI
          </h1>
          <p className="text-lg sm:text-xl text-muted-foreground max-w-3xl mx-auto">
            Revolutionizing agriculture through artificial intelligence and data-driven insights
          </p>
        </motion.div>

        <motion.div 
          className="space-y-12 sm:space-y-16"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Mission Section */}
          <motion.section 
            className="bg-card/50 backdrop-blur-sm rounded-2xl p-6 sm:p-8 lg:p-12 border border-border/50 shadow-lg"
            variants={itemVariants}
          >
            <div className="flex items-center mb-6">
              <motion.div
                className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mr-4"
                whileHover={{ rotate: 360, scale: 1.1 }}
                transition={{ duration: 0.6 }}
              >
                <Target className="h-6 w-6 text-primary" />
              </motion.div>
              <h2 className="text-2xl sm:text-3xl font-bold text-foreground">Our Mission</h2>
            </div>
            <p className="text-muted-foreground leading-relaxed text-base sm:text-lg">
              At CropAI, we're dedicated to helping farmers maximize their crop yields while minimizing environmental impact. 
              Our AI-powered platform combines satellite imagery, weather data, soil analysis, and machine learning to provide 
              personalized recommendations that increase productivity and sustainability.
            </p>
          </motion.section>

          {/* Vision Section */}
          <motion.section 
            className="bg-card/50 backdrop-blur-sm rounded-2xl p-6 sm:p-8 lg:p-12 border border-border/50 shadow-lg"
            variants={itemVariants}
          >
            <div className="flex items-center mb-6">
              <motion.div
                className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mr-4"
                whileHover={{ scale: 1.2 }}
                transition={{ duration: 0.3 }}
              >
                <Eye className="h-6 w-6 text-primary" />
              </motion.div>
              <h2 className="text-2xl sm:text-3xl font-bold text-foreground">How It Works</h2>
            </div>
            <p className="text-muted-foreground leading-relaxed text-base sm:text-lg">
              Our platform analyzes multiple data sources including weather patterns, soil conditions, crop health indicators, 
              and historical yield data to generate accurate predictions and actionable insights. Farmers can make informed 
              decisions about irrigation, fertilization, pest control, and harvest timing.
            </p>
          </motion.section>

          {/* Impact Section */}
          <motion.section 
            className="bg-card/50 backdrop-blur-sm rounded-2xl p-6 sm:p-8 lg:p-12 border border-border/50 shadow-lg"
            variants={itemVariants}
          >
            <div className="text-center mb-8 sm:mb-12">
              <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-4">Our Impact</h2>
              <p className="text-muted-foreground text-base sm:text-lg max-w-2xl mx-auto">
                See how CropAI is transforming agriculture and helping farmers achieve better results
              </p>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
              {impactStats.map((stat, index) => (
                <motion.div 
                  key={index}
                  className="text-center p-6 rounded-xl bg-background/50 border border-border/30 hover:bg-background/70 transition-all duration-300"
                  whileHover={{ scale: 1.05, y: -5 }}
                  transition={{ duration: 0.3 }}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  whileInView={{ 
                    scale: [1, 1.1, 1],
                    transition: { duration: 0.6, delay: index * 0.1 }
                  }}
                  viewport={{ once: true }}
                >
                  <motion.div
                    className="flex justify-center mb-4"
                    whileHover={{ rotate: 360 }}
                    transition={{ duration: 0.6 }}
                  >
                    <stat.icon className={`h-8 w-8 sm:h-10 sm:w-10 ${stat.color}`} />
                  </motion.div>
                  <motion.div 
                    className="text-3xl sm:text-4xl font-bold text-foreground mb-2"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ duration: 0.5, delay: index * 0.1 + 0.3 }}
                  >
                    {stat.value}
                  </motion.div>
                  <div className="text-sm sm:text-base text-muted-foreground">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </motion.section>

          {/* Technology Section */}
          <motion.section 
            className="bg-gradient-to-r from-primary/10 via-primary/5 to-primary/10 rounded-2xl p-6 sm:p-8 lg:p-12 border border-primary/20"
            variants={itemVariants}
          >
            <div className="text-center">
              <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-4 sm:mb-6">
                Cutting-Edge Technology
              </h2>
              <p className="text-muted-foreground leading-relaxed text-base sm:text-lg mb-8 max-w-3xl mx-auto">
                We leverage the latest advancements in artificial intelligence, machine learning, and satellite technology 
                to provide farmers with unprecedented insights into their crops and land.
              </p>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 text-left">
                {[
                  { title: "Machine Learning", desc: "Advanced algorithms that learn from your farm's unique patterns" },
                  { title: "Satellite Imagery", desc: "Real-time monitoring using high-resolution satellite data" },
                  { title: "IoT Integration", desc: "Connect sensors and devices for comprehensive data collection" },
                  { title: "Weather Forecasting", desc: "Hyperlocal weather predictions for precise planning" },
                  { title: "Computer Vision", desc: "Automated crop health assessment and pest detection" },
                  { title: "Data Analytics", desc: "Transform raw data into actionable farming insights" }
                ].map((tech, index) => (
                  <motion.div
                    key={index}
                    className="p-4 rounded-xl bg-background/30 border border-border/30"
                    whileHover={{ scale: 1.02, y: -2 }}
                    transition={{ duration: 0.2 }}
                  >
                    <h3 className="font-semibold text-foreground mb-2">{tech.title}</h3>
                    <p className="text-sm text-muted-foreground">{tech.desc}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.section>
        </motion.div>
      </div>
    </motion.main>
  )
}