import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"
import { Sprout, Eye, EyeOff, Mail, Lock, User, ArrowRight, Check, AlertCircle } from "lucide-react"
import { validateSignupForm } from "../utils/validation"
import { ApiService } from "../lib/api"

export default function SignupPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    farmSize: "",
    agreeToTerms: false,
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErrors({})
    
    // Validate form
    const validation = validateSignupForm(formData)
    if (!validation.isValid) {
      setErrors(validation.errors)
      return
    }
    
    setIsLoading(true)
    
    try {
      // Call backend API for registration
      const result = await ApiService.register(formData)
      
      if (result.success) {
        // After successful registration, log in the user
        const loginResult = await ApiService.login(formData.email, formData.password)
        
        if (loginResult.success) {
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
            setErrors({ general: "Registration successful but failed to get user info. Please try logging in." })
          }
        } else {
          setErrors({ general: "Registration successful but auto-login failed. Please try logging in manually." })
        }
      } else {
        // Handle registration errors
        if (result.error && typeof result.error === 'string') {
          if (result.error.includes('already registered') || result.error.includes('already exists')) {
            setErrors({ general: "An account with this email already exists. Please sign in instead." })
          } else {
            setErrors({ general: result.error })
          }
        } else {
          setErrors({ general: "Registration failed. Please try again." })
        }
      }
    } catch (error) {
      console.error('Registration error:', error)
      setErrors({ general: "Registration failed. Please check your connection and try again." })
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <motion.div 
      className="flex items-center justify-center min-h-screen pt-16 pb-8 bg-gradient-to-br from-background via-background to-primary/5"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <motion.div 
        className="w-full max-w-lg mx-4"
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
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground mb-2">Join CropAI</h1>
            <p className="text-muted-foreground">
              Create your account and start optimizing your crop yields today
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
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <motion.div 
                  className="space-y-2"
                  whileFocus={{ scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                >
                  <label htmlFor="firstName" className="text-foreground text-sm font-medium block">
                    First Name
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                    <motion.input
                      id="firstName"
                      type="text"
                      placeholder="John"
                      value={formData.firstName}
                      onChange={(e) => handleInputChange("firstName", e.target.value)}
                      className={`flex h-12 w-full rounded-xl border px-3 py-2 text-sm pl-11 focus:outline-none focus:ring-2 transition-all duration-300 ${
                        errors.firstName 
                          ? 'border-red-300 bg-red-50/50 focus:ring-red-200 focus:border-red-400' 
                          : 'border-input bg-background/50 focus:ring-primary/50 focus:border-primary'
                      }`}
                      whileFocus={{ scale: 1.02 }}
                      required
                    />
                  </div>
                  {errors.firstName && (
                    <motion.p 
                      className="text-red-500 text-sm mt-1 flex items-center space-x-1"
                      initial={{ opacity: 0, y: -5 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <AlertCircle className="h-4 w-4" />
                      <span>{errors.firstName}</span>
                    </motion.p>
                  )}
                </motion.div>

                <motion.div 
                  className="space-y-2"
                  whileFocus={{ scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                >
                  <label htmlFor="lastName" className="text-foreground text-sm font-medium block">
                    Last Name
                  </label>
                  <motion.input
                    id="lastName"
                    type="text"
                    placeholder="Doe"
                    value={formData.lastName}
                    onChange={(e) => handleInputChange("lastName", e.target.value)}
                    className={`flex h-12 w-full rounded-xl border px-3 py-2 text-sm focus:outline-none focus:ring-2 transition-all duration-300 ${
                      errors.lastName 
                        ? 'border-red-300 bg-red-50/50 focus:ring-red-200 focus:border-red-400' 
                        : 'border-input bg-background/50 focus:ring-primary/50 focus:border-primary'
                    }`}
                    whileFocus={{ scale: 1.02 }}
                    required
                  />
                  {errors.lastName && (
                    <motion.p 
                      className="text-red-500 text-sm mt-1 flex items-center space-x-1"
                      initial={{ opacity: 0, y: -5 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <AlertCircle className="h-4 w-4" />
                      <span>{errors.lastName}</span>
                    </motion.p>
                  )}
                </motion.div>
              </div>

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
                    value={formData.email}
                    onChange={(e) => handleInputChange("email", e.target.value)}
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
                <label htmlFor="farmSize" className="text-foreground text-sm font-medium block">
                  Farm Size
                </label>
                <motion.select 
                  className={`flex h-12 w-full rounded-xl border px-3 py-2 text-sm focus:outline-none focus:ring-2 transition-all duration-300 ${
                    errors.farmSize 
                      ? 'border-red-300 bg-red-50/50 focus:ring-red-200 focus:border-red-400' 
                      : 'border-input bg-background/50 focus:ring-primary/50 focus:border-primary'
                  }`}
                  onChange={(e) => handleInputChange("farmSize", e.target.value)}
                  whileFocus={{ scale: 1.02 }}
                  required
                >
                  <option value="">Select farm size</option>
                  <option value="small">Small (1-50 acres)</option>
                  <option value="medium">Medium (51-200 acres)</option>
                  <option value="large">Large (201-1000 acres)</option>
                  <option value="enterprise">Enterprise (1000+ acres)</option>
                </motion.select>
                {errors.farmSize && (
                  <motion.p 
                    className="text-red-500 text-sm mt-1 flex items-center space-x-1"
                    initial={{ opacity: 0, y: -5 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <AlertCircle className="h-4 w-4" />
                    <span>{errors.farmSize}</span>
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
                    placeholder="Create a strong password (min. 6 characters)"
                    value={formData.password}
                    onChange={(e) => handleInputChange("password", e.target.value)}
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

              <motion.div 
                className={`flex items-start space-x-3 p-4 rounded-xl border transition-all duration-300 ${
                  errors.agreeToTerms 
                    ? 'bg-red-50/50 border-red-200' 
                    : 'bg-primary/5 border-primary/20'
                }`}
                whileHover={{ scale: 1.01 }}
                transition={{ duration: 0.2 }}
              >
                <motion.input
                  id="terms"
                  type="checkbox"
                  checked={formData.agreeToTerms}
                  onChange={(e) => handleInputChange("agreeToTerms", e.target.checked)}
                  className="w-5 h-5 mt-0.5 rounded border-2 border-primary/30 text-primary focus:ring-primary/50"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                />
                <label htmlFor="terms" className="text-sm text-muted-foreground leading-relaxed flex-1">
                  I agree to the{" "}
                  <Link to="/terms" className="text-primary hover:text-primary/80 transition-colors font-medium">
                    Terms of Service
                  </Link>{" "}
                  and{" "}
                  <Link to="/privacy" className="text-primary hover:text-primary/80 transition-colors font-medium">
                    Privacy Policy
                  </Link>
                </label>
              </motion.div>
              {errors.agreeToTerms && (
                <motion.p 
                  className="text-red-500 text-sm mt-1 flex items-center space-x-1"
                  initial={{ opacity: 0, y: -5 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <AlertCircle className="h-4 w-4" />
                  <span>{errors.agreeToTerms}</span>
                </motion.p>
              )}

              <motion.button 
                type="submit" 
                disabled={!formData.agreeToTerms || isLoading}
                className={`w-full h-12 px-4 py-2 rounded-xl font-medium transition-all duration-300 shadow-lg hover:shadow-xl flex items-center justify-center space-x-2 ${
                  !formData.agreeToTerms || isLoading
                    ? 'bg-primary/50 text-primary-foreground cursor-not-allowed opacity-50' 
                    : 'bg-primary text-primary-foreground hover:bg-primary/90'
                }`}
                whileHover={formData.agreeToTerms && !isLoading ? { scale: 1.02, y: -2 } : {}}
                whileTap={formData.agreeToTerms && !isLoading ? { scale: 0.98 } : {}}
                transition={{ duration: 0.2 }}
              >
                {isLoading ? (
                  <>
                    <motion.div
                      className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full"
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    />
                    <span>Creating Account...</span>
                  </>
                ) : (
                  <>
                    <span>Create Account</span>
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
                Already have an account?{" "}
                <Link to="/login" className="text-primary hover:text-primary/80 transition-colors font-medium">
                  Sign in
                </Link>
              </p>
            </motion.div>
          </motion.div>
        </motion.div>
        
        {/* Benefits */}
        <motion.div 
          className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-4 text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1 }}
        >
          {[
            { icon: Check, text: "Free 30-day trial" },
            { icon: Check, text: "No setup fees" },
            { icon: Check, text: "Cancel anytime" }
          ].map((benefit, index) => (
            <motion.div
              key={index}
              className="flex items-center justify-center space-x-2 text-sm text-muted-foreground p-3 rounded-xl bg-card/30 backdrop-blur-sm border border-border/30"
              whileHover={{ scale: 1.05, y: -2 }}
              transition={{ duration: 0.2 }}
            >
              <benefit.icon className="h-4 w-4 text-green-500" />
              <span>{benefit.text}</span>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </motion.div>
  )
}