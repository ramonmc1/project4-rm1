
function init() {

//Needed to bypass CORS restrictions when running the Json file locally
const sampleData2 = "/api/cluster";
const sampleData3 = "/api/elbow";
d3.json(sampleData2).then(function(data) {
  console.log(data)
  let resultname= ["2 Clusters", "3 Clusters", "4 Clusters", "6 Clusters"];
  
  
  var dropdownMenu = d3.select("#selDataset");

  let seldata = data.cluster2;


  bubbleChart(seldata);
  scatterChart(seldata);

resultname.forEach(function(CLUSTER){
  dropdownMenu.append("option").text(CLUSTER);
})

// On change to the DOM, call getData()
d3.selectAll("#selDataset").on("change", getData);


function getData() {

  // Assign the value of the dropdown menu option to a variable
  var dataset = dropdownMenu.property("value");
  var ndata = [];

if (dataset == '2 Clusters') {
   ndata = data.cluster2
}
else if (dataset == '3 Clusters') {
  ndata = data.cluster3;
}
else if (dataset == '4 Clusters') {
  ndata = data.cluster4;
}
else if (dataset == '6 Clusters') {
  ndata = data.cluster6;
}
  // Call function to update the chart
  updatePlotly(ndata);


}

function bubbleChart(seldata) {

  var trace1 = {
    x: seldata.x,
    y: seldata.y,
    //text: text1,
    mode: 'markers',
    marker: {
      size: 10,
      color:seldata.c,
      sizemode:'area',
      sizeref: .1
    }
  };
console.log(trace1);
  var datax = [trace1];
  
  var layout = {
    title: 'Housing Clusters',
    // xaxis: {
    //   title:'OTU IDs',},
    showlegend: false,
    height: 900,
    width: 1000
  };
  
  Plotly.newPlot('bubble', datax, layout);

}

function scatterChart(seldata) {

    var trace1 = {
      x: seldata.price,
      y: seldata.living_area,
      //text: text1,
      mode: 'markers',
      marker: {
        size: 5,
        color:seldata.clusters,
      }
    };
  
    var dataz = [trace1];
    
    var layout = {
      title: 'Price vs Living Area w/ Clusters',
      xaxis: {
      title:'Living Area',},
      yaxis: {
      title:'Price',},
      showlegend: false,
      height: 600,
      width: 600
    };
    
    Plotly.newPlot('scatter', dataz, layout);
  
  }
 
  function updatePlotly(newdata) {

  bubbleChart(newdata);
  scatterChart(newdata);

      }
  
d3.json(sampleData3).then(function(data2) {

  lineChart(data2);
  
function lineChart(data2) {

  var trace1 = {
    x: data2.k,
    y: data2.Inertia,
    type: 'scatter'
  };
  

  var data2 = [trace1];
  
  var layout = {
    title: 'Elbow Curve',
    xaxis: {
    title:'k values',},
    yaxis: {
    title:'Inertia',},
    showlegend: false,
    height: 450,
    width: 500
  };
  
  Plotly.newPlot('line', data2, layout);

};

});


});


}

init();
