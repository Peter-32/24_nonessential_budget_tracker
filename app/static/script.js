console.log("Verify")
var spec = "/Users/petermyers/Desktop/high_quality_programs/24_nonessential_budget_tracker/chart.json";
  vegaEmbed('#vis', spec).then(function(result) {
    // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
  }).catch(console.error);
