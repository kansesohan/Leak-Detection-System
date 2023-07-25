import numpy as np
import folium
import time
from folium import plugins
import geopandas as gpd

# Define pressure ranges for each sensor
pressure_ranges = [(49, 55), (25, 31), (9, 15), (9, 15), (42, 48), (43, 49)]

# Define sensor locations
sensor_locations = {
    "PS-1": [17.26386253, 74.15921483],
    "PS-2": [17.2604159, 74.16703653],
    "PS-3": [17.25856371, 74.16733243],
    "PS-4": [17.25861973, 74.17031081],
    "PS-5": [17.25771591, 74.17722277],
    "PS-6": [17.26003834, 74.18505906],
}

# Manually pass sensor readings for each sensor
sensor_readings = [
    [50, 52, 54, 50, 50, 50],  # Sensor PS-1 readings
    [30, 26, 26, 26, 26, 30],  # Sensor PS-2 readings 
    [10, 10, 10, 11, 12, 11],  # Sensor PS-3 readings
    [10, 10, 10, 11, 12, 16],  # Sensor PS-4 readings
    [43, 43, 43, 43, 43, 43],  # Sensor PS-5 readings
    [44, 44, 44, 44, 45, 45]   # Sensor PS-6 readings
]

# Create a map
m = folium.Map(location=[17.2617, 74.1674], zoom_start=13)

# Add the GeoJSON file as a GeoJSON layer to the map
geojson_file = r"E:\IoT_based_Pipeline_Leak_Detection\Malkapur_Nagarpanchayat\Pipeline.geojson"
folium.GeoJson(geojson_file, name="KML").add_to(m)

# Detect leaks for each sensor and plot on map
for i, readings in enumerate(sensor_readings):
    # Check if any reading is outside the pressure range for the sensor
    leak_flag = any(p < pressure_ranges[i][0] or p > pressure_ranges[i][1] for p in readings)

    if leak_flag:
        # Get the leaked pressure reading
        leaked_reading = max(readings)

        # Get the latitude and longitude of the sensor
        lat, lon = sensor_locations[f"PS-{i+1}"]

        # Create a custom icon with the leaked pressure reading as the symbol
        custom_icon = folium.Icon(color='red', icon_color='white', icon='fa-tachometer', prefix='fa')

        # Create the marker with the custom icon and the leaked pressure reading as a popup
        marker = folium.Marker(location=[lat, lon],
                              icon=custom_icon,
                              popup=f"Leaked Pressure: {leaked_reading}\nLat: {lat}, Lon: {lon}",
                              draggable=False)

        # Add the marker to the map and apply blinking effect
        marker.add_to(m)
        for _ in range(3):
            marker.add_to(m)
            m.get_root().add_child(marker)
            marker.add_to(m)

    else:
        lat, lon = sensor_locations[f"PS-{i+1}"]
        folium.Marker(location=[lat, lon],
                      popup=f"Normal Pressure\nLat: {lat}, Lon: {lon}",
                      draggable=False).add_to(m)

# Display the map
m
