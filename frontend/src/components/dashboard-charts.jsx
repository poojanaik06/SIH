import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts'

const monthlyData = [
  { month: "Jan", yield: 85, revenue: 12000, expenses: 8000 },
  { month: "Feb", yield: 88, revenue: 13200, expenses: 8500 },
  { month: "Mar", yield: 92, revenue: 14800, expenses: 9000 },
  { month: "Apr", yield: 95, revenue: 16200, expenses: 9200 },
  { month: "May", yield: 98, revenue: 17800, expenses: 9500 },
  { month: "Jun", yield: 102, revenue: 19400, expenses: 9800 },
]

const cropComparison = [
  { crop: "Corn", thisYear: 95, lastYear: 88 },
  { crop: "Soybeans", thisYear: 82, lastYear: 79 },
  { crop: "Wheat", thisYear: 78, lastYear: 75 },
  { crop: "Cotton", thisYear: 91, lastYear: 85 },
]

export function DashboardCharts() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
        <div className="p-6 border-b border-gray-300">
          <h3 className="text-lg font-semibold text-gray-900">Monthly Performance</h3>
          <p className="text-sm text-gray-600">Yield and revenue trends over time</p>
        </div>
        <div className="p-6 bg-gray-100">
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis 
                dataKey="month" 
                className="text-xs" 
                tick={{ fontSize: 12 }}
                axisLine={false}
              />
              <YAxis 
                className="text-xs" 
                tick={{ fontSize: 12 }}
                axisLine={false}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  fontSize: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
                formatter={(value, name) => {
                  if (name === 'yield') return [`${value}%`, 'Yield']
                  if (name === 'revenue') return [`$${value.toLocaleString()}`, 'Revenue']
                  if (name === 'expenses') return [`$${value.toLocaleString()}`, 'Expenses']
                  return [value, name]
                }}
              />
              <Legend 
                wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}
                formatter={(value) => {
                  if (value === 'yield') return 'Yield (%)'
                  if (value === 'revenue') return 'Revenue ($)'
                  if (value === 'expenses') return 'Expenses ($)'
                  return value
                }}
              />
              <Line 
                type="monotone" 
                dataKey="yield" 
                stroke="hsl(142, 76%, 36%)" 
                strokeWidth={3}
                dot={{ fill: 'hsl(142, 76%, 36%)', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: 'hsl(142, 76%, 36%)', strokeWidth: 2 }}
              />
              <Line 
                type="monotone" 
                dataKey="revenue" 
                stroke="hsl(221, 83%, 53%)" 
                strokeWidth={2}
                dot={{ fill: 'hsl(221, 83%, 53%)', strokeWidth: 2, r: 3 }}
              />
              <Line 
                type="monotone" 
                dataKey="expenses" 
                stroke="hsl(0, 84%, 60%)" 
                strokeWidth={2}
                dot={{ fill: 'hsl(0, 84%, 60%)', strokeWidth: 2, r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
        <div className="p-6 border-b border-gray-300">
          <h3 className="text-lg font-semibold text-gray-900">Crop Comparison</h3>
          <p className="text-sm text-gray-600">This year vs last year performance</p>
        </div>
        <div className="p-6 bg-gray-100">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={cropComparison} barCategoryGap={20}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis 
                dataKey="crop" 
                className="text-xs" 
                tick={{ fontSize: 12 }}
                axisLine={false}
              />
              <YAxis 
                className="text-xs" 
                tick={{ fontSize: 12 }}
                axisLine={false}
                label={{ value: 'Yield (%)', angle: -90, position: 'insideLeft', style: { fontSize: '12px' } }}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  fontSize: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
                formatter={(value, name) => {
                  if (name === 'thisYear') return [`${value}%`, 'This Year']
                  if (name === 'lastYear') return [`${value}%`, 'Last Year']
                  return [value, name]
                }}
              />
              <Legend 
                wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}
                formatter={(value) => {
                  if (value === 'thisYear') return 'This Year (%)'
                  if (value === 'lastYear') return 'Last Year (%)'
                  return value
                }}
              />
              <Bar 
                dataKey="thisYear" 
                fill="hsl(142, 76%, 36%)" 
                radius={[4, 4, 0, 0]}
                name="thisYear"
              />
              <Bar 
                dataKey="lastYear" 
                fill="hsl(142, 76%, 60%)" 
                radius={[4, 4, 0, 0]}
                name="lastYear"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}