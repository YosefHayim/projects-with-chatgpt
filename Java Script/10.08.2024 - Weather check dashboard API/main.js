// This script fetches weather data for a specified city and country code from the OpenWeatherMap API.
// It uses the Geocoding API to convert the city and country code into geographical coordinates (latitude and longitude),
// and then it uses these coordinates to fetch the current weather data. The script also stores the user's recent
// location searches in the browser's local storage and displays them.

const apiKey = 'faf110a59fa592f3bb08d8544ea30081'; 
// API key to authenticate requests to the OpenWeatherMap API.

let recentLocations = JSON.parse(localStorage.getItem('recentLocations')) || []; 
// Retrieve the list of recent locations from local storage if it exists, or initialize an empty array.

document.getElementById('showWeather').addEventListener('click', showWeather); 
// Add an event listener to the "Show Weather" button that triggers the showWeather function when clicked.

document.addEventListener('keydown', function(event) { 
    // Add an event listener to the entire document to detect when the Enter key is pressed.
    if (event.key === 'Enter') {
        showWeather(); 
        // Trigger the showWeather function if the Enter key is pressed.
    }
});

function showWeather() { 
    // Main function that handles the process of showing the weather for a specific city.
    const city = document.getElementById('cityInput').value.trim(); 
    // Get the city name entered by the user and remove any extra spaces.
    const countryCode = document.getElementById('countrySelect').value.trim(); 
    // Get the country code selected by the user and remove any extra spaces.
    const limit = 1; 
    // Limit the geocoding results to just one location.

    // Check if city or countryCode is missing
    if (!city || !countryCode) {
        alert('Error: You must provide both a city and a country code.');
        return; 
        // If either the city or country code is missing, show an alert and stop further execution.
    }

    const geoApiUrl = `http://api.openweathermap.org/geo/1.0/direct?q=${city},${countryCode}&limit=${limit}&appid=${apiKey}`;
    // Construct the URL for the Geocoding API request using the city, country code, and API key.

    // Function to get the latitude and longitude for a city
    function getLatLon() {
        return fetch(geoApiUrl)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    const lat = data[0].lat;
                    const lon = data[0].lon;
                    return { lat, lon }; 
                    // If the API returns data, extract the latitude and longitude and return them.
                } else {
                    throw new Error('Incorrect city or country.');
                    // If no data is returned, throw an error.
                }
            })
            .catch(error => {
                alert(error.message);
                return null; 
                // If an error occurs, alert the user and return null.
            });
    }

    // Function to get the weather data based on latitude and longitude
    function getWeather(lat, lon) {
        const weatherApiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`;
        // Construct the URL for the Weather API request using the latitude, longitude, API key, and specifying metric units.

        return fetch(weatherApiUrl)
            .then(response => response.json())
            .then(weatherData => {
                const temperature = weatherData.main.temp;
                const weatherDescription = weatherData.weather[0].description;

                // Determine the emoji based on the temperature
                let emoji = '';
                if (temperature < 0) {
                    emoji = '❄️';
                } else if (temperature < 15) {
                    emoji = '🌬️';
                } else if (temperature < 25) {
                    emoji = '☁️';
                } else if (temperature < 35) {
                    emoji = '🌤️';
                } else {
                    emoji = '🔥';
                }

                // Display the weather information
                document.getElementById('weatherResult').innerHTML = `
                    <h3>Weather in ${city}, ${countryCode}</h3>
                    <p>Temperature: ${temperature}°C ${emoji}</p>
                    <p>Description: ${weatherDescription}</p>
                `;

                const now = new Date();
                const date = now.toLocaleDateString();
                const time = now.toLocaleTimeString();
                const location = {
                    date,
                    time,
                    countryCode,
                    city,
                    temperature: `${temperature}°C ${emoji}`
                };

                recentLocations.push(location);
                localStorage.setItem('recentLocations', JSON.stringify(recentLocations)); 
                // Store updated recent locations in local storage.
                updateRecentLocations(); 
                // Update the UI with the new recent location.
            })
            .catch(error => console.error('Error fetching weather data:', error)); 
            // Log any errors that occur while fetching the weather data.
    }

    // Function to update the recent locations list in the UI
    function updateRecentLocations() {
        const recentLocationsList = document.getElementById('recentLocations');
        recentLocationsList.innerHTML = ''; 
        // Clear the current list.
        recentLocations.slice().reverse().forEach(location => { 
            // Reverse the order to show the most recent location first.
            const li = document.createElement('li');
            li.textContent = `${location.date} - ${location.time} - ${location.countryCode} - ${location.city} - ${location.temperature}`;
            recentLocationsList.appendChild(li); 
            // Create a new list item for each location and add it to the list.
        });
    }

    // Fetch latitude and longitude, then get weather
    getLatLon().then(coords => { 
        // Call the function to get the latitude and longitude.
        if (coords) { 
            // If coordinates were successfully retrieved...
            const { lat, lon } = coords; 
            // Destructure the latitude and longitude from the coords object.
            getWeather(lat, lon); 
            // Call the function to get the weather data for these coordinates.
        }
    });
}

// Update the list with any previously stored locations on page load
updateRecentLocations(); 
// When the page loads, update the list of recent locations from local storage.
