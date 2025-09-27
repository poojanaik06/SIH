import { Suspense } from "react"
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom"
import { Navbar } from "./components/navbar"
import { DashboardNav } from "./components/dashboard-nav"
import { AdminNav } from "./components/admin-nav"
import { Hero } from "./components/hero"
import { Features } from "./components/feature"
import { Footer } from "./components/footer"
import AboutPage from "./pages/about"
import ContactPage from "./pages/contact"
import LoginPage from "./pages/login"
import LoginDebug from "./pages/login-debug"
import APIDiagnostics from "./pages/api-diagnostics"
import SignupPage from "./pages/signup"
import DashboardPage from "./pages/dashboard"
import AdminPage from "./pages/admin"
import PredictionsPage from "./pages/predictions"
import FieldManagementPage from "./pages/field-management"
import UserDataViewer from "./pages/admin/user-data-viewer"
import "./App.css"

// Loading component
function Loading() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="w-8 h-8 border-4 border-primary/30 border-t-primary rounded-full animate-spin mx-auto mb-4"></div>
        <p className="text-muted-foreground">Loading...</p>
      </div>
    </div>
  )
}

// Home component
function HomePage() {
  return (
    <>
      <Hero />
      <Features />
    </>
  )
}

// Navigation component that renders different navs based on route
function AppNavigation() {
  const location = useLocation()
  
  if (location.pathname.startsWith('/dashboard') || 
      location.pathname === '/predictions' ||
      location.pathname.startsWith('/dashboard/fields')) {
    return <DashboardNav />
  }
  
  if (location.pathname.startsWith('/admin')) {
    return <AdminNav />
  }
  
  return <Navbar />
}

// Footer component that only shows on public pages
function AppFooter() {
  const location = useLocation()
  
  // Don't show footer on dashboard, admin, or predictions pages
  if (location.pathname.startsWith('/dashboard') || 
      location.pathname.startsWith('/admin') || 
      location.pathname === '/predictions') {
    return null
  }
  
  return <Footer />
}

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Suspense fallback={<Loading />}>
          <AppNavigation />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/login-debug" element={<LoginDebug />} />
            <Route path="/api-diagnostics" element={<APIDiagnostics />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/dashboard/fields" element={<FieldManagementPage />} />
            <Route path="/admin" element={<AdminPage />} />
            <Route path="/admin/user-data" element={<UserDataViewer />} />
            <Route path="/predictions" element={<PredictionsPage />} />
          </Routes>
          <AppFooter />
        </Suspense>
      </div>
    </Router>
  )
}