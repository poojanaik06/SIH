// Application constants and configuration
export const APP_CONFIG = {
  name: "CropAI",
  description: "AI-powered crop yield optimization platform",
  version: "1.0.0",
  supportEmail: "support@cropai.com",
  maxFileSize: 10 * 1024 * 1024, // 10MB
  allowedImageTypes: ["image/jpeg", "image/png", "image/webp"],
}

export const CROP_TYPES = [
  { value: "wheat", label: "Wheat" },
  { value: "corn", label: "Corn" },
  { value: "rice", label: "Rice" },
  { value: "soybean", label: "Soybean" },
  { value: "cotton", label: "Cotton" },
  { value: "barley", label: "Barley" },
  { value: "oats", label: "Oats" },
]

export const SOIL_TYPES = [
  { value: "clay", label: "Clay" },
  { value: "sandy", label: "Sandy" },
  { value: "loamy", label: "Loamy" },
  { value: "silty", label: "Silty" },
  { value: "peaty", label: "Peaty" },
  { value: "chalky", label: "Chalky" },
]

export const FARM_SIZES = [
  { value: "small", label: "Small (1-100 acres)" },
  { value: "medium", label: "Medium (100-500 acres)" },
  { value: "large", label: "Large (500+ acres)" },
]

export const REGIONS = [
  { value: "midwest", label: "Midwest" },
  { value: "great-plains", label: "Great Plains" },
  { value: "southeast", label: "Southeast" },
  { value: "west-coast", label: "West Coast" },
  { value: "northeast", label: "Northeast" },
  { value: "southwest", label: "Southwest" },
]