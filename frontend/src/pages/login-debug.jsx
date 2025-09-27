import { useState } from "react"
import { ApiService } from "../lib/api"

export default function LoginDebug() {
  const [email, setEmail] = useState("test@example.com")
  const [password, setPassword] = useState("testpass123")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const testLogin = async () => {
    setLoading(true)
    setResult(null)
    
    console.log('Testing login with:', { email, password })
    
    try {
      const loginResult = await ApiService.login(email, password)
      console.log('Login result:', loginResult)
      
      if (loginResult.success) {
        // Test getting user info
        const userResult = await ApiService.getCurrentUser()
        console.log('User info result:', userResult)
        
        setResult({
          type: 'success',
          loginResult,
          userResult
        })
      } else {
        setResult({
          type: 'login_failed',
          error: loginResult.error
        })
      }
    } catch (error) {
      console.error('Login test error:', error)
      setResult({
        type: 'exception',
        error: error.message
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">🔍 Login Debug Tool</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
            placeholder="Enter email"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
            placeholder="Enter password"
          />
        </div>
        
        <button
          onClick={testLogin}
          disabled={loading}
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Testing...' : 'Test Login'}
        </button>
      </div>
      
      {result && (
        <div className="mt-6 p-4 rounded-lg border">
          <h3 className="font-bold mb-2">Test Result:</h3>
          <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
      
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="font-bold mb-2">📋 Available Test Accounts:</h3>
        <div className="space-y-2 text-sm">
          <div>📧 <strong>test@example.com</strong> / Password: <strong>testpass123</strong></div>
          <div>📧 <strong>abc@gmail.com</strong> / Password: <strong>(unknown - was registered via frontend)</strong></div>
          <div>📧 <strong>sahanamadival@gmail.com</strong> / Password: <strong>(unknown - was registered via frontend)</strong></div>
        </div>
      </div>
      
      <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
        <h3 className="font-bold mb-2">💡 Troubleshooting Tips:</h3>
        <ul className="list-disc list-inside text-sm space-y-1">
          <li>Check browser console for detailed error logs</li>
          <li>Verify backend server is running on port 8000</li>
          <li>Ensure correct email and password combination</li>
          <li>Try the test account: test@example.com / testpass123</li>
        </ul>
      </div>
    </div>
  )
}