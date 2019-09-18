var data = [4, 8, 15, 16, 23, 42, 50];

var x = d3.scale.linear()
    .domain([0, d3.max(data)])
    .range([0, 500]);

d3.select(".chart")
  .selectAll("div")
    .data(data)
  .enter().append("div")
    .style("width", function(d) { return x(d) + "px"; })
    .text(function(d) { return d; });