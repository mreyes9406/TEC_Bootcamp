var tableData = data;

var searchDate = d3.select("#filter-btn");

var tbody = d3.select("tbody");

data.forEach(function(ufoReport) {
    
    var row = tbody.append("tr");
    Object.entries(ufoReport).forEach(function([key, value]) {
        
        var cell = tbody.append("td");
        cell.text(value);
    });
});

searchDate.on("click", function() {
                            
    d3.event.preventDefault();
                            
    var inputElement = d3.select("#datetime");
                            
    var inputValue = inputElement.property("value");
                            
    var filteredData = data.filter(data => data.datetime === inputValue);
                            
    console.log(filteredData);
    
})