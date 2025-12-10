import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { PriceHistory } from '../api/types'

interface PriceChartProps {
  data: PriceHistory[]
}

export default function PriceChart({ data }: PriceChartProps) {
  const chartData = data.map(item => {
    const dateObj = new Date(item.scraped_at + 'Z') // Add Z to convert from UTC
    return {
      date: dateObj.toLocaleDateString(),
      dateTime: dateObj.toLocaleString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        second: '2-digit',
        hour12: true 
      }),
      price: item.price,
      timestamp: dateObj.getTime(),
    }
  })

  if (chartData.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <p className="text-gray-500">No price history available</p>
      </div>
    )
  }

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="date" 
            stroke="#6b7280"
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            stroke="#6b7280"
            tick={{ fontSize: 12 }}
            domain={[0, 'auto']}
            tickFormatter={(value) => `$${value.toFixed(2)}`}
          />
          <Tooltip 
            formatter={(value: number) => [`$${value.toFixed(2)}`, 'Price']}
            labelFormatter={(label) => {
              // Find the full dateTime for this label
              const dataPoint = chartData.find(d => d.date === label)
              return dataPoint?.dateTime || label
            }}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '0.375rem',
            }}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="price" 
            stroke="#0ea5e9" 
            strokeWidth={2}
            dot={{ fill: '#0ea5e9', r: 4 }}
            activeDot={{ r: 6 }}
            name="Price"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}


