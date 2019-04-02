function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
    var metaDataQueryURL = `/metadata/${sample}`

    d3.json(metaDataQueryURL).then((metaData) => {
      var sampleMetaData = metaData;

      // Use d3 to select the panel with id of `#sample-metadata`
      var metaDataPanel = d3.select("#sample-metadata");

      // Use `.html("") to clear any existing metadata
      metaDataPanel.html("");

      // Use `Object.entries` to add each key and value pair to the panel
      // Hint: Inside the loop, you will need to use d3 to append new
      // tags for each key-value in the metadata.

      for (var i = 0; i < Object.keys(sampleMetaData).length - 1; i++) {
        metaDataPanel.append("li").text(`${Object.entries(sampleMetaData)[i][0]}: ${Object.entries(sampleMetaData)[i][1]}`);
      };
    });
    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
};

function buildCharts(sample) {

  var dataQueryURL = `/samples/${sample}`;
  // @TODO: Use `d3.json` to fetch the sample data for the plots
  d3.json(dataQueryURL).then(function(data) {
    var otuIDs = data.otu_ids;
    var sampleValues = data.sample_values;
    var otuLabels = data.otu_labels;

    // @TODO: Build a Bubble Chart using the sample data
    var trace = {
      x: otuIDs,
      y: sampleValues,
      text: otuLabels,
      mode: 'markers',
      marker: {
        color: otuLabels,
        size: sampleValues        
      }
    };

    var data1 = [trace];

    var layout = {
      showlegend: false,
      xaxis: {
        title:"OTU ID"
      }
  };

    Plotly.newPlot('bubble', data1, layout);
    
    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
    var dataArray = [];
    
    for (var i = 0; i < otuIDs.length; i++) {
      dataArray.push({
        otuIDs:otuIDs[i],
        otuLabels:otuLabels[i], 
        sampleValues:sampleValues[i]
        })
    };
    
    var orderedData = dataArray.sort(function(a, b) {
      return b.sampleValues - a.sampleValues;
      });

    var topTen = orderedData.slice(0, 10);

    var topTenOtuIDs = topTen.map(item => item.otuIDs);
    var topTenSampleValues = topTen.map(item => item.sampleValues);
    var topTenLabels = topTen.map(item => item.otuLabels);

    var data2 = [{
      values: topTenSampleValues,
      labels: topTenOtuIDs,
      text: topTenLabels,
      textinfo: 'percent',
      type: "pie"
    }];

    var layout = {

    };

    Plotly.newPlot("pie",data2,layout);

  });
};

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
};

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
};

// Initialize the dashboard
init();
