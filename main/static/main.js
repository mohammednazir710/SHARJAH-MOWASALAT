
// Define the boundaries of UAE
var uaeBounds = L.latLngBounds(
    [22.6, 51.5], // Southwest corner of UAE
    [26.1, 56.5]  // Northeast corner of UAE
);

// Initialize the map with Sharjah as the center and a closer default zoom level
var map = L.map('map', {
    center: [25.3460, 55.4209], // Centered on Sharjah
    zoom: 15,
    maxBounds: uaeBounds,
    minZoom: 6
});

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 25,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

fetch('static/export.geojson')
  .then(response => response.json())
  .then(geoJsonData => {
    L.geoJSON(geoJsonData).addTo(map);
  })
  .catch(error => {
    console.log('Error loading GeoJSON data:', error);
  });

// Initialize variables
var locationMarker;
var userLocation = null; // Will store user's location if available


// Function to handle the current location
function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                userLocation = L.latLng(position.coords.latitude, position.coords.longitude);

                // Check if within UAE bounds
                if (uaeBounds.contains(userLocation)) {
                    map.setView(userLocation, 14); // Zoom to user's location
                    document.getElementById("currentLocationBtn").style.backgroundColor = "#fff";
                    document.getElementById("currentLocationBtn").setAttribute("data-tooltip", "You are inside UAE");
                } else {
                    map.setView(userLocation, 6); // Zoom to broader view
                    document.getElementById("currentLocationBtn").style.backgroundColor = "#dc3545";
                    document.getElementById("currentLocationBtn").setAttribute("data-tooltip", "You are outside of UAE");
                }

                // Add or move the location marker
                if (locationMarker) {
                    locationMarker.setLatLng(userLocation).bindPopup("Your Location").openPopup();
                } else {
                    locationMarker = L.marker(userLocation).addTo(map).bindPopup("Your Location").openPopup();
                }
            },
            function () {
                alert("Unable to retrieve your location. Reason: Your location is outside UAE");
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

// Function to pick a location on the map and fetch location name and distance
function onMapClick(e) {
    var pickedLatLng = e.latlng;

    // Move the marker immediately and show loading placeholder
    if (locationMarker) {
        locationMarker.setLatLng(pickedLatLng).bindPopup("Picked Location").openPopup();
    } else {
        locationMarker = L.marker(pickedLatLng).addTo(map).bindPopup("Picked Location").openPopup();
    }

    // Show the location info box and set placeholders
    document.getElementById("locationInfo").style.display = "block";
    document.getElementById("locationName").innerText = "Loading...";
    document.getElementById("distance").innerText = "???";

    // Fetch location name using reverse geocoding API
    fetch(`https://nominatim.openstreetmap.org/reverse?lat=${pickedLatLng.lat}&lon=${pickedLatLng.lng}&format=json`)
        .then(response => response.json())
        .then(data => {
            var locationName = data.display_name || "Unknown Location";

            // Calculate distance if user's location is available and within UAE
            var distanceText = "???";
            if (userLocation && uaeBounds.contains(userLocation)) {
                var distance = map.distance(userLocation, pickedLatLng) / 1000; // Distance in kilometers
                distanceText = distance.toFixed(1) + " KM";
            }

            // Update the UI with location name and distance
            document.getElementById("locationName").innerText = locationName;
            document.getElementById("distance").innerText = distanceText;

            // Center map on the picked location (if desired)
            map.setView(pickedLatLng, 14);
        })
        .catch(error => {
            console.error("Error fetching location name:", error);
            document.getElementById("locationName").innerText = "Unable to fetch location name.";
        });
}

// Add event listener for map clicks to pick a location
map.on('click', onMapClick);

// Event listener for the current location button
document.getElementById("currentLocationBtn").addEventListener("click", getCurrentLocation);

// Close button functionality to hide the location info box
document.getElementById("closeInfo").addEventListener("click", function () {
    document.getElementById("locationInfo").style.display = "none";
});


let routingControls = []; // To store multiple routing controls

// Function to show routes for multiple coordinates
function showRoutes(locations) {
    // Remove existing routes
    routingControls.forEach(control => map.removeControl(control));
    routingControls = [];

    // Clear route details container
    const routeDetailsContainer = document.getElementById('route-details');
    routeDetailsContainer.innerHTML = '';

    // Iterate through the locations and add routes between consecutive points
    for (let i = 0; i < locations.length - 1; i++) {
        const start = locations[i].split(',').map(Number);
        const end = locations[i + 1].split(',').map(Number);

        // Assign a random color for each route segment
        const routeColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;

        // Add routing control for the segment
        const routingControl = L.Routing.control({
            waypoints: [
                L.latLng(start[0], start[1]),
                L.latLng(end[0], end[1])
            ],
            routeWhileDragging: false,
            addWaypoints: false, // Disable waypoint dragging
            lineOptions: {
                styles: [{ color: routeColor, opacity: 0.8, weight: 4 }]
            },
            show: false // Hide default route instructions
        }).addTo(map);

        // Event listener for custom instructions
        routingControl.on('routesfound', (function (index) {
            return function (e) {
                const routes = e.routes[0]; // Take the first route for simplicity
        
                // Add a header for the route
                routeDetailsContainer.innerHTML += `<h4>Route ${index + 1}:</h4>`;
        
                // Add summary info
                const distance = (routes.summary.totalDistance / 1000).toFixed(2); // Convert to km
                const time = Math.round(routes.summary.totalTime / 60); // Convert to minutes
                routeDetailsContainer.innerHTML += `<p><strong>Distance:</strong> ${distance} km</p>`;
                routeDetailsContainer.innerHTML += `<p><strong>Time:</strong> ${time} mins</p>`;
        
                // Add detailed instructions (skip for Route 2)
                if (index !== 1) { // Skip detailed instructions for the second route
                    routeDetailsContainer.innerHTML += '<ol>'; // Ordered list for steps
                    routes.instructions.forEach(step => {
                        routeDetailsContainer.innerHTML += `<li>${step.text} (${(step.distance / 1000).toFixed(2)} km)</li>`;
                    });
                    routeDetailsContainer.innerHTML += '</ol>'; // Close ordered list
                }
                routeDetailsContainer.innerHTML += `<hr>`;

            };
        })(i));
        

        // Store the routing control
        routingControls.push(routingControl);
    }
}


// Bus stops data (example locations)
// Fetch bus stop data from the server
fetch('/api/bus-stops/')
    .then(response => response.json())
    .then(busStops => {
        // Define a custom bus icon
        var busIcon = L.icon({
            iconUrl: 'https://cdn-icons-png.flaticon.com/512/0/308.png', // Replace with your bus icon URL
            iconSize: [15, 15], // Size of the icon
            iconAnchor: [12, 12], // Anchor point of the icon (centered)
            popupAnchor: [0, -12] // Position of the popup relative to the icon
        });

        // Add markers for each bus stop
        busStops.forEach(function (stop) {
            L.marker([stop.lat, stop.lng], { icon: busIcon })
                .bindPopup(`<strong>${stop.name}</strong>`) // Display the bus stop name in a popup
                .addTo(map);
        });
    })
    .catch(error => console.error('Error fetching bus stops:', error));
