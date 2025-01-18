import requests

CARBON_INTERFACE_API_KEY = "your_carbon_interface_api_key"
OPENWEATHERMAP_API_KEY = "your_openweathermap_api_key"
EPA_API_KEY = "your_epa_api_key"

CARBON_INTERFACE_URL = "https://www.carboninterface.com/api/v1"
OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/weather"
EPA_URL = "https://api.epa.gov/air_quality"

headers = {
    "Authorization": f"Bearer {CARBON_INTERFACE_API_KEY}",
    "Content-Type": "application/json"
}

def get_electricity_emissions(country_code):
    try:
        response = requests.get(f"{CARBON_INTERFACE_URL}/emissions/electricity", headers=headers)
        response.raise_for_status()
        data = response.json()
        for item in data:
            if item["data"]["attributes"]["country"] == country_code.upper():
                return item["data"]["attributes"]["grams_per_kwh"] / 1000
        return None
    except requests.exceptions.RequestException:
        return None

def get_weather_data(city):
    try:
        response = requests.get(f"{OPENWEATHERMAP_URL}?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric")
        response.raise_for_status()
        data = response.json()
        return data['main']['temp']
    except requests.exceptions.RequestException:
        return None

def get_air_quality(city):
    try:
        response = requests.get(f"{EPA_URL}?city={city}&apiKey={EPA_API_KEY}")
        response.raise_for_status()
        data = response.json()
        return data['data']['aqi']
    except requests.exceptions.RequestException:
        return None

print("Welcome to the Carbon Footprint Calculator!")

city = input("Enter your city: ")
country_code = input("Enter your country code (e.g., US, UK, IN): ").upper()

temperature = get_weather_data(city)
if temperature is not None:
    print(f"The current temperature in {city} is {temperature}°C.")

air_quality = get_air_quality(city)
if air_quality is not None:
    print(f"The current air quality index (AQI) in {city} is {air_quality}.")

transportation = input("How do you primarily get around? (car/public transport/bike/walk): ").lower()
electricity_bill = float(input("What is your average monthly electricity bill in USD? "))
electricity_usage = electricity_bill * 1.2

heating = input("What type of heating do you use? (gas/electricity): ").lower()
if heating == "gas":
    heating_emissions = 1500
elif heating == "electricity":
    heating_emissions = 1000
else:
    heating_emissions = 0

recycling = input("Do you regularly recycle? (yes/no): ").lower()
if recycling == "yes":
    recycling_emissions = -500
else:
    recycling_emissions = 500

flights_per_year = int(input("How many flights do you take per year? (estimate for vacations or work): "))
flight_emissions = flights_per_year * 1500

emissions_factor = get_electricity_emissions(country_code)
if emissions_factor is None:
    emissions_factor = 0.5

electricity_emissions = electricity_usage * 12 * emissions_factor

if transportation == "car":
    car_usage = int(input("How many miles do you drive on average per week? "))
    transport_emissions = car_usage * 0.9
elif transportation == "public transport":
    transport_emissions = 1000
elif transportation in ["bike", "walk"]:
    transport_emissions = 0
else:
    transport_emissions = 2000

total_emissions = electricity_emissions + transport_emissions + heating_emissions + recycling_emissions + flight_emissions

print("\n--- Results ---")
print(f"Your estimated annual carbon footprint is: {total_emissions:.2f} kg of CO2.")
if total_emissions > 5000:
    print("Your carbon footprint is higher than average. Consider making small changes to reduce it!")
elif total_emissions > 3000:
    print("Your carbon footprint is around average. There’s still room for improvement!")
else:
    print("Great job! Your carbon footprint is lower than average. Keep it up!")

print("\nThank you for using the Carbon Footprint Calculator!")
