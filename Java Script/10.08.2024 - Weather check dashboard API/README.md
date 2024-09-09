# Weather Fetcher

This JavaScript project retrieves current weather data for a specified city and country code using the OpenWeatherMap API. The application also stores and displays the user's recent location searches.

## Features

- **Fetch Weather Data**: Retrieves weather information, including temperature and description, for a specific city and country using the OpenWeatherMap API.
- **Geocoding**: Converts city names and country codes into geographical coordinates (latitude and longitude) using the OpenWeatherMap Geocoding API.
- **Recent Locations**: Stores recent location searches in the browser's local storage and displays them on the page.

## How It Works

1. **User Input**: The user enters a city name and selects a country code.
2. **Geocoding API**: The script fetches geographical coordinates for the specified city and country.
3. **Weather API**: Using the coordinates, the script retrieves the current weather data.
4. **Display Data**: The weather data, such as temperature and description, is displayed.
5. **Recent Locations**: The search data, including date, time, city, country, and temperature, is stored in local storage and displayed as a list.

## Usage

1. Clone the repository to your local machine.
2. Open `index.html` in your browser.
3. Enter a city name and select a country code.
4. Click the "Show Weather" button or press Enter to display the weather data.

## Setup

1. Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api).
2. Replace the placeholder API key in the script (`const apiKey = 'your_api_key_here';`) with your actual API key.

## Dependencies

- **OpenWeatherMap API**: Used for fetching weather and geocoding data.