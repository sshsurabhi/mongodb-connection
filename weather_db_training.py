import os
import requests
from datetime import datetime
from pymongo import MongoClient

# Load API key from environment variable
KEY = os.getenv("weather")
CITY = "COURBEVOIE"

# Make the API call
r = requests.get(
    url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(
        CITY, KEY
    )
)
data = r.json()

# Print the API response for debugging
print(data)

# Check if the expected keys are present
if "weather" in data and "main" in data:
    clean_data = {i: data[i] for i in ["weather", "main"]}
    clean_data["weather"] = clean_data["weather"][0]

    current = datetime.now().strftime("%H:%M:%S")
    clean_data["time"] = current
    clean_data["city"] = CITY  # Ensure the variable is correctly named

    # Connect to MongoDB
    client = MongoClient(host="localhost", port=27017, username="datascientest", password="dst123")
    sample = client["sample"]

    # Check if the collection exists, if not create it
    if "weather" not in sample.list_collection_names():
        col = sample.create_collection(name="weather")
    else:
        col = sample["weather"]

    col.insert_one(clean_data)

else:
    print("Error: Expected keys not found in the response.")
    print("Response data:", data)