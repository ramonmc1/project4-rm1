
function init() {

//Needed to bypass CORS restrictions when running the Json file locally
const sampleData4 = "/api/linear";
const sampleData5 = "/api/linreg";

d3.json(sampleData4).then(function(data) {
    
  boxChart(data);


function boxChart(data) {


var box1 = [
  {
    y: data.price,
    name: "House Pricing",
    boxpoints: 'all',
    jitter: 0.3,
    pointpos: -1.8,
    type: 'box'
  }
];

Plotly.newPlot('box1', box1);

var box2 = [
  {
    y: data.livingarea,
    name: "Living Area",
    boxpoints: 'all',
    jitter: 0.3,
    pointpos: -1.8,
    type: 'box'
  }
];

Plotly.newPlot('box2', box2);


var box3 = [
  {
    y: data.yearbuilt,
    name: "Year Built",
    boxpoints: 'all',
    jitter: 0.3,
    pointpos: -1.8,
    type: 'box'
  }
];

Plotly.newPlot('box3', box3);


var box4 = [
  {
    y: data.familyincome,
    name: "Average Family Income",
    boxpoints: 'all',
    jitter: 0.3,
    pointpos: -1.8,
    type: 'box'
  }
];

Plotly.newPlot('box4', box4);
}




d3.json(sampleData5).then(function(data) {
  
  scatterChart(data);

  function scatterChart(data) {

       var trace1 = {
        x: data.livingarea,
        y: data.price,
        //text: text1,
        mode: 'markers',
        marker: {
          size: 5,
          //color:data.class3,
        }
      };
      var trace2 = {
        x: data.livingarea,
        y: data.pred_la_price,
        //text: text1,
        mode: 'lines'
 
      };
      
      var data = [trace1, trace2];
      
      var layout = {
        title: 'Price vs Living Area w/ regression',
        xaxis: {
          title: 'Living Area (ft2)',
          showgrid: false,
          zeroline: false
        },
        yaxis: {
          title: 'Price - USD',
          showline: false
        },
         showlegend: false,
         height: 500,
         width: 500
       };
      Plotly.newPlot('linreg1', data,  layout);
    
    };
    scatterChart2(data);
    function scatterChart2(data) {

      var trace1 = {
       x: data.bathrooms,
       y: data.price,
       //text: text1,
       mode: 'markers',
       marker: {
         size: 5,
         //color:data.class3,
       }
     };
     var trace2 = {
       x: data.bathrooms,
       y: data.pred_ba_price,
       //text: text1,
       mode: 'lines'

     };
     
     var data = [trace1, trace2];
     
     var layout = {
       title: 'Price vs Number of Bathrooms w/ regression',
       xaxis: {
        title: 'Number of Bathrooms',
        showgrid: false,
        zeroline: false
      },
      yaxis: {
        title: 'Price - USD',
        showline: false
      },
       showlegend: false,
       height: 500,
       width: 500
     };
     
     Plotly.newPlot('linreg2', data,  layout);
   
   };




});

});


}

init();
