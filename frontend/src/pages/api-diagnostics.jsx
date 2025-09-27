import { useState } from "react"
import { ApiService } from "../lib/api"

export default function APIDiagnostics() {
  const [results, setResults] = useState({})
  const [loading, setLoading] = useState(false)

  const runDiagnostics = async () => {
    setLoading(true)
    const diagnostics = {}
    
    try {
      // Test 1: Backend Health Check
      console.log("🔍 Testing backend health...")
      try {
        const response = await fetch("http://127.0.0.1:8000/predict/health")
        if (response.ok) {
          const data = await response.json()
          diagnostics.health = { success: true, data }
        } else {
          diagnostics.health = { success: false, error: `HTTP ${response.status}` }
        }
      } catch (error) {
        diagnostics.health = { success: false, error: error.message }
      }

      // Test 2: Login API Test
      console.log("🔍 Testing login API...")
      try {
        const loginResult = await ApiService.login("test@example.com", "testpass123")
        diagnostics.login = loginResult
      } catch (error) {
        diagnostics.login = { success: false, error: error.message }
      }

      // Test 3: User Info API Test (if login successful)
      if (diagnostics.login?.success) {
        console.log("🔍 Testing user info API...")
        try {
          const userResult = await ApiService.getCurrentUser()
          diagnostics.userInfo = userResult
        } catch (error) {
          diagnostics.userInfo = { success: false, error: error.message }
        }
      }

      // Test 4: Direct Auth Token Test
      console.log("🔍 Testing direct auth endpoint...")
      try {
        const response = await fetch("http://127.0.0.1:8000/auth/token", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({
            username: "test@example.com",
            password: "testpass123"
          })
        })
        
        if (response.ok) {
          const data = await response.json()
          diagnostics.directAuth = { success: true, data }
        } else {
          const errorData = await response.json()
          diagnostics.directAuth = { 
            success: false, 
            error: errorData.detail || `HTTP ${response.status}`,
            status: response.status
          }
        }
      } catch (error) {
        diagnostics.directAuth = { success: false, error: error.message }
      }

      // Test 5: Prediction API Test
      console.log("🔍 Testing prediction API...")
      try {
        const predictionResult = await ApiService.predictYieldFarmerFriendly({
          location: "Punjab, India",
          crop_name: "Wheat"
        })
        diagnostics.prediction = predictionResult
      } catch (error) {
        diagnostics.prediction = { success: false, error: error.message }
      }

      setResults(diagnostics)
    } catch (error) {
      console.error("Diagnostics error:", error)
      setResults({ error: error.message })
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (result) => {
    if (!result) return "⚪"
    return result.success ? "✅" : "❌"
  }

  const getStatusColor = (result) => {
    if (!result) return "text-gray-500"
    return result.success ? "text-green-600" : "text-red-600"
  }

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">🔧 API Diagnostics Tool</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <button
          onClick={runDiagnostics}
          disabled={loading}
          className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Running Diagnostics..." : "🚀 Run Full Diagnostics"}
        </button>
      </div>

      {Object.keys(results).length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-semibold mb-4">📊 Diagnostic Results</h2>
          
          {/* Health Check */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3 flex items-center">
              {getStatusIcon(results.health)} Backend Health Check
            </h3>
            <div className={`p-4 rounded ${getStatusColor(results.health)}`}>
              <pre className="text-sm overflow-auto">
                {JSON.stringify(results.health, null, 2)}
              </pre>
            </div>
          </div>

          {/* Login Test */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3 flex items-center">
              {getStatusIcon(results.login)} API Service Login Test
            </h3>
            <div className={`p-4 rounded ${getStatusColor(results.login)}`}>
              <pre className="text-sm overflow-auto">
                {JSON.stringify(results.login, null, 2)}
              </pre>
            </div>
          </div>

          {/* Direct Auth Test */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3 flex items-center">
              {getStatusIcon(results.directAuth)} Direct Auth Endpoint Test
            </h3>
            <div className={`p-4 rounded ${getStatusColor(results.directAuth)}`}>
              <pre className="text-sm overflow-auto">
                {JSON.stringify(results.directAuth, null, 2)}
              </pre>
            </div>
          </div>

          {/* User Info Test */}
          {results.userInfo && (
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-3 flex items-center">
                {getStatusIcon(results.userInfo)} User Info API Test
              </h3>
              <div className={`p-4 rounded ${getStatusColor(results.userInfo)}`}>
                <pre className="text-sm overflow-auto">
                  {JSON.stringify(results.userInfo, null, 2)}
                </pre>
              </div>
            </div>
          )}

          {/* Prediction Test */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3 flex items-center">
              {getStatusIcon(results.prediction)} Prediction API Test
            </h3>
            <div className={`p-4 rounded ${getStatusColor(results.prediction)}`}>
              <pre className="text-sm overflow-auto">
                {JSON.stringify(results.prediction, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      )}

      <div className="mt-8 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
        <h3 className="font-bold mb-2">💡 Troubleshooting Steps:</h3>
        <ul className="list-disc list-inside text-sm space-y-1">
          <li>Check if backend server is running on <code>http://127.0.0.1:8000</code></li>
          <li>Verify database is accessible and contains user data</li>
          <li>Check browser console for additional error details</li>
          <li>Ensure CORS is properly configured for frontend requests</li>
          <li>Verify environment variables are properly set</li>
        </ul>
      </div>
    </div>
  )
}