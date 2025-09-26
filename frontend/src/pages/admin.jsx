import { PlatformAnalytics } from "../components/platform-analytics"
import { UserManagement } from "../components/user-management"

export default function AdminPage() {
  return (
    <div className="min-h-screen bg-background">
      <main className="pt-20 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">Admin Dashboard</h1>
            <p className="text-muted-foreground">Platform overview and user management</p>
          </div>

          <div className="space-y-8">
            <PlatformAnalytics />
            <UserManagement />
          </div>
        </div>
      </main>
    </div>
  )
}