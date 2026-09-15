import requests
import streamlit as st


st.set_page_config(
    page_title="AI Weather Assistant",
    page_icon="🌤️"
)


# Common Indian places
indian_places = {
    "bangalore": ("Bengaluru", "India", 12.9716, 77.5946),
    "bengaluru": ("Bengaluru", "India", 12.9716, 77.5946),
    "chennai": ("Chennai", "India", 13.0827, 80.2707),
    "mumbai": ("Mumbai", "India", 19.0760, 72.8777),
    "delhi": ("New Delhi", "India", 28.6139, 77.2090),
    "new delhi": ("New Delhi", "India", 28.6139, 77.2090),
    "hyderabad": ("Hyderabad", "India", 17.3850, 78.4867),
    "kochi": ("Kochi", "India", 9.9312, 76.2673),
    "kerala": ("Kerala", "India", 10.8505, 76.2711),
    "coimbatore": ("Coimbatore", "India", 11.0168, 76.9558),
    "madurai": ("Madurai", "India", 9.9252, 78.1198),
    "trichy": ("Tiruchirappalli", "India", 10.7905, 78.7047)
}


# Get weather
def get_weather(city):

    city = city.strip().lower()

    if city in indian_places:

        name, country, latitude, longitude = indian_places[city]

    else:

        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"

        geocode_params = {
            "name": city,
            "count": 10,
            "language": "en",
            "format": "json"
        }

        response = requests.get(
            geocode_url,
            params=geocode_params,
            timeout=10
        )

        data = response.json()

        if "results" not in data:
            return {
                "error": f"City '{city}' not found."
            }

        location = data["results"][0]

        name = location["name"]
        country = location.get("country", "")
        latitude = location["latitude"]
        longitude = location["longitude"]


    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=10
    )

    weather_data = weather_response.json()

    current = weather_data["current"]

    return {
        "city": name,
        "country": country,
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "precipitation": current["precipitation"],
        "wind_speed": current["wind_speed_10m"],
        "weather_code": current["weather_code"],
        "time": current["time"]
    }


# Weather condition
def get_condition(code):

    if code == 0:
        return "Clear Sky ☀️"

    elif code in [1, 2, 3]:
        return "Partly Cloudy ⛅"

    elif code in [45, 48]:
        return "Foggy 🌫️"

    elif code in [51, 53, 55, 56, 57]:
        return "Drizzle 🌦️"

    elif code in [61, 63, 65, 66, 67]:
        return "Rainy 🌧️"

    elif code in [80, 81, 82]:
        return "Rain Showers 🌦️"

    elif code in [95, 96, 99]:
        return "Thunderstorm ⛈️"

    return "Unknown"


# Title
st.title("🌤️ AI Weather Assistant")

st.write("Check the current weather of a city.")


# Input
city = st.text_input(
    "Enter City Name",
    placeholder="Example: Bangalore"
)


# Button
if st.button("Get Weather"):

    if city.strip() == "":
        st.warning("Please enter a city name.")

    else:

        weather = get_weather(city)

        if "error" in weather:

            st.error(weather["error"])

        else:

            condition = get_condition(
                weather["weather_code"]
            )

            # Weather result
            st.success(
                f"🌤️ Weather in {weather['city']}, {weather['country']}"
            )

            st.write(f"### {condition}")

            st.write(
                f"🌡️ Temperature: "
                f"{weather['temperature']} °C"
            )

            st.write(
                f"🌡️ Feels Like: "
                f"{weather['feels_like']} °C"
            )

            st.write(
                f"💧 Humidity: "
                f"{weather['humidity']} %"
            )

            st.write(
                f"💨 Wind Speed: "
                f"{weather['wind_speed']} km/h"
            )

            st.write(
                f"🌧️ Precipitation: "
                f"{weather['precipitation']} mm"
            )

            st.write(
                f"🕒 Time: "
                f"{weather['time']}"
            )