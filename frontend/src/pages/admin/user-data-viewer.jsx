import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Users, Download, Database, RefreshCw, Eye, Calendar, Mail, MapPin } from "lucide-react"

export default function UserDataViewer() {
  const [localStorageUsers, setLocalStorageUsers] = useState([])
  const [currentUser, setCurrentUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadUserData()
  }, [])

  const loadUserData = () => {
    setLoading(true)
    try {
      // Get registered users from localStorage
      const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]')
      setLocalStorageUsers(registeredUsers)
      
      // Get current user session
      const currentUserSession = JSON.parse(localStorage.getItem('user') || 'null')
      setCurrentUser(currentUserSession)
      
    } catch (error) {
      console.error('Error loading user data:', error)
    } finally {
      setLoading(false)
    }
  }

  const exportUserData = () => {
    const userData = {
      registeredUsers: localStorageUsers,
      currentUser: currentUser,
      exportedAt: new Date().toISOString()
    }
    
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(userData, null, 2))
    const downloadAnchorNode = document.createElement('a')
    downloadAnchorNode.setAttribute("href", dataStr)
    downloadAnchorNode.setAttribute("download", "user_data_export.json")
    document.body.appendChild(downloadAnchorNode)
    downloadAnchorNode.click()
    downloadAnchorNode.remove()
  }

  const clearAllData = () => {
    if (confirm('Are you sure you want to clear all user data? This cannot be undone.')) {
      localStorage.removeItem('registeredUsers')
      localStorage.removeItem('user')
      localStorage.removeItem('auth_token')
      loadUserData()
      alert('All user data cleared!')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <motion.div
          className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
      </div>
    )
  }

  return (
    <motion.div 
      className="min-h-screen bg-gradient-to-br from-background to-primary/5 p-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div 
          className="text-center mb-8"
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <h1 className="text-4xl font-bold text-foreground mb-4 flex items-center justify-center gap-3">
            <Database className="h-10 w-10 text-primary" />
            User Data Viewer
          </h1>
          <p className="text-muted-foreground text-lg">
            View and manage user data stored in browser localStorage
          </p>
        </motion.div>

        {/* Stats Cards */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div className="bg-card/80 backdrop-blur-md border border-border/50 rounded-xl p-6 text-center">
            <Users className="h-8 w-8 text-blue-500 mx-auto mb-2" />
            <h3 className="text-2xl font-bold text-foreground">{localStorageUsers.length}</h3>
            <p className="text-muted-foreground">Registered Users</p>
          </div>
          
          <div className="bg-card/80 backdrop-blur-md border border-border/50 rounded-xl p-6 text-center">
            <Eye className="h-8 w-8 text-green-500 mx-auto mb-2" />
            <h3 className="text-2xl font-bold text-foreground">{currentUser ? 1 : 0}</h3>
            <p className="text-muted-foreground">Active Session</p>
          </div>
          
          <div className="bg-card/80 backdrop-blur-md border border-border/50 rounded-xl p-6 text-center">
            <Database className="h-8 w-8 text-purple-500 mx-auto mb-2" />
            <h3 className="text-2xl font-bold text-foreground">localStorage</h3>
            <p className="text-muted-foreground">Storage Type</p>
          </div>
        </motion.div>

        {/* Actions */}
        <motion.div 
          className="flex flex-wrap gap-4 mb-8 justify-center"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          <button
            onClick={loadUserData}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <RefreshCw className="h-4 w-4" />
            Refresh Data
          </button>
          
          <button
            onClick={exportUserData}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <Download className="h-4 w-4" />
            Export to JSON
          </button>
          
          <button
            onClick={clearAllData}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            <Database className="h-4 w-4" />
            Clear All Data
          </button>
        </motion.div>

        {/* Current User Session */}
        {currentUser && (
          <motion.div 
            className="bg-card/80 backdrop-blur-md border border-border/50 rounded-xl p-6 mb-8"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.8 }}
          >
            <h2 className="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
              <Eye className="h-5 w-5 text-green-500" />
              Current User Session
            </h2>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-green-600" />
                  <span className="font-medium">Email:</span> {currentUser.email}
                </div>
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-green-600" />
                  <span className="font-medium">Name:</span> {currentUser.firstName} {currentUser.lastName}
                </div>
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-green-600" />
                  <span className="font-medium">Farm Size:</span> {currentUser.farmSize}
                </div>
                <div className="flex items-center gap-2">
                  <Eye className="h-4 w-4 text-green-600" />
                  <span className="font-medium">Status:</span> {currentUser.isAuthenticated ? 'Authenticated' : 'Not Authenticated'}
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Registered Users Table */}
        <motion.div 
          className="bg-card/80 backdrop-blur-md border border-border/50 rounded-xl overflow-hidden"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 1 }}
        >
          <div className="p-6 border-b border-border/50">
            <h2 className="text-xl font-semibold text-foreground flex items-center gap-2">
              <Users className="h-5 w-5 text-blue-500" />
              All Registered Users ({localStorageUsers.length})
            </h2>
          </div>
          
          <div className="overflow-x-auto">
            {localStorageUsers.length > 0 ? (
              <table className="w-full">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      User Info
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Contact
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Farm Details
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                      Registration
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/50">
                  {localStorageUsers.map((user, index) => (
                    <motion.tr 
                      key={index}
                      className="hover:bg-muted/30 transition-colors"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.1 }}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                            <Users className="h-5 w-5 text-primary" />
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-medium text-foreground">
                              {user.firstName} {user.lastName}
                            </div>
                            <div className="text-sm text-muted-foreground">
                              User #{index + 1}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-foreground">{user.email}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-foreground">{user.farmSize || 'Not specified'}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {user.registeredAt ? new Date(user.registeredAt).toLocaleDateString() : 'Unknown'}
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="text-center py-12">
                <Users className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="text-lg font-medium text-foreground mb-2">No Users Found</h3>
                <p className="text-muted-foreground">
                  No users found in localStorage. Users will appear here after registration.
                </p>
              </div>
            )}
          </div>
        </motion.div>

        {/* Help Section */}
        <motion.div 
          className="mt-8 bg-blue-50 border border-blue-200 rounded-xl p-6"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 1.2 }}
        >
          <h3 className="text-lg font-semibold text-blue-800 mb-4">💡 Understanding Your Data Storage</h3>
          <div className="space-y-2 text-sm text-blue-700">
            <p><strong>localStorage:</strong> User data is stored in your browser's local storage</p>
            <p><strong>Location:</strong> Browser Developer Tools → Application → Local Storage → localhost:5173</p>
            <p><strong>Keys:</strong> 'registeredUsers' (all users), 'user' (current session)</p>
            <p><strong>Note:</strong> This data is only on your computer and will be lost if you clear browser data</p>
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}