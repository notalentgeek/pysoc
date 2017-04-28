var currDateTime = new Date();

var simulateClientNameIRCodeList = [

    "carl",
    "chris",
    "dennet",
    "richard",
    "neil",
    "sam"

];

var d3Dimension = { width: 480, height: 480 };
var d3DimensionSmallest = (d3Dimension.width < d3Dimension.height) ? d3Dimension.width : d3Dimension.height;
var d3DimensionTranslate = { x: (d3Dimension.width/2), y: (d3Dimension.height/2) };
var d3Padding = d3DimensionSmallest/8;

var mainCircleRadius = (d3DimensionSmallest/2) - d3Padding;
var d3SVG = d3.select("#d3real").append("svg")
    .attr("height", d3Dimension.height)
    .attr("id", "d3SVG")
    .attr("width", d3Dimension.width);
    //.style("border", "2px solid blue");
var simulateD3SVG = d3.select("#d3sim").append("svg")
    .attr("height", d3Dimension.height)
    .attr("id", "simulateD3SVG")
    .attr("width", d3Dimension.width);
    //.style("border", "2px solid red");

/*
var mainCircleFill = "none";
var mainCircleStroke = "#008000";
var mainCircleStrokeWidth = 5;
var mainCirc = simulateD3SVG.append("circle")
    .attr("cx", 0)
    .attr("cy", 0)
    .attr("fill", mainCircleFill)
    .attr("r", mainCircleRadius)
    .attr("stroke", mainCircleStroke)
    .attr("stroke-width", mainCircleStrokeWidth)
    .attr("transform", "translate(" + d3DimensionTranslate.x + ", " + d3DimensionTranslate.y + ")");
*/