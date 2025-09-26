import sqlite3
import sys
sys.path.append('app')

def populate_sample_data():
    """Populate the database with sample data for testing"""
    try:
        conn = sqlite3.connect('sih_crop_yield.db')
        cursor = conn.cursor()
        
        print("Adding sample data...")
        
        # Insert sample areas
        areas_data = [
            (1, 'India'),
            (2, 'China'),
            (3, 'USA'),
            (4, 'Brazil')
        ]
        
        cursor.executemany("INSERT OR IGNORE INTO areas (area_id, area_name) VALUES (?, ?)", areas_data)
        
        # Insert sample crops
        crops_data = [
            (1, 'Wheat'),
            (2, 'Rice'),
            (3, 'Maize'),
            (4, 'Soybean')
        ]
        
        cursor.executemany("INSERT OR IGNORE INTO crops (crop_id, crop_name) VALUES (?, ?)", crops_data)
        
        # Insert sample yield data
        yield_data = [
            (1, 1, 1, 2023, 45.5, 'hg/ha'),
            (2, 1, 2, 2023, 38.2, 'hg/ha'),
            (3, 2, 1, 2023, 52.1, 'hg/ha'),
            (4, 2, 3, 2023, 48.7, 'hg/ha'),
            (5, 1, 1, 2024, 47.2, 'hg/ha')
        ]
        
        cursor.executemany("INSERT OR IGNORE INTO yield_data (yield_id, area_id, crop_id, year, yield_value, unit) VALUES (?, ?, ?, ?, ?, ?)", yield_data)
        
        # Insert sample rainfall data
        rainfall_data = [
            (1, 1, 2023, 850.5),
            (2, 2, 2023, 720.3),
            (3, 1, 2024, 920.1)
        ]
        
        cursor.executemany("INSERT OR IGNORE INTO rainfall_data (rainfall_id, area_id, year, rainfall_mm) VALUES (?, ?, ?, ?)", rainfall_data)
        
        # Insert sample temperature data
        temperature_data = [
            (1, 1, 2023, 24.5),
            (2, 2, 2023, 22.8),
            (3, 1, 2024, 25.2)
        ]
        
        cursor.executemany("INSERT OR IGNORE INTO temperature_data (temp_id, area_id, year, avg_temp) VALUES (?, ?, ?, ?)", temperature_data)
        
        # Insert sample pesticide data
        pesticide_data = [
            (1, 1, 2023, 125.5),
            (2, 2, 2023, 98.3),
            (3, 1, 2024, 132.1)
        ]
        
        cursor.executemany("INSERT OR IGNORE INTO pesticide_data (pesticide_id, area_id, year, pesticide_tonnes) VALUES (?, ?, ?, ?)", pesticide_data)
        
        conn.commit()
        
        print("✅ Sample data added successfully!")
        
        # Test the combined view
        print("\n📊 Testing combined_dataset view:")
        cursor.execute("SELECT * FROM combined_dataset ORDER BY area_name, crop_name, year;")
        results = cursor.fetchall()
        
        if results:
            print("View results:")
            for row in results:
                print(f"  Area: {row[0]}, Crop: {row[1]}, Year: {row[2]}, Yield: {row[3]}, Rainfall: {row[5]}, Temp: {row[6]}, Pesticides: {row[7]}")
        else:
            print("No results from view")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    populate_sample_data()