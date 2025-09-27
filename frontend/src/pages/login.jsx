import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { Sprout, Eye, EyeOff, Mail, Lock, ArrowRight, AlertCircle } from "lucide-react"
import { validateLoginForm } from "../utils/validation"
import { ApiService } from "../lib/api"

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrors({})
    
    // Validate form
    const validation = validateLoginForm(email, password)
    if (!validation.isValid) {
      setErrors(validation.errors)
      return
    }
    
    setIsLoading(true)
    
    try {
      // Call backend API for login
      const result = await ApiService.login(email, password)
      
      if (result.success) {
        // Get user profile information
        const userResult = await ApiService.getCurrentUser()
        
        if (userResult.success) {
          // Store user session
          localStorage.setItem('user', JSON.stringify({ 
            email: userResult.data.email, 
            firstName: userResult.data.first_name,
            lastName: userResult.data.last_name,
            farmSize: userResult.data.farm_size,
            isAuthenticated: true 
          }))
          
          // Navigate to dashboard
          navigate('/dashboard')
        } else {
          setErrors({ general: "Login successful but failed to get user info. Please try again." })
        }
      } else {
        // Handle login errors with more specific messages
        console.log('Login failed:', result.error) // Debug log
        
        if (result.error && typeof result.error === 'string') {
          if (result.error.includes('Incorrect email or password')) {
            setErrors({ general: "Invalid email or password. Please check your credentials and try again." })
          } else if (result.error.includes('Network error')) {
            setErrors({ general: "Connection failed. Please check your internet connection and try again." })
          } else {
            setErrors({ general: result.error })
          }
        } else {
          setErrors({ general: "Login failed. Please verify your email and password are correct." })
        }
      }
    } catch (error) {
      console.error('Login error:', error)
      setErrors({ general: "Login failed. Please check your connection and try again." })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <motion.div 
      className="flex items-center justify-center min-h-screen pt-16 pb-8 bg-gradient-to-br from-background via-background to-primary/5"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <motion.div 
        className="w-full max-w-md mx-4"
        initial={{ y: 30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <motion.div 
          className="bg-card/80 backdrop-blur-md border border-border/50 rounded-2xl shadow-2xl overflow-hidden"
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.3 }}
        >
          <motion.div 
            className="p-6 sm:p-8 text-center bg-gradient-to-b from-primary/5 to-transparent"
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <motion.div 
              className="flex justify-center mb-6"
              whileHover={{ rotate: 360, scale: 1.1 }}
              transition={{ duration: 0.6 }}
            >
              <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center">
                <Sprout className="h-8 w-8 text-primary" />
              </div>
            </motion.div>
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground mb-2">Welcome back</h1>
            <p className="text-muted-foreground">
              Sign in to your CropAI account to access your dashboard
            </p>
          </motion.div>
          
          <motion.div 
            className="p-6 sm:p-8 pt-0"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.6 }}
          >
            <form onSubmit={handleSubmit} className="space-y-6">
              {errors.general && (
                <motion.div 
                  className="p-4 bg-red-50 border border-red-200 rounded-xl flex items-center space-x-3"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <AlertCircle className="h-5 w-5 text-red-500" />
                  <span className="text-red-700 text-sm">{errors.general}</span>
                </motion.div>
              )}
              <motion.div 
                className="space-y-2"
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              >
                <label htmlFor="email" className="text-foreground text-sm font-medium block">
                  Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                  <motion.input
                    id="email"
                    type="email"
                    placeholder="farmer@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className={`flex h-12 w-full rounded-xl border px-3 py-2 text-sm pl-11 focus:outline-none focus:ring-2 transition-all duration-300 ${
                      errors.email 
                        ? 'border-red-300 bg-red-50/50 focus:ring-red-200 focus:border-red-400' 
                        : 'border-input bg-background/50 focus:ring-primary/50 focus:border-primary'
                    }`}
                    whileFocus={{ scale: 1.02 }}
                    required
                  />
                </div>
                {errors.email && (
                  <motion.p 
                    className="text-red-500 text-sm mt-1 flex items-center space-x-1"
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <AlertCircle className="h-4 w-4" />
                    <span>{errors.email}</span>
                  </motion.p>
                )}
              </motion.div>

              <motion.div 
                className="space-y-2"
                whileFocus={{ scale: 1.02 }}
                transition={{ duration: 0.2 }}
              >
                <label htmlFor="password" className="text-foreground text-sm font-medium block">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                  <motion.input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className={`flex h-12 w-full rounded-xl border px-3 py-2 text-sm pl-11 pr-11 focus:outline-none focus:ring-2 transition-all duration-300 ${
                      errors.password 
                        ? 'border-red-300 bg-red-50/50 focus:ring-red-200 focus:border-red-400' 
                        : 'border-input bg-background/50 focus:ring-primary/50 focus:border-primary'
                    }`}
                    whileFocus={{ scale: 1.02 }}
                    required
                  />
                  <motion.button
                    type="button"
                    className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                    onClick={() => setShowPassword(!showPassword)}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-muted-foreground" />
                    ) : (
                      <Eye className="h-5 w-5 text-muted-foreground" />
                    )}
                  </motion.button>
                </div>
                {errors.password && (
                  <motion.p 
                    className="text-red-500 text-sm mt-1 flex items-center space-x-1"
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <AlertCircle className="h-4 w-4" />
                    <span>{errors.password}</span>
                  </motion.p>
                )}
              </motion.div>

              <div className="flex items-center justify-between">
                <Link
                  to="/forgot-password"
                  className="text-sm text-primary hover:text-primary/80 transition-colors duration-300"
                >
                  Forgot password?
                </Link>
              </div>

              <motion.button 
                type="submit" 
                disabled={isLoading}
                className={`w-full h-12 px-4 py-2 rounded-xl font-medium transition-all duration-300 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2 ${
                  isLoading 
                    ? 'bg-primary/50 text-primary-foreground cursor-not-allowed' 
                    : 'bg-primary text-primary-foreground hover:bg-primary/90'
                }`}
                whileHover={!isLoading ? { scale: 1.02, y: -2 } : {}}
                whileTap={!isLoading ? { scale: 0.98 } : {}}
                transition={{ duration: 0.2 }}
              >
                {isLoading ? (
                  <>
                    <motion.div
                      className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full"
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    />
                    <span>Signing In...</span>
                  </>
                ) : (
                  <>
                    <span>Sign In</span>
                    <motion.div
                      whileHover={{ x: 5 }}
                      transition={{ duration: 0.2 }}
                    >
                      <ArrowRight className="h-4 w-4" />
                    </motion.div>
                  </>
                )}
              </motion.button>
            </form>

            <motion.div 
              className="mt-8 text-center"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.8 }}
            >
              <p className="text-muted-foreground">
                Don't have an account?{" "}
                <Link to="/signup" className="text-primary hover:text-primary/80 transition-colors font-medium">
                  Sign up
                </Link>
              </p>
            </motion.div>
          </motion.div>
        </motion.div>
        
        {/* Additional features */}
        <motion.div 
          className="mt-8 text-center space-y-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1 }}
        >
          <div className="flex items-center justify-center space-x-6 text-sm text-muted-foreground">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Secure Login</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span>24/7 Support</span>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </motion.div>
  )
}