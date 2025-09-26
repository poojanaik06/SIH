import { motion } from "framer-motion"
import { Link } from "react-router-dom"
import { ArrowRight, TrendingUp, Zap, Shield } from "lucide-react"

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.3,
      delayChildren: 0.2
    }
  }
}

const itemVariants = {
  hidden: { y: 30, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.8,
      ease: "easeOut"
    }
  }
}

const statsVariants = {
  hidden: { y: 50, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.8,
      ease: "easeOut",
      staggerChildren: 0.2
    }
  }
}

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center hero-gradient overflow-hidden">
      {/* Background pattern */}
      <motion.div 
        className="absolute inset-0 opacity-10"
        initial={{ scale: 1.1, opacity: 0 }}
        animate={{ scale: 1, opacity: 0.1 }}
        transition={{ duration: 1.5, ease: "easeOut" }}
      >
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fillRule='evenodd'%3E%3Cg fill='%23ffffff' fillOpacity='0.1'%3E%3Ccircle cx='30' cy='30' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />
      </motion.div>

      <motion.div 
        className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="max-w-4xl mx-auto">
          <motion.h1 
            className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-balance mb-6 leading-tight"
            variants={itemVariants}
          >
            <span className="text-foreground">Optimize crop yields with</span>{" "}
            <motion.span 
              className="text-primary inline-block"
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              AI-powered insights
            </motion.span>
          </motion.h1>

          <motion.p 
            className="text-lg sm:text-xl md:text-2xl text-muted-foreground text-balance mb-8 max-w-3xl mx-auto leading-relaxed"
            variants={itemVariants}
          >
            Transform your farming with advanced AI predictions, real-time monitoring, and data-driven recommendations
            that maximize productivity and sustainability.
          </motion.p>

          <motion.div 
            className="flex flex-col sm:flex-row gap-4 justify-center mb-12 sm:mb-16"
            variants={itemVariants}
          >
            <Link to="/signup">
              <motion.button 
                className="w-full sm:w-auto text-lg px-8 py-4 sm:py-6 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl"
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                Start Optimizing
                <motion.div
                  className="ml-2"
                  whileHover={{ x: 5 }}
                  transition={{ duration: 0.2 }}
                >
                  <ArrowRight className="h-5 w-5" />
                </motion.div>
              </motion.button>
            </Link>
            <Link to="/dashboard">
              <motion.button 
                className="w-full sm:w-auto text-lg px-8 py-4 sm:py-6 border-2 border-primary/20 bg-transparent hover:bg-primary/10 hover:border-primary/40 rounded-lg transition-all duration-300 backdrop-blur-sm"
                whileHover={{ scale: 1.02, y: -1 }}
                whileTap={{ scale: 0.98 }}
                transition={{ duration: 0.2 }}
              >
                View Demo
              </motion.button>
            </Link>
          </motion.div>

          {/* Stats */}
          <motion.div 
            className="grid grid-cols-1 sm:grid-cols-3 gap-6 sm:gap-8 max-w-4xl mx-auto"
            variants={statsVariants}
          >
            <motion.div 
              className="flex flex-col items-center p-6 rounded-xl bg-background/50 backdrop-blur-sm border border-border/50 hover:bg-background/70 transition-all duration-300"
              variants={itemVariants}
              whileHover={{ scale: 1.05, y: -5 }}
              transition={{ duration: 0.3 }}
            >
              <motion.div
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
              >
                <TrendingUp className="h-8 w-8 text-primary mb-3" />
              </motion.div>
              <div className="text-2xl sm:text-3xl font-bold text-foreground mb-1">35%</div>
              <div className="text-sm sm:text-base text-muted-foreground text-center">Average Yield Increase</div>
            </motion.div>
            <motion.div 
              className="flex flex-col items-center p-6 rounded-xl bg-background/50 backdrop-blur-sm border border-border/50 hover:bg-background/70 transition-all duration-300"
              variants={itemVariants}
              whileHover={{ scale: 1.05, y: -5 }}
              transition={{ duration: 0.3 }}
            >
              <motion.div
                whileHover={{ scale: 1.2 }}
                transition={{ duration: 0.3 }}
              >
                <Zap className="h-8 w-8 text-primary mb-3" />
              </motion.div>
              <div className="text-2xl sm:text-3xl font-bold text-foreground mb-1">24/7</div>
              <div className="text-sm sm:text-base text-muted-foreground text-center">Real-time Monitoring</div>
            </motion.div>
            <motion.div 
              className="flex flex-col items-center p-6 rounded-xl bg-background/50 backdrop-blur-sm border border-border/50 hover:bg-background/70 transition-all duration-300"
              variants={itemVariants}
              whileHover={{ scale: 1.05, y: -5 }}
              transition={{ duration: 0.3 }}
            >
              <motion.div
                whileHover={{ rotateY: 180 }}
                transition={{ duration: 0.6 }}
              >
                <Shield className="h-8 w-8 text-primary mb-3" />
              </motion.div>
              <div className="text-2xl sm:text-3xl font-bold text-foreground mb-1">99.9%</div>
              <div className="text-sm sm:text-base text-muted-foreground text-center">Prediction Accuracy</div>
            </motion.div>
          </motion.div>
        </div>
      </motion.div>
    </section>
  )
}