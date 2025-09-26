"use client"

const userGrowthData = [
  { month: "Jan", users: 1200, revenue: 48000 },
  { month: "Feb", users: 1450, revenue: 58000 },
  { month: "Mar", users: 1680, revenue: 67200 },
  { month: "Apr", users: 1920, revenue: 76800 },
  { month: "May", users: 2150, revenue: 86000 },
  { month: "Jun", users: 2400, revenue: 96000 },
]

const cropDistribution = [
  { name: "Corn", value: 35, color: "oklch(0.65 0.2 142)" },
  { name: "Soybeans", value: 28, color: "oklch(0.7 0.15 200)" },
  { name: "Wheat", value: 18, color: "oklch(0.6 0.18 280)" },
  { name: "Cotton", value: 12, color: "oklch(0.75 0.12 60)" },
  { name: "Other", value: 7, color: "oklch(0.68 0.16 320)" },
]

const regionData = [
  { region: "Midwest", farms: 850, yield: 92 },
  { region: "Great Plains", farms: 620, yield: 88 },
  { region: "Southeast", farms: 480, yield: 85 },
  { region: "West Coast", farms: 320, yield: 90 },
  { region: "Northeast", farms: 180, yield: 87 },
]

export function PlatformAnalytics() {
  return (
    <div className="space-y-8">
      {/* User Growth Chart */}
      <div className="border-border bg-card border rounded-lg">
        <div className="p-6">
          <h3 className="text-foreground text-lg font-semibold">User Growth & Revenue</h3>
          <p className="text-muted-foreground text-sm">
            Platform adoption and revenue trends over the last 6 months
          </p>
        </div>
        <div className="p-6 pt-0">
          <div className="w-full h-80 flex items-center justify-center bg-accent/30 rounded-lg">
            <p className="text-muted-foreground">Chart Component Placeholder - User Growth</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Crop Distribution */}
        <div className="border-border bg-card border rounded-lg">
          <div className="p-6">
            <h3 className="text-foreground text-lg font-semibold">Crop Distribution</h3>
            <p className="text-muted-foreground text-sm">
              Breakdown of crops monitored on the platform
            </p>
          </div>
          <div className="p-6 pt-0">
            <div className="w-full h-80 flex items-center justify-center bg-accent/30 rounded-lg">
              <div className="text-center">
                <p className="text-muted-foreground mb-4">Crop Distribution Chart</p>
                <div className="space-y-2 text-sm">
                  {cropDistribution.map((crop, index) => (
                    <div key={index} className="flex justify-between">
                      <span>{crop.name}</span>
                      <span>{crop.value}%</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Regional Performance */}
        <div className="border-border bg-card border rounded-lg">
          <div className="p-6">
            <h3 className="text-foreground text-lg font-semibold">Regional Performance</h3>
            <p className="text-muted-foreground text-sm">Farm count and average yield by region</p>
          </div>
          <div className="p-6 pt-0">
            <div className="w-full h-80 flex items-center justify-center bg-accent/30 rounded-lg">
              <div className="text-center">
                <p className="text-muted-foreground mb-4">Regional Performance Chart</p>
                <div className="space-y-2 text-sm">
                  {regionData.map((region, index) => (
                    <div key={index} className="flex justify-between">
                      <span>{region.region}</span>
                      <span>{region.farms} farms</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}