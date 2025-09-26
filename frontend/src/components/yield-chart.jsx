"use client"

import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts'

const yieldData = [
  { month: "Jan", predicted: 85, actual: 82, historical: 78 },
  { month: "Feb", predicted: 88, actual: 86, historical: 80 },
  { month: "Mar", predicted: 92, actual: 90, historical: 85 },
  { month: "Apr", predicted: 95, actual: 94, historical: 88 },
  { month: "May", predicted: 98, actual: 96, historical: 90 },
  { month: "Jun", predicted: 102, actual: 100, historical: 92 },
  { month: "Jul", predicted: 105, actual: null, historical: 95 },
  { month: "Aug", predicted: 108, actual: null, historical: 98 },
  { month: "Sep", predicted: 110, actual: null, historical: 100 },
  { month: "Oct", predicted: 112, actual: null, historical: 102 },
  { month: "Nov", predicted: 115, actual: null, historical: 105 },
  { month: "Dec", predicted: 118, actual: null, historical: 108 },
]

export function YieldChart() {
  return (
    <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
      <div className="p-6">
        <h3 className="text-foreground text-lg font-semibold">Yield Predictions vs Actual</h3>
        <p className="text-muted-foreground text-sm">
          Bushels per acre - Current season vs historical average
        </p>
      </div>
      <div className="p-6 pt-0">
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={yieldData}>
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
              label={{ value: 'Bushels/Acre', angle: -90, position: 'insideLeft', style: { fontSize: '12px' } }}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '8px',
                fontSize: '12px'
              }}
              formatter={(value, name) => {
                if (value === null) return ['N/A', name]
                return [`${value} bu/acre`, name]
              }}
            />
            <Legend 
              wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}
            />
            <Line 
              type="monotone" 
              dataKey="predicted" 
              stroke="hsl(142, 76%, 36%)" 
              strokeWidth={3}
              strokeDasharray="5 5"
              dot={{ fill: 'hsl(142, 76%, 36%)', strokeWidth: 2, r: 4 }}
              name="Predicted"
            />
            <Line 
              type="monotone" 
              dataKey="actual" 
              stroke="hsl(221, 83%, 53%)" 
              strokeWidth={3}
              dot={{ fill: 'hsl(221, 83%, 53%)', strokeWidth: 2, r: 4 }}
              connectNulls={false}
              name="Actual"
            />
            <Line 
              type="monotone" 
              dataKey="historical" 
              stroke="hsl(0, 0%, 60%)" 
              strokeWidth={2}
              dot={{ fill: 'hsl(0, 0%, 60%)', strokeWidth: 2, r: 3 }}
              name="Historical Avg"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}