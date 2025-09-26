import { Sprout, Users, BarChart3, Settings, Database, Bell, User, LogOut } from "lucide-react"
import { useState } from "react"

export function AdminNav() {
  const [activeTab, setActiveTab] = useState("overview")

  const navItems = [
    { id: "overview", label: "Overview", icon: BarChart3, href: "/admin" },
    { id: "users", label: "User Management", icon: Users, href: "/admin/users" },
    { id: "analytics", label: "Analytics", icon: BarChart3, href: "/admin/analytics" },
    { id: "data", label: "Data Management", icon: Database, href: "/admin/data" },
    { id: "settings", label: "Settings", icon: Settings, href: "/admin/settings" },
  ]

  return (
    <nav className="fixed top-0 w-full z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <a href="/" className="flex items-center space-x-2">
              <Sprout className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold text-foreground">CropAI Admin</span>
            </a>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => (
              <a
                key={item.id}
                href={item.href}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md transition-colors ${
                  activeTab === item.id ? "text-primary bg-primary/10" : "text-muted-foreground hover:text-primary"
                }`}
                onClick={() => setActiveTab(item.id)}
              >
                <item.icon className="h-4 w-4" />
                <span>{item.label}</span>
              </a>
            ))}
          </div>

          <div className="flex items-center space-x-4">
            <button className="p-2 hover:bg-accent hover:text-accent-foreground rounded-md transition-colors">
              <Bell className="h-4 w-4" />
            </button>
            <button className="p-2 hover:bg-accent hover:text-accent-foreground rounded-md transition-colors">
              <User className="h-4 w-4" />
            </button>
            <button className="p-2 hover:bg-accent hover:text-accent-foreground rounded-md transition-colors">
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}