console.log("Verify")
var spec = "/Users/petermyers/Desktop/high_quality_programs/24_nonessential_budget_tracker/chart.json";
var spec2 = "/Users/petermyers/Desktop/high_quality_programs/24_nonessential_budget_tracker/bar.vl.json";
  vegaEmbed('#vis', spec2).then(function(result) {
    // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
  }).catch(console.error);
