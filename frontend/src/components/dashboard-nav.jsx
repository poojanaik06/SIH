"use client"

import { Sprout, BarChart3, Satellite, LogOut, User, Bell, X, Check, AlertTriangle, Info, Droplets, Sun } from "lucide-react"
import { useState, useEffect } from "react"
import { Link, useLocation, useNavigate } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"

export function DashboardNav() {
  const [activeTab, setActiveTab] = useState("overview")
  const [user, setUser] = useState(null)
  const [isNotificationsPanelOpen, setIsNotificationsPanelOpen] = useState(false)
  const [isProfilePanelOpen, setIsProfilePanelOpen] = useState(false)
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'success',
      title: 'Crop Analysis Complete',
      message: 'Your field #A001 analysis has been completed successfully.',
      time: '2 minutes ago',
      read: false,
      icon: Check
    },
    {
      id: 2,
      type: 'warning',
      title: 'Weather Alert',
      message: 'Heavy rainfall expected in your area tomorrow. Consider protective measures.',
      time: '1 hour ago',
      read: false,
      icon: Droplets
    },
    {
      id: 3,
      type: 'info',
      title: 'Yield Prediction Ready',
      message: 'New yield predictions are available for Field B002. Check your dashboard.',
      time: '3 hours ago',
      read: true,
      icon: BarChart3
    },
    {
      id: 4,
      type: 'alert',
      title: 'Soil Moisture Low',
      message: 'Field C003 shows low soil moisture levels. Irrigation recommended.',
      time: '5 hours ago',
      read: true,
      icon: AlertTriangle
    },
    {
      id: 5,
      type: 'info',
      title: 'System Update',
      message: 'New features have been added to your dashboard. Explore the enhanced analytics.',
      time: '1 day ago',
      read: true,
      icon: Info
    }
  ])
  const location = useLocation()
  const navigate = useNavigate()
  
  useEffect(() => {
    // Check if user is authenticated
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    }
    
    // Set active tab based on current location
    if (location.pathname === '/dashboard') {
      setActiveTab('overview')
    } else if (location.pathname === '/predictions') {
      setActiveTab('predictions')
    } else if (location.pathname.startsWith('/dashboard/fields')) {
      setActiveTab('fields')
    }
  }, [location])
  
  const handleLogout = () => {
    localStorage.removeItem('user')
    navigate('/')
  }

  const navItems = [
    { id: "overview", label: "Overview", icon: BarChart3, href: "/dashboard" },
    { id: "fields", label: "Field Management", icon: Satellite, href: "/dashboard/fields" },
    { id: "predictions", label: "Yield Predictions", icon: Sprout, href: "/predictions" },
  ]

  return (
    <nav className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Sprout className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold text-foreground">CropAI</span>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <Link
                key={item.id}
                to={item.href}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md transition-colors ${
                  activeTab === item.id ? "text-primary bg-primary/10" : "text-muted-foreground hover:text-primary"
                }`}
                onClick={() => setActiveTab(item.id)}
              >
                <item.icon className="h-4 w-4" />
                <span>{item.label}</span>
              </Link>
            ))}
          </div>

          <div className="flex items-center space-x-4">
            {user && (
              <span className="text-sm text-muted-foreground hidden md:block">
                Welcome, {user.firstName || user.email}
              </span>
            )}
            <button 
              onClick={() => setIsNotificationsPanelOpen(!isNotificationsPanelOpen)}
              className={`p-2 hover:bg-accent hover:text-accent-foreground rounded-md transition-colors relative ${
                isNotificationsPanelOpen ? 'bg-accent text-accent-foreground' : ''
              }`}
            >
              <Bell className="h-4 w-4" />
              {notifications.some(n => !n.read) && (
                <span className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full animate-pulse" />
              )}
            </button>
            <button 
              onClick={() => setIsProfilePanelOpen(!isProfilePanelOpen)}
              className={`p-2 hover:bg-accent hover:text-accent-foreground rounded-md transition-colors ${
                isProfilePanelOpen ? 'bg-accent text-accent-foreground' : ''
              }`}
            >
              <User className="h-4 w-4" />
            </button>
            <button 
              onClick={handleLogout}
              className="p-2 hover:bg-accent hover:text-accent-foreground rounded-md transition-colors"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
      
      {/* Notifications Side Panel */}
      {isNotificationsPanelOpen && (
        <>
          {/* Backdrop */}
          <div
            onClick={() => setIsNotificationsPanelOpen(false)}
            style={{
              position: 'fixed',
              inset: '0',
              backgroundColor: 'rgba(0, 0, 0, 0.2)',
              backdropFilter: 'blur(4px)',
              zIndex: '9998'
            }}
          />
          
          {/* Notifications Panel */}
          <div style={{
            position: 'fixed',
            right: '0',
            top: '0',
            height: '100vh',
            width: '384px',
            backgroundColor: 'white',
            borderLeft: '1px solid #e5e7eb',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
            zIndex: '9999',
            overflow: 'hidden'
          }}>
            <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
              {/* Header */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '24px',
                borderBottom: '1px solid #e5e7eb'
              }}>
                <div>
                  <h2 style={{ fontSize: '18px', fontWeight: '600', color: '#111827' }}>Notifications</h2>
                  <p style={{ fontSize: '14px', color: '#6b7280' }}>
                    {notifications.filter(n => !n.read).length} unread notifications
                  </p>
                </div>
                <button
                  onClick={() => setIsNotificationsPanelOpen(false)}
                  style={{
                    padding: '8px',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: 'transparent',
                    cursor: 'pointer',
                    transition: 'background-color 0.2s'
                  }}
                  onMouseEnter={(e) => e.target.style.backgroundColor = '#f3f4f6'}
                  onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
                >
                  <X style={{ width: '16px', height: '16px' }} />
                </button>
              </div>
              
              {/* Actions */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '16px',
                backgroundColor: '#f9fafb'
              }}>
                <button
                  onClick={() => {
                    setNotifications(notifications.map(n => ({ ...n, read: true })))
                  }}
                  style={{
                    fontSize: '14px',
                    color: '#2563eb',
                    fontWeight: '500',
                    border: 'none',
                    backgroundColor: 'transparent',
                    cursor: 'pointer',
                    transition: 'color 0.2s'
                  }}
                  onMouseEnter={(e) => e.target.style.color = '#1d4ed8'}
                  onMouseLeave={(e) => e.target.style.color = '#2563eb'}
                >
                  Mark all as read
                </button>
                <button
                  onClick={() => setNotifications([])}
                  style={{
                    fontSize: '14px',
                    color: '#6b7280',
                    border: 'none',
                    backgroundColor: 'transparent',
                    cursor: 'pointer',
                    transition: 'color 0.2s'
                  }}
                  onMouseEnter={(e) => e.target.style.color = '#111827'}
                  onMouseLeave={(e) => e.target.style.color = '#6b7280'}
                >
                  Clear all
                </button>
              </div>
              
              {/* Notifications List */}
              <div style={{ flex: '1', overflowY: 'auto' }}>
                {notifications.length === 0 ? (
                  <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100%',
                    textAlign: 'center',
                    padding: '24px'
                  }}>
                    <Bell style={{ width: '48px', height: '48px', color: '#9ca3af', marginBottom: '16px' }} />
                    <p style={{ color: '#6b7280' }}>No notifications yet</p>
                    <p style={{ fontSize: '14px', color: '#9ca3af', marginTop: '4px' }}>
                      You'll see updates about your crops here
                    </p>
                  </div>
                ) : (
                  <div style={{ padding: '8px' }}>
                    {notifications.map((notification) => {
                      const IconComponent = notification.icon
                      const getTypeStyles = (type) => {
                        switch (type) {
                          case 'success':
                            return { color: '#059669', backgroundColor: '#dcfce7' }
                          case 'warning':
                            return { color: '#d97706', backgroundColor: '#fef3c7' }
                          case 'alert':
                            return { color: '#dc2626', backgroundColor: '#fee2e2' }
                          case 'info':
                          default:
                            return { color: '#2563eb', backgroundColor: '#dbeafe' }
                        }
                      }
                      
                      const typeStyles = getTypeStyles(notification.type)
                      
                      return (
                        <div
                          key={notification.id}
                          onClick={() => {
                            setNotifications(notifications.map(n => 
                              n.id === notification.id ? { ...n, read: true } : n
                            ))
                          }}
                          style={{
                            padding: '16px',
                            marginBottom: '4px',
                            borderRadius: '8px',
                            border: '1px solid',
                            borderColor: !notification.read ? '#bfdbfe' : '#e5e7eb',
                            backgroundColor: !notification.read ? '#eff6ff' : 'white',
                            cursor: 'pointer',
                            transition: 'all 0.2s',
                            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
                          }}
                          onMouseEnter={(e) => {
                            e.target.style.backgroundColor = !notification.read ? '#dbeafe' : '#f9fafb'
                            e.target.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)'
                          }}
                          onMouseLeave={(e) => {
                            e.target.style.backgroundColor = !notification.read ? '#eff6ff' : 'white'
                            e.target.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)'
                          }}
                        >
                          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                            <div style={{
                              padding: '8px',
                              borderRadius: '50%',
                              ...typeStyles
                            }}>
                              <IconComponent style={{ width: '16px', height: '16px' }} />
                            </div>
                            <div style={{ flex: '1', minWidth: '0' }}>
                              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                <h3 style={{
                                  fontSize: '14px',
                                  fontWeight: '500',
                                  color: !notification.read ? '#111827' : '#6b7280',
                                  overflow: 'hidden',
                                  textOverflow: 'ellipsis',
                                  whiteSpace: 'nowrap'
                                }}>
                                  {notification.title}
                                </h3>
                                {!notification.read && (
                                  <div style={{
                                    width: '8px',
                                    height: '8px',
                                    backgroundColor: '#2563eb',
                                    borderRadius: '50%',
                                    marginLeft: '8px',
                                    flexShrink: '0'
                                  }} />
                                )}
                              </div>
                              <p style={{
                                fontSize: '12px',
                                marginTop: '4px',
                                color: !notification.read ? '#374151' : '#9ca3af'
                              }}>
                                {notification.message}
                              </p>
                              <p style={{
                                fontSize: '12px',
                                color: '#9ca3af',
                                marginTop: '8px'
                              }}>
                                {notification.time}
                              </p>
                            </div>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
      )}
      
      {/* Profile Side Panel */}
      {isProfilePanelOpen && (
        <>
          {/* Backdrop */}
          <div
            onClick={() => setIsProfilePanelOpen(false)}
            style={{
              position: 'fixed',
              inset: '0',
              backgroundColor: 'rgba(0, 0, 0, 0.2)',
              backdropFilter: 'blur(4px)',
              zIndex: '9998'
            }}
          />
          
          {/* Profile Panel */}
          <div style={{
            position: 'fixed',
            right: '0',
            top: '0',
            height: '100vh',
            width: '384px',
            backgroundColor: 'white',
            borderLeft: '1px solid #e5e7eb',
            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
            zIndex: '9999',
            overflow: 'hidden'
          }}>
            <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
              {/* Header */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '24px',
                borderBottom: '1px solid #e5e7eb'
              }}>
                <div>
                  <h2 style={{ fontSize: '18px', fontWeight: '600', color: '#111827' }}>Profile</h2>
                  <p style={{ fontSize: '14px', color: '#6b7280' }}>
                    Manage your account settings
                  </p>
                </div>
                <button
                  onClick={() => setIsProfilePanelOpen(false)}
                  style={{
                    padding: '8px',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: 'transparent',
                    cursor: 'pointer',
                    transition: 'background-color 0.2s'
                  }}
                  onMouseEnter={(e) => e.target.style.backgroundColor = '#f3f4f6'}
                  onMouseLeave={(e) => e.target.style.backgroundColor = 'transparent'}
                >
                  <X style={{ width: '16px', height: '16px' }} />
                </button>
              </div>
              
              {/* Profile Content */}
              <div style={{ flex: '1', overflowY: 'auto', padding: '24px' }}>
                {user ? (
                  <div>
                    {/* Profile Avatar Section */}
                    <div style={{
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      textAlign: 'center',
                      marginBottom: '32px'
                    }}>
                      <div style={{
                        width: '80px',
                        height: '80px',
                        backgroundColor: '#3b82f6',
                        borderRadius: '50%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginBottom: '16px'
                      }}>
                        <User style={{ width: '40px', height: '40px', color: 'white' }} />
                      </div>
                      <h3 style={{ fontSize: '20px', fontWeight: '600', color: '#111827', marginBottom: '4px' }}>
                        {user.firstName && user.lastName ? `${user.firstName} ${user.lastName}` : 
                         user.firstName ? user.firstName : 
                         user.name ? user.name : 
                         user.email ? user.email.split('@')[0] : 'User'}
                      </h3>
                      <p style={{ fontSize: '14px', color: '#6b7280' }}>
                        Farmer
                      </p>
                    </div>
                    
                    {/* Profile Information */}
                    <div style={{ space: '16px' }}>
                      {/* Email */}
                      <div style={{ marginBottom: '20px' }}>
                        <label style={{ fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                          Email Address
                        </label>
                        <div style={{
                          marginTop: '8px',
                          padding: '12px 16px',
                          backgroundColor: '#f9fafb',
                          border: '1px solid #e5e7eb',
                          borderRadius: '8px',
                          fontSize: '14px',
                          color: '#111827'
                        }}>
                          {user.email}
                        </div>
                      </div>
                      
                      {/* Name */}
                      {(user.firstName || user.name) && (
                        <div style={{ marginBottom: '20px' }}>
                          <label style={{ fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                            Full Name
                          </label>
                          <div style={{
                            marginTop: '8px',
                            padding: '12px 16px',
                            backgroundColor: '#f9fafb',
                            border: '1px solid #e5e7eb',
                            borderRadius: '8px',
                            fontSize: '14px',
                            color: '#111827'
                          }}>
                            {user.firstName && user.lastName ? `${user.firstName} ${user.lastName}` : 
                             user.firstName ? user.firstName : 
                             user.name ? user.name : 'Not provided'}
                          </div>
                        </div>
                      )}
                      
                      {/* Farm Size */}
                      {user.farmSize && (
                        <div style={{ marginBottom: '20px' }}>
                          <label style={{ fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                            Farm Size
                          </label>
                          <div style={{
                            marginTop: '8px',
                            padding: '12px 16px',
                            backgroundColor: '#f9fafb',
                            border: '1px solid #e5e7eb',
                            borderRadius: '8px',
                            fontSize: '14px',
                            color: '#111827'
                          }}>
                            {user.farmSize} acres
                          </div>
                        </div>
                      )}
                      
                      {/* Additional Info */}
                      {user.phone && (
                        <div style={{ marginBottom: '20px' }}>
                          <label style={{ fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                            Phone Number
                          </label>
                          <div style={{
                            marginTop: '8px',
                            padding: '12px 16px',
                            backgroundColor: '#f9fafb',
                            border: '1px solid #e5e7eb',
                            borderRadius: '8px',
                            fontSize: '14px',
                            color: '#111827'
                          }}>
                            {user.phone}
                          </div>
                        </div>
                      )}
                      
                      {/* Location */}
                      {user.location && (
                        <div style={{ marginBottom: '20px' }}>
                          <label style={{ fontSize: '12px', fontWeight: '500', color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                            Location
                          </label>
                          <div style={{
                            marginTop: '8px',
                            padding: '12px 16px',
                            backgroundColor: '#f9fafb',
                            border: '1px solid #e5e7eb',
                            borderRadius: '8px',
                            fontSize: '14px',
                            color: '#111827'
                          }}>
                            {user.location}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100%',
                    textAlign: 'center'
                  }}>
                    <User style={{ width: '48px', height: '48px', color: '#9ca3af', marginBottom: '16px' }} />
                    <p style={{ color: '#6b7280' }}>No user data available</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </nav>
  )
}