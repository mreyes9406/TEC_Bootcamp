function createMap(earthquakes) {

    // Create the tile layer that will be the background of our map
    var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
      maxZoom: 18,
      id: "mapbox.light",
      accessToken: API_KEY
    });
  
    // Create a baseMaps object to hold the lightmap layer
    var baseMaps = {
      "Light Map": lightmap
    };
  
    // Create an overlayMaps object to hold the earthquakes layer
    var overlayMaps = {
      "Earthquakes": earthquakes
    };
  
    // Create the map object with options
    var map = L.map("map-id", {
      center: [0, 0],
      zoom: 0,
      layers: [lightmap, earthquakes]
    });
  
    // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(map);
  }

  function createMarkers(response) {

    // Pull the "features" property off of response
    var features = response.features;
  
    // Initialize an array to hold earthquake markers
    var earthquakeMarkers = [];
  
    // Loop through the features array
    for (var index = 0; index < features.length; index++) {
      var feature = features[index];
  
      // For each feature, create a marker and bind a popup with the feature's place
      var earthquakeMarker = L.marker([feature.geometry.coordinates[1], feature.geometry.coordinates[0]])
        .bindPopup("<h3>" + feature.properties.place + "<h3>");
  
      // Add the marker to the bikeMarkers array
      earthquakeMarkers.push(earthquakeMarker);
    }
  
    // Create a layer group made from the bike markers array, pass it into the createMap function
    createMap(L.layerGroup(earthquakeMarkers));
  }


// Perform an API call to USGS to get data about last 30 days' significant earthquakes. Call createMarkers when complete
d3.json("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson", createMarkers);
 
  