import { useState } from "react"
import { Link, useLocation } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import { Sprout, Menu, X } from "lucide-react"

export function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const location = useLocation()

  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/'
    }
    return location.pathname.startsWith(path)
  }

  return (
    <motion.nav 
      className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-border"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <motion.div
                whileHover={{ rotate: 360, scale: 1.1 }}
                transition={{ duration: 0.3 }}
              >
                <Sprout className="h-8 w-8 text-primary" />
              </motion.div>
              <motion.span 
                className="text-xl font-bold text-foreground"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.2 }}
              >
                CropAI
              </motion.span>
            </Link>
          </div>

          <div className="hidden md:block">
            <motion.div 
              className="ml-10 flex items-baseline space-x-8"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link 
                  to="/" 
                  className={`transition-colors duration-300 ${
                    isActive('/') 
                      ? 'text-primary font-semibold' 
                      : 'text-muted-foreground hover:text-primary'
                  }`}
                >
                  Home
                </Link>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link 
                  to="/about" 
                  className={`transition-colors duration-300 ${
                    isActive('/about') 
                      ? 'text-primary font-semibold' 
                      : 'text-muted-foreground hover:text-primary'
                  }`}
                >
                  About
                </Link>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link 
                  to="/contact" 
                  className={`transition-colors duration-300 ${
                    isActive('/contact') 
                      ? 'text-primary font-semibold' 
                      : 'text-muted-foreground hover:text-primary'
                  }`}
                >
                  Contact
                </Link>
              </motion.div>

            </motion.div>
          </div>

          <motion.div 
            className="hidden md:flex items-center space-x-4"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <Link to="/login">
              <motion.button 
                className={`px-4 py-2 text-sm font-medium transition-colors duration-300 ${
                  isActive('/login') 
                    ? 'text-primary font-semibold' 
                    : 'text-muted-foreground hover:text-primary'
                }`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Sign In
              </motion.button>
            </Link>
            <Link to="/signup">
              <motion.button 
                className={`px-4 py-2 text-sm font-medium rounded-md transition-all duration-300 shadow-lg hover:shadow-xl ${
                  isActive('/signup')
                    ? 'bg-primary text-primary-foreground ring-2 ring-primary/50'
                    : 'bg-primary text-primary-foreground hover:bg-primary/90'
                }`}
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
              >
                Get Started
              </motion.button>
            </Link>
          </motion.div>

          <div className="md:hidden">
            <motion.button 
              className="p-2 text-foreground hover:text-primary transition-colors" 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              <AnimatePresence mode="wait">
                {isMenuOpen ? (
                  <motion.div
                    key="close"
                    initial={{ rotate: -90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: 90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <X className="h-5 w-5" />
                  </motion.div>
                ) : (
                  <motion.div
                    key="menu"
                    initial={{ rotate: 90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: -90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Menu className="h-5 w-5" />
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.button>
          </div>
        </div>

        <AnimatePresence>
          {isMenuOpen && (
            <motion.div 
              className="md:hidden"
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3, ease: "easeInOut" }}
            >
              <motion.div 
                className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-card border-t border-border"
                initial={{ y: -20 }}
                animate={{ y: 0 }}
                transition={{ duration: 0.3, delay: 0.1 }}
              >
                <motion.div
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <Link 
                    to="/" 
                    className={`block px-3 py-2 transition-colors duration-300 rounded-md hover:bg-accent ${
                      isActive('/') 
                        ? 'text-primary font-semibold bg-primary/10' 
                        : 'text-muted-foreground hover:text-primary'
                    }`}
                  >
                    Home
                  </Link>
                </motion.div>
                <motion.div
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.3 }}
                >
                  <Link 
                    to="/about" 
                    className={`block px-3 py-2 transition-colors duration-300 rounded-md hover:bg-accent ${
                      isActive('/about') 
                        ? 'text-primary font-semibold bg-primary/10' 
                        : 'text-muted-foreground hover:text-primary'
                    }`}
                  >
                    About
                  </Link>
                </motion.div>
                <motion.div
                  initial={{ x: -20, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  <Link 
                    to="/contact" 
                    className={`block px-3 py-2 transition-colors duration-300 rounded-md hover:bg-accent ${
                      isActive('/contact') 
                        ? 'text-primary font-semibold bg-primary/10' 
                        : 'text-muted-foreground hover:text-primary'
                    }`}
                  >
                    Contact
                  </Link>
                </motion.div>

                <motion.div 
                  className="flex flex-col space-y-2 px-3 py-2"
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  <Link to="/login">
                    <motion.button 
                      className={`w-full px-4 py-2 text-sm font-medium transition-colors duration-300 rounded-md hover:bg-accent ${
                        isActive('/login') 
                          ? 'text-primary font-semibold bg-primary/10' 
                          : 'text-muted-foreground hover:text-primary'
                      }`}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      Sign In
                    </motion.button>
                  </Link>
                  <Link to="/signup">
                    <motion.button 
                      className={`w-full px-4 py-2 text-sm font-medium rounded-md transition-all duration-300 shadow-md hover:shadow-lg ${
                        isActive('/signup')
                          ? 'bg-primary text-primary-foreground ring-2 ring-primary/50'
                          : 'bg-primary text-primary-foreground hover:bg-primary/90'
                      }`}
                      whileHover={{ scale: 1.02, y: -1 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      Get Started
                    </motion.button>
                  </Link>
                </motion.div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.nav>
  )
}