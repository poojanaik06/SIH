import { motion } from "framer-motion"
import { Mail, Phone, MapPin, Send } from "lucide-react"

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

export default function ContactPage() {
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
            Contact Us
          </h1>
          <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto">
            Get in touch with our team and let's discuss how we can help optimize your farming operations.
          </p>
        </motion.div>

        <motion.div 
          className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div 
            className="space-y-8"
            variants={itemVariants}
          >
            <div className="bg-card/50 backdrop-blur-sm rounded-2xl p-6 sm:p-8 border border-border/50 shadow-lg">
              <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-6">Get In Touch</h2>
              <div className="space-y-6">
                <motion.div 
                  className="flex items-start space-x-4 p-4 rounded-xl hover:bg-accent/50 transition-colors duration-300"
                  whileHover={{ scale: 1.02, x: 5 }}
                  transition={{ duration: 0.2 }}
                >
                  <motion.div
                    className="flex-shrink-0 w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center"
                    whileHover={{ rotate: 360 }}
                    transition={{ duration: 0.6 }}
                  >
                    <Mail className="h-6 w-6 text-primary" />
                  </motion.div>
                  <div>
                    <h3 className="font-semibold text-foreground text-lg mb-1">Email</h3>
                    <p className="text-muted-foreground">contact@cropai.com</p>
                    <p className="text-sm text-muted-foreground/80">We'll respond within 24 hours</p>
                  </div>
                </motion.div>
                
                <motion.div 
                  className="flex items-start space-x-4 p-4 rounded-xl hover:bg-accent/50 transition-colors duration-300"
                  whileHover={{ scale: 1.02, x: 5 }}
                  transition={{ duration: 0.2 }}
                >
                  <motion.div
                    className="flex-shrink-0 w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center"
                    whileHover={{ scale: 1.2 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Phone className="h-6 w-6 text-primary" />
                  </motion.div>
                  <div>
                    <h3 className="font-semibold text-foreground text-lg mb-1">Phone</h3>
                    <p className="text-muted-foreground">+1 (555) 123-4567</p>
                    <p className="text-sm text-muted-foreground/80">Mon-Fri 9AM-6PM EST</p>
                  </div>
                </motion.div>
                
                <motion.div 
                  className="flex items-start space-x-4 p-4 rounded-xl hover:bg-accent/50 transition-colors duration-300"
                  whileHover={{ scale: 1.02, x: 5 }}
                  transition={{ duration: 0.2 }}
                >
                  <motion.div
                    className="flex-shrink-0 w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center"
                    whileHover={{ y: -3 }}
                    transition={{ duration: 0.3 }}
                  >
                    <MapPin className="h-6 w-6 text-primary" />
                  </motion.div>
                  <div>
                    <h3 className="font-semibold text-foreground text-lg mb-1">Address</h3>
                    <p className="text-muted-foreground">
                      123 Agriculture Lane<br />
                      Farm City, FC 12345<br />
                      United States
                    </p>
                  </div>
                </motion.div>
              </div>
            </div>
          </motion.div>

          <motion.div 
            className="bg-card/50 backdrop-blur-sm rounded-2xl p-6 sm:p-8 border border-border/50 shadow-lg"
            variants={itemVariants}
          >
            <h2 className="text-2xl sm:text-3xl font-bold text-foreground mb-6">Send Message</h2>
            <form className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                <motion.div
                  whileFocus={{ scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                >
                  <label className="block text-sm font-medium text-foreground mb-2">First Name</label>
                  <input 
                    type="text" 
                    className="w-full px-4 py-3 border border-input rounded-xl bg-background/50 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all duration-300" 
                    placeholder="John"
                  />
                </motion.div>
                <motion.div
                  whileFocus={{ scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                >
                  <label className="block text-sm font-medium text-foreground mb-2">Last Name</label>
                  <input 
                    type="text" 
                    className="w-full px-4 py-3 border border-input rounded-xl bg-background/50 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all duration-300" 
                    placeholder="Doe"
                  />
                </motion.div>
              </div>
              
              <motion.div
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              >
                <label className="block text-sm font-medium text-foreground mb-2">Email</label>
                <input 
                  type="email" 
                  className="w-full px-4 py-3 border border-input rounded-xl bg-background/50 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all duration-300" 
                  placeholder="your@email.com"
                />
              </motion.div>
              
              <motion.div
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              >
                <label className="block text-sm font-medium text-foreground mb-2">Subject</label>
                <input 
                  type="text" 
                  className="w-full px-4 py-3 border border-input rounded-xl bg-background/50 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all duration-300" 
                  placeholder="How can we help you?"
                />
              </motion.div>
              
              <motion.div
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              >
                <label className="block text-sm font-medium text-foreground mb-2">Message</label>
                <textarea 
                  rows={6} 
                  className="w-full px-4 py-3 border border-input rounded-xl bg-background/50 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all duration-300 resize-none" 
                  placeholder="Tell us about your farming needs and how we can help..."
                ></textarea>
              </motion.div>
              
              <motion.button 
                type="submit" 
                className="w-full py-4 px-6 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-all duration-300 font-medium text-lg shadow-lg hover:shadow-xl flex items-center justify-center space-x-2"
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                transition={{ duration: 0.2 }}
              >
                <span>Send Message</span>
                <motion.div
                  whileHover={{ x: 5 }}
                  transition={{ duration: 0.2 }}
                >
                  <Send className="h-5 w-5" />
                </motion.div>
              </motion.button>
            </form>
          </motion.div>
        </motion.div>
        
        {/* Additional CTA Section */}
        <motion.div 
          className="mt-16 sm:mt-24 text-center"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
        >
          <div className="bg-gradient-to-r from-primary/10 via-primary/5 to-primary/10 rounded-2xl p-8 sm:p-12 border border-primary/20">
            <h3 className="text-2xl sm:text-3xl font-bold text-foreground mb-4">
              Ready to transform your farming?
            </h3>
            <p className="text-lg text-muted-foreground mb-6 max-w-2xl mx-auto">
              Join thousands of farmers who are already using CropAI to optimize their operations and increase yields.
            </p>
            <motion.button
              className="px-8 py-4 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-all duration-300 font-medium shadow-lg hover:shadow-xl"
              whileHover={{ scale: 1.05, y: -2 }}
              whileTap={{ scale: 0.95 }}
            >
              Get Started Today
            </motion.button>
          </div>
        </motion.div>
      </div>
    </motion.main>
  )
}