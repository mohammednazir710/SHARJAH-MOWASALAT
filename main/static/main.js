
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

function showRoutes(locations) {
    // Ensure locations are valid
    console.log("All locations:", locations);

    const validLocations = locations.filter(location => {
        const [lat, lng] = location.split(',').map(Number);
        return !isNaN(lat) && !isNaN(lng) && lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180;
    });

    if (validLocations.length < 2) {
        console.error("Insufficient valid locations for routing.");
        return;
    }

    console.log("Valid locations:", validLocations);

    // Add markers for each location
    validLocations.forEach((location, index) => {
        const [lat, lng] = location.split(',').map(Number);
        L.marker([lat, lng]).addTo(map).bindPopup(`Stop ${index + 1}`);
    });

    // Add route using OSRM API
    const waypoints = validLocations.map(location => {
        const [lat, lng] = location.split(',').map(Number);
        return L.latLng(lat, lng);
    });

    L.Routing.control({
        waypoints,
        router: new L.Routing.osrmv1({
            serviceUrl: 'https://router.project-osrm.org/route/v1',
            profile: 'driving', // You can experiment with 'driving', 'foot', or 'cycling'
            useHints: false,
        }),
        routeWhileDragging: false, // Disable route dragging
        fitSelectedRoutes: true,  // Zoom map to fit the route
        showAlternatives: false, // Disable alternative routes
        createMarker: (i, wp) => {
            return L.marker(wp.latLng).bindPopup(`Stop ${i + 1}`);
        },
    }).addTo(map);
}


// Bus stops data (example locations)
// Fetch bus stop data from the server
fetch('/bus-stops/')
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
            L.marker([stop.latitude, stop.longitude], { icon: busIcon })
                .bindPopup(`<strong>${stop.name}</strong>`) // Display the bus stop name in a popup
                .addTo(map);
        });
    })
    .catch(error => console.error('Error fetching bus stops:', error));
