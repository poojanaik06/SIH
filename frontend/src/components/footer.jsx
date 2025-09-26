import { motion } from "framer-motion"
import { Sprout, Mail, Twitter, Linkedin, Github, ArrowUp } from "lucide-react"
import { useState } from "react"

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
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.6,
      ease: "easeOut"
    }
  }
}

export function Footer() {
  const [showBackToTop, setShowBackToTop] = useState(false)
  const [clickedItem, setClickedItem] = useState(null)

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleLinkClick = (itemName) => {
    setClickedItem(itemName)
    // Reset the highlight after 300ms
    setTimeout(() => {
      setClickedItem(null)
    }, 300)
  }

  return (
    <motion.footer 
      className="bg-card/50 backdrop-blur-sm border-t border-border/50 relative overflow-hidden"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      viewport={{ once: true }}
    >
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-5">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23000000' fillOpacity='0.05'%3E%3Cpath d='M20 20c0 11.046-8.954 20-20 20v-40c11.046 0 20 8.954 20 20z'/%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />
      </div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
        <motion.div 
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          <motion.div 
            className="col-span-1 sm:col-span-2 lg:col-span-2"
            variants={itemVariants}
          >
            <motion.div 
              className="flex items-center space-x-3 mb-6"
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              <motion.div
                whileHover={{ rotate: 360 }}
                transition={{ duration: 0.6 }}
              >
                <Sprout className="h-8 w-8 text-primary" />
              </motion.div>
              <span className="text-2xl font-bold text-foreground">CropAI</span>
            </motion.div>
            <p className="text-muted-foreground mb-6 max-w-lg leading-relaxed text-base">
              Empowering farmers worldwide with AI-driven crop optimization technology. Maximize yields, reduce costs,
              and farm sustainably with our advanced platform.
            </p>
            <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-6 space-y-3 sm:space-y-0">
              <motion.div 
                className="flex items-center text-muted-foreground hover:text-primary transition-colors cursor-pointer"
                whileHover={{ scale: 1.05, x: 5 }}
                transition={{ duration: 0.2 }}
              >
                <Mail className="h-5 w-5 mr-2" />
                <span>contact@cropai.com</span>
              </motion.div>
              <div className="flex space-x-4">
                {[
                  { Icon: Twitter, href: "#", label: "Twitter" },
                  { Icon: Github, href: "#", label: "GitHub" },
                  { Icon: Linkedin, href: "#", label: "LinkedIn" }
                ].map(({ Icon, href, label }) => (
                  <motion.a
                    key={label}
                    href={href}
                    className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center text-primary hover:bg-primary hover:text-primary-foreground transition-all duration-300"
                    whileHover={{ scale: 1.1, y: -2 }}
                    whileTap={{ scale: 0.9 }}
                    aria-label={label}
                  >
                    <Icon className="h-4 w-4" />
                  </motion.a>
                ))}
              </div>
            </div>
          </motion.div>

          <motion.div variants={itemVariants}>
            <h3 className="text-foreground font-semibold mb-6 text-lg">Platform</h3>
            <ul className="space-y-3">
              {[
                { label: "Dashboard" },
                { label: "Features" },
                { label: "Pricing" },
                { label: "API" }
              ].map(({ label }) => (
                <motion.li key={label}>
                  <motion.button
                    onClick={() => handleLinkClick(`platform-${label.toLowerCase()}`)}
                    className={`text-left w-full text-muted-foreground hover:text-primary transition-all duration-300 flex items-center group ${
                      clickedItem === `platform-${label.toLowerCase()}` ? 'text-primary font-semibold' : ''
                    }`}
                    whileHover={{ scale: 1.02, x: 5 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <motion.span
                      className="group-hover:translate-x-1 transition-transform duration-200"
                    >
                      {label}
                    </motion.span>
                  </motion.button>
                </motion.li>
              ))}
            </ul>
          </motion.div>

          <motion.div variants={itemVariants}>
            <h3 className="text-foreground font-semibold mb-6 text-lg">Company</h3>
            <ul className="space-y-3">
              {[
                { label: "About" },
                { label: "Contact" },
                { label: "Careers" },
                { label: "Blog" }
              ].map(({ label }) => (
                <motion.li key={label}>
                  <motion.button
                    onClick={() => handleLinkClick(`company-${label.toLowerCase()}`)}
                    className={`text-left w-full text-muted-foreground hover:text-primary transition-all duration-300 flex items-center group ${
                      clickedItem === `company-${label.toLowerCase()}` ? 'text-primary font-semibold' : ''
                    }`}
                    whileHover={{ scale: 1.02, x: 5 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <motion.span
                      className="group-hover:translate-x-1 transition-transform duration-200"
                    >
                      {label}
                    </motion.span>
                  </motion.button>
                </motion.li>
              ))}
            </ul>
          </motion.div>
        </motion.div>

        <motion.div 
          className="border-t border-border/50 mt-12 pt-8 flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          viewport={{ once: true }}
        >
          <p className="text-muted-foreground text-sm text-center sm:text-left">
            © 2025 CropAI. All rights reserved. Built with 💚 for farmers worldwide.
          </p>
          <div className="flex items-center space-x-6">
            <motion.button
              onClick={() => handleLinkClick('privacy')}
              className={`text-sm transition-colors ${
                clickedItem === 'privacy' ? 'text-primary font-semibold' : 'text-muted-foreground hover:text-primary'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Privacy Policy
            </motion.button>
            <motion.button
              onClick={() => handleLinkClick('terms')}
              className={`text-sm transition-colors ${
                clickedItem === 'terms' ? 'text-primary font-semibold' : 'text-muted-foreground hover:text-primary'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Terms of Service
            </motion.button>
            <motion.button
              onClick={scrollToTop}
              className="ml-4 w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center text-primary hover:bg-primary hover:text-primary-foreground transition-all duration-300"
              whileHover={{ scale: 1.1, y: -2 }}
              whileTap={{ scale: 0.9 }}
              aria-label="Back to top"
            >
              <ArrowUp className="h-4 w-4" />
            </motion.button>
          </div>
        </motion.div>
      </div>
    </motion.footer>
  )
}