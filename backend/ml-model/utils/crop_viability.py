"""
Crop viability checker to validate if crops can be grown in specific regions
"""

# Define regions where agriculture is not viable
NON_AGRICULTURAL_REGIONS = {
    'antarctica', 'antarctic', 'south pole', 'north pole', 'arctic', 
    'sahara desert', 'gobi desert', 'death valley', 'greenland',
    'siberia', 'alaska tundra', 'himalayan peaks', 'mount everest',
    'ocean', 'pacific ocean', 'atlantic ocean', 'indian ocean'
}

# Define extreme climate conditions where agriculture is not viable
EXTREME_CLIMATE_LIMITS = {
    'temperature': {
        'min': -10,  # Below -10°C, most crops cannot survive
        'max': 50    # Above 50°C, most crops cannot survive
    },
    'rainfall': {
        'min': 100,  # Below 100mm annually, very difficult for most crops
        'max': 5000  # Above 5000mm annually, flooding issues
    }
}

# Define crop-specific growing conditions
CROP_REQUIREMENTS = {
    'wheat': {
        'min_temp': 3,
        'max_temp': 35,
        'min_rainfall': 300,
        'max_rainfall': 2000,  # Increased from 1500 to allow for Indian monsoon
        'unsuitable_regions': ['tropical rainforest', 'desert', 'arctic', 'antarctica']
    },
    'rice': {
        'min_temp': 16,
        'max_temp': 35,
        'min_rainfall': 1000,
        'max_rainfall': 4000,  # Rice can handle high rainfall
        'unsuitable_regions': ['desert', 'arctic', 'antarctica', 'arid']
    },
    'maize': {
        'min_temp': 8,
        'max_temp': 35,
        'min_rainfall': 400,
        'max_rainfall': 2500,  # Increased for tropical regions
        'unsuitable_regions': ['arctic', 'antarctica', 'extreme desert']
    },
    'corn': {  # Same as maize
        'min_temp': 8,
        'max_temp': 35,
        'min_rainfall': 400,
        'max_rainfall': 2500,
        'unsuitable_regions': ['arctic', 'antarctica', 'extreme desert']
    },
    'soybean': {
        'min_temp': 10,
        'max_temp': 35,
        'min_rainfall': 450,
        'max_rainfall': 2000,  # Increased for monsoon regions
        'unsuitable_regions': ['arctic', 'antarctica', 'desert']
    },
    'cotton': {
        'min_temp': 15,
        'max_temp': 40,
        'min_rainfall': 500,
        'max_rainfall': 1800,  # Increased for monsoon regions
        'unsuitable_regions': ['arctic', 'antarctica', 'temperate cold']
    },
    'barley': {
        'min_temp': 0,
        'max_temp': 32,
        'min_rainfall': 200,
        'max_rainfall': 1500,
        'unsuitable_regions': ['tropical', 'antarctica', 'extreme desert']
    },
    'sugarcane': {
        'min_temp': 18,
        'max_temp': 40,
        'min_rainfall': 1000,
        'max_rainfall': 3500,  # Sugarcane can handle very high rainfall
        'unsuitable_regions': ['temperate', 'arctic', 'antarctica', 'desert']
    },
    'potato': {
        'min_temp': 5,
        'max_temp': 25,
        'min_rainfall': 400,
        'max_rainfall': 2000,  # Increased for hill stations with high rainfall
        'unsuitable_regions': ['tropical hot', 'antarctica', 'extreme desert']
    }
}

def is_agricultural_region(location):
    """Check if the location is suitable for agriculture"""
    location_lower = location.lower()
    
    # Check for explicitly non-agricultural regions
    for region in NON_AGRICULTURAL_REGIONS:
        if region in location_lower:
            return False, f"Agriculture is not viable in {region}"
    
    return True, "Region suitable for agriculture"

def validate_crop_climate(crop, temperature, rainfall):
    """Validate if crop can grow in given climate conditions"""
    crop_lower = crop.lower()
    
    # Check if we have requirements for this crop
    if crop_lower not in CROP_REQUIREMENTS:
        # For unknown crops, use general limits
        if temperature < EXTREME_CLIMATE_LIMITS['temperature']['min']:
            return False, f"Temperature too low ({temperature}°C) for most crops"
        if temperature > EXTREME_CLIMATE_LIMITS['temperature']['max']:
            return False, f"Temperature too high ({temperature}°C) for most crops"
        if rainfall < EXTREME_CLIMATE_LIMITS['rainfall']['min']:
            return False, f"Insufficient rainfall ({rainfall}mm) for most crops"
        if rainfall > EXTREME_CLIMATE_LIMITS['rainfall']['max']:
            return False, f"Excessive rainfall ({rainfall}mm) may cause flooding"
        return True, "Climate conditions acceptable for general crops"
    
    # Check specific crop requirements
    requirements = CROP_REQUIREMENTS[crop_lower]
    
    if temperature < requirements['min_temp']:
        return False, f"{crop} requires minimum temperature of {requirements['min_temp']}°C (current: {temperature}°C)"
    
    if temperature > requirements['max_temp']:
        return False, f"{crop} cannot tolerate temperatures above {requirements['max_temp']}°C (current: {temperature}°C)"
    
    if rainfall < requirements['min_rainfall']:
        return False, f"{crop} requires minimum {requirements['min_rainfall']}mm rainfall (current: {rainfall}mm)"
    
    if rainfall > requirements['max_rainfall']:
        return False, f"{crop} cannot handle more than {requirements['max_rainfall']}mm rainfall (current: {rainfall}mm)"
    
    return True, f"Climate conditions suitable for {crop}"

def validate_crop_region(crop, location):
    """Validate if crop can be grown in specific region"""
    crop_lower = crop.lower()
    location_lower = location.lower()
    
    if crop_lower not in CROP_REQUIREMENTS:
        return True, "No specific regional restrictions for this crop"
    
    requirements = CROP_REQUIREMENTS[crop_lower]
    unsuitable_regions = requirements.get('unsuitable_regions', [])
    
    for unsuitable in unsuitable_regions:
        if unsuitable in location_lower:
            return False, f"{crop} is not suitable for {unsuitable} regions"
    
    return True, f"{crop} can potentially be grown in this region"

def comprehensive_viability_check(crop, location, temperature=None, rainfall=None):
    """Perform comprehensive viability check for crop and location"""
    
    # Check if location is agricultural
    is_agri, agri_msg = is_agricultural_region(location)
    if not is_agri:
        return {
            'viable': False,
            'reason': agri_msg,
            'recommendation': f"Consider locations with suitable agricultural conditions instead of {location}",
            'severity': 'critical'
        }
    
    # Check regional suitability for crop
    region_ok, region_msg = validate_crop_region(crop, location)
    if not region_ok:
        return {
            'viable': False,
            'reason': region_msg,
            'recommendation': f"Consider growing {crop} in more suitable regions or choose crops better adapted to {location}",
            'severity': 'high'
        }
    
    # Check climate suitability if temperature and rainfall are provided
    if temperature is not None and rainfall is not None:
        climate_ok, climate_msg = validate_crop_climate(crop, temperature, rainfall)
        if not climate_ok:
            return {
                'viable': False,
                'reason': climate_msg,
                'recommendation': f"Current climate conditions in {location} are not suitable for {crop}",
                'severity': 'high'
            }
    
    # If all checks pass
    return {
        'viable': True,
        'reason': f"{crop} appears suitable for cultivation in {location}",
        'recommendation': "Conditions look favorable for this crop",
        'severity': 'none'
    }

def get_alternative_crops(location, temperature=None, rainfall=None):
    """Suggest alternative crops suitable for the location"""
    suitable_crops = []
    
    for crop, requirements in CROP_REQUIREMENTS.items():
        # Check regional suitability
        region_ok, _ = validate_crop_region(crop, location)
        if not region_ok:
            continue
            
        # Check climate suitability if data available
        if temperature is not None and rainfall is not None:
            climate_ok, _ = validate_crop_climate(crop, temperature, rainfall)
            if not climate_ok:
                continue
                
        suitable_crops.append(crop)
    
    return suitable_crops