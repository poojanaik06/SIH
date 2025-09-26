"use client"

import { Cloud, Sun, CloudRain, Wind, Droplets } from "lucide-react"

const weatherData = {
  current: {
    temp: 72,
    condition: "Partly Cloudy",
    humidity: 65,
    windSpeed: 8,
    precipitation: 0,
  },
  forecast: [
    { day: "Today", high: 75, low: 62, condition: "sunny", precipitation: 0 },
    { day: "Tomorrow", high: 78, low: 65, condition: "cloudy", precipitation: 10 },
    { day: "Wed", high: 73, low: 58, condition: "rainy", precipitation: 80 },
    { day: "Thu", high: 69, low: 55, condition: "rainy", precipitation: 90 },
    { day: "Fri", high: 71, low: 57, condition: "cloudy", precipitation: 20 },
  ],
}

const getWeatherIcon = (condition) => {
  switch (condition) {
    case "sunny":
      return <Sun className="h-6 w-6 text-yellow-500" />
    case "cloudy":
      return <Cloud className="h-6 w-6 text-gray-400" />
    case "rainy":
      return <CloudRain className="h-6 w-6 text-blue-400" />
    default:
      return <Sun className="h-6 w-6 text-yellow-500" />
  }
}

export function WeatherWidget() {
  return (
    <div className="bg-gray-200 border border-gray-300 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
      <div className="p-6">
        <h3 className="text-foreground text-lg font-semibold">Weather Conditions</h3>
        <p className="text-muted-foreground text-sm">Current conditions and 5-day forecast</p>
      </div>
      <div className="p-6 pt-0">
        {/* Current Weather */}
        <div className="mb-6 p-4 bg-accent/50 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="text-3xl font-bold text-foreground">{weatherData.current.temp}°F</div>
              <div className="text-muted-foreground">{weatherData.current.condition}</div>
            </div>
            <Cloud className="h-12 w-12 text-primary" />
          </div>

          <div className="grid grid-cols-3 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <Droplets className="h-4 w-4 text-blue-400" />
              <span className="text-muted-foreground">{weatherData.current.humidity}%</span>
            </div>
            <div className="flex items-center space-x-2">
              <Wind className="h-4 w-4 text-gray-400" />
              <span className="text-muted-foreground">{weatherData.current.windSpeed} mph</span>
            </div>
            <div className="flex items-center space-x-2">
              <CloudRain className="h-4 w-4 text-blue-400" />
              <span className="text-muted-foreground">{weatherData.current.precipitation}%</span>
            </div>
          </div>
        </div>

        {/* 5-Day Forecast */}
        <div className="space-y-3">
          <h4 className="font-semibold text-foreground">5-Day Forecast</h4>
          {weatherData.forecast.map((day, index) => (
            <div key={index} className="flex items-center justify-between py-2">
              <div className="flex items-center space-x-3">
                {getWeatherIcon(day.condition)}
                <span className="text-foreground font-medium">{day.day}</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-muted-foreground text-sm">{day.precipitation}%</span>
                <span className="text-foreground">
                  {day.high}°/{day.low}°
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}