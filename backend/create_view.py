import sqlite3

def create_combined_dataset_view():
    """Create the combined_dataset view in the database"""
    try:
        # Connect to database
        conn = sqlite3.connect('sih_crop_yield.db')
        cursor = conn.cursor()
        
        # Drop view if it exists
        cursor.execute("DROP VIEW IF EXISTS combined_dataset;")
        
        # Create the view with corrected SQL
        create_view_sql = """
        CREATE VIEW combined_dataset AS
        SELECT 
            a.area_name,
            c.crop_name,
            y.year,
            y.yield_value,
            y.unit,
            r.rainfall_mm,
            t.avg_temp,
            p.pesticide_tonnes
        FROM yield_data y
        LEFT JOIN areas a ON y.area_id = a.area_id
        LEFT JOIN crops c ON y.crop_id = c.crop_id
        LEFT JOIN rainfall_data r ON y.area_id = r.area_id AND y.year = r.year
        LEFT JOIN temperature_data t ON y.area_id = t.area_id AND y.year = t.year
        LEFT JOIN pesticide_data p ON y.area_id = p.area_id AND y.year = p.year;
        """
        
        cursor.execute(create_view_sql)
        conn.commit()
        
        print("✅ View 'combined_dataset' created successfully!")
        
        # Test the view
        cursor.execute("SELECT * FROM combined_dataset LIMIT 5;")
        results = cursor.fetchall()
        
        if results:
            print("✅ View is working! Sample data:")
            for row in results:
                print(f"  {row}")
        else:
            print("⚠️ View created but no data found (tables might be empty)")
        
        # Get column info
        cursor.execute("PRAGMA table_info(combined_dataset)")
        columns = cursor.fetchall()
        print("\n📊 View columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Creating combined_dataset view...")
    create_combined_dataset_view()