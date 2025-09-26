// Type definitions converted to JSDoc comments for better development experience

/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} name
 * @property {string} email
 * @property {string} [farmName]
 * @property {string} location
 * @property {"small" | "medium" | "large"} farmSize
 * @property {string} joinDate
 * @property {"basic" | "premium" | "enterprise"} subscription
 * @property {"active" | "inactive" | "suspended"} status
 */

/**
 * @typedef {Object} Field
 * @property {string} id
 * @property {string} name
 * @property {string} crop
 * @property {number} area - in acres
 * @property {Object} location
 * @property {number} location.latitude
 * @property {number} location.longitude
 * @property {string} soilType
 * @property {string} plantingDate
 * @property {string} expectedHarvestDate
 * @property {number} health - percentage
 * @property {number} soilMoisture - percentage
 * @property {string} growthStage
 * @property {Alert[]} alerts
 */

/**
 * @typedef {Object} Alert
 * @property {string} id
 * @property {"warning" | "info" | "success" | "error"} type
 * @property {string} title
 * @property {string} description
 * @property {string} timestamp
 * @property {"low" | "medium" | "high"} priority
 * @property {boolean} resolved
 */

/**
 * @typedef {Object} WeatherData
 * @property {Object} current
 * @property {number} current.temperature
 * @property {number} current.humidity
 * @property {number} current.windSpeed
 * @property {number} current.precipitation
 * @property {string} current.condition
 * @property {Array} forecast
 */

/**
 * @typedef {Object} YieldPrediction
 * @property {string} fieldId
 * @property {string} crop
 * @property {number} predictedYield
 * @property {number} confidence
 * @property {Array} factors
 * @property {string[]} recommendations
 * @property {string} timestamp
 */

/**
 * @typedef {Object} AIInsight
 * @property {string} id
 * @property {"recommendation" | "alert" | "prediction" | "success"} type
 * @property {"high" | "medium" | "low" | "info"} priority
 * @property {string} title
 * @property {string} description
 * @property {string} impact
 * @property {number} confidence
 * @property {string} action
 * @property {string} timestamp
 */

// Export empty object to make this a valid module
export {}