"use client"

import { Search, Filter, UserPlus, MoreHorizontal, MapPin } from "lucide-react"
import { useState } from "react"

const users = [
  {
    id: 1,
    name: "John Smith",
    email: "john.smith@farm.com",
    location: "Iowa, USA",
    farmSize: "Large (500+ acres)",
    joinDate: "2024-01-15",
    status: "active",
    subscription: "premium",
    lastActive: "2 hours ago",
  },
  {
    id: 2,
    name: "Maria Garcia",
    email: "maria.garcia@agri.com",
    location: "California, USA",
    farmSize: "Medium (100-500 acres)",
    joinDate: "2024-02-20",
    status: "active",
    subscription: "basic",
    lastActive: "1 day ago",
  },
  {
    id: 3,
    name: "David Chen",
    email: "david.chen@crops.com",
    location: "Nebraska, USA",
    farmSize: "Large (500+ acres)",
    joinDate: "2024-01-08",
    status: "inactive",
    subscription: "premium",
    lastActive: "1 week ago",
  },
  {
    id: 4,
    name: "Sarah Johnson",
    email: "sarah.j@farming.com",
    location: "Kansas, USA",
    farmSize: "Small (1-100 acres)",
    joinDate: "2024-03-10",
    status: "active",
    subscription: "basic",
    lastActive: "5 minutes ago",
  },
  {
    id: 5,
    name: "Robert Wilson",
    email: "r.wilson@agriculture.com",
    location: "Illinois, USA",
    farmSize: "Medium (100-500 acres)",
    joinDate: "2024-02-05",
    status: "active",
    subscription: "premium",
    lastActive: "3 hours ago",
  },
]

const getStatusColor = (status) => {
  switch (status) {
    case "active":
      return "bg-green-500/20 text-green-400 border-green-500/30"
    case "inactive":
      return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    case "suspended":
      return "bg-red-500/20 text-red-400 border-red-500/30"
    default:
      return "bg-gray-500/20 text-gray-400 border-gray-500/30"
  }
}

const getSubscriptionColor = (subscription) => {
  switch (subscription) {
    case "premium":
      return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
    case "basic":
      return "bg-blue-500/20 text-blue-400 border-blue-500/30"
    case "trial":
      return "bg-purple-500/20 text-purple-400 border-purple-500/30"
    default:
      return "bg-gray-500/20 text-gray-400 border-gray-500/30"
  }
}

export function UserManagement() {
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  const filteredUsers = users.filter((user) => {
    const matchesSearch =
      user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "all" || user.status === statusFilter
    return matchesSearch && matchesStatus
  })

  return (
    <div className="border-border bg-card border rounded-lg">
      <div className="p-6">
        <h3 className="text-foreground flex items-center text-lg font-semibold">
          <UserPlus className="h-5 w-5 mr-2 text-primary" />
          User Management
        </h3>
        <p className="text-muted-foreground text-sm">
          Manage farmers and agricultural organizations using the platform
        </p>
      </div>
      <div className="p-6 pt-0">
        {/* Filters */}
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <input
              placeholder="Search users..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm pl-10"
            />
          </div>
          <select 
            value={statusFilter} 
            onChange={(e) => setStatusFilter(e.target.value)}
            className="flex h-10 w-full md:w-48 rounded-md border border-input bg-background px-3 py-2 text-sm"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="suspended">Suspended</option>
          </select>
          <button className="flex h-10 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90">
            <UserPlus className="h-4 w-4 mr-2" />
            Add User
          </button>
        </div>

        {/* Users Table */}
        <div className="rounded-md border border-border overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="h-12 px-4 text-left align-middle font-medium text-foreground">User</th>
                <th className="h-12 px-4 text-left align-middle font-medium text-foreground">Location</th>
                <th className="h-12 px-4 text-left align-middle font-medium text-foreground">Farm Size</th>
                <th className="h-12 px-4 text-left align-middle font-medium text-foreground">Status</th>
                <th className="h-12 px-4 text-left align-middle font-medium text-foreground">Subscription</th>
                <th className="h-12 px-4 text-left align-middle font-medium text-foreground">Last Active</th>
                <th className="h-12 px-4 text-left align-middle font-medium text-foreground">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map((user) => (
                <tr key={user.id} className="border-b border-border">
                  <td className="p-4 align-middle">
                    <div>
                      <div className="font-medium text-foreground">{user.name}</div>
                      <div className="text-sm text-muted-foreground">{user.email}</div>
                    </div>
                  </td>
                  <td className="p-4 align-middle">
                    <div className="flex items-center text-muted-foreground">
                      <MapPin className="h-4 w-4 mr-1" />
                      {user.location}
                    </div>
                  </td>
                  <td className="p-4 align-middle text-muted-foreground">{user.farmSize}</td>
                  <td className="p-4 align-middle">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(user.status)}`}>
                      {user.status}
                    </span>
                  </td>
                  <td className="p-4 align-middle">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${getSubscriptionColor(user.subscription)}`}>
                      {user.subscription}
                    </span>
                  </td>
                  <td className="p-4 align-middle text-muted-foreground">{user.lastActive}</td>
                  <td className="p-4 align-middle">
                    <button className="p-2 hover:bg-accent hover:text-accent-foreground rounded-md transition-colors">
                      <MoreHorizontal className="h-4 w-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
          <div className="p-4 bg-accent/30 rounded-lg">
            <div className="text-2xl font-bold text-foreground">{users.length}</div>
            <div className="text-sm text-muted-foreground">Total Users</div>
          </div>
          <div className="p-4 bg-accent/30 rounded-lg">
            <div className="text-2xl font-bold text-foreground">
              {users.filter((u) => u.status === "active").length}
            </div>
            <div className="text-sm text-muted-foreground">Active Users</div>
          </div>
          <div className="p-4 bg-accent/30 rounded-lg">
            <div className="text-2xl font-bold text-foreground">
              {users.filter((u) => u.subscription === "premium").length}
            </div>
            <div className="text-sm text-muted-foreground">Premium Users</div>
          </div>
          <div className="p-4 bg-accent/30 rounded-lg">
            <div className="text-2xl font-bold text-foreground">
              {users.filter((u) => new Date(u.joinDate) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)).length}
            </div>
            <div className="text-sm text-muted-foreground">New This Month</div>
          </div>
        </div>
      </div>
    </div>
  )
}