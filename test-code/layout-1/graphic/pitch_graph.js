var axis_pitch_graph           = null;
var bottom_padding_pitch_graph = null;
var div_container_pitch_graph  = "";
var duration_pitch_graph       = null;
var has_inited_pitch_graph     = false;
var height_pitch_graph         = null;
var limit_pitch_graph          = null;
var line_pitch_graph           = null;
var now_pitch_graph            = null;
var path_data_pitch_graph      = null;
var path_pitch_graph           = null;
var svg_pitch_graph            = null;
var wait_pitch_graph           = 0;
var wait_start_pitch_graph     = false;
var width_pitch_graph          = null;
var x_pitch_graph              = null;
var y_pitch_graph              = null;
function pitch_graph_init () {
  bottom_padding_pitch_graph = $(div_container_pitch_graph).height()/6;
  duration_pitch_graph = 750;
  height_pitch_graph = $(div_container_pitch_graph).height() - bottom_padding_pitch_graph;
  limit_pitch_graph = 60;
  width_pitch_graph = $(div_container_pitch_graph).width();
  now_pitch_graph = new Date(Date.now() - duration_pitch_graph);

  path_data_pitch_graph = {
    pitch:{
      color:"gold",
      data:d3.range(limit_pitch_graph).map(function () {
        return 0;
      }),
      value:0
    }
  };

  x_pitch_graph = d3.scaleTime()
    .domain([now_pitch_graph - (limit_pitch_graph - 2), now_pitch_graph - duration_pitch_graph])
    .range([0, width_pitch_graph]);
  y_pitch_graph = d3.scaleLinear()
    .domain([0, 5000])
    .range([height_pitch_graph, 0]);

  line_pitch_graph = d3.line()
    .curve(d3.curveBasis)
    .x(function (d, i) {
      return x_pitch_graph(now_pitch_graph - (limit_pitch_graph - 1 - i)*duration_pitch_graph);
    })
    .y(function (d) {
      return y_pitch_graph(d);
    });

  svg_pitch_graph = d3.select(div_container_pitch_graph).append("svg")
    .attr("class", "chart")
    .attr("width", width_pitch_graph)
    .attr("height", height_pitch_graph + bottom_padding_pitch_graph);

  axis_pitch_graph = svg_pitch_graph.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height_pitch_graph + ")")
    .call(x_pitch_graph.axis = d3.axisBottom().scale(x_pitch_graph));

  path_pitch_graph = svg_pitch_graph.append("g")

  path_data_pitch_graph["pitch"].path = path_pitch_graph.append("path")
    .data([path_data_pitch_graph["pitch"].data])
    .attr("class", "pitch path")
    .style("stroke", path_data_pitch_graph["pitch"].color);

  pitch_graph_loop();
}
function pitch_graph_loop () {
  now_pitch_graph = new Date();

  path_data_pitch_graph["pitch"].data.push(pitch_value);
  path_data_pitch_graph["pitch"].path.attr("d", line_pitch_graph);

  x_pitch_graph.domain([
    now_pitch_graph - (limit_pitch_graph - 2)*duration_pitch_graph,
    now_pitch_graph - duration_pitch_graph
  ]);

  axis_pitch_graph
    .transition()
    .duration(duration_pitch_graph)
    .ease(d3.easeLinear)
    .call(x_pitch_graph.axis);

  path_pitch_graph.attr("transform", null)
    .transition()
    .attr("transform", "translate(" + x_pitch_graph(now_pitch_graph - (limit_pitch_graph - 1)*duration_pitch_graph) + ")")
    .duration(duration_pitch_graph)
    .ease(d3.easeLinear)
    .on("end", pitch_graph_loop);

  //Remove oldest data point from each groups.
  path_data_pitch_graph["pitch"].data.shift();
}
// Function to re - adjust the position and size of this graph.
function pitch_graph_resize () {
  bottom_padding_pitch_graph = $(div_container_pitch_graph).height()/6;
  height_pitch_graph = $(div_container_pitch_graph).height() - bottom_padding_pitch_graph;
  width_pitch_graph = $(div_container_pitch_graph).width();
  x_pitch_graph.range([0, width_pitch_graph]);
  y_pitch_graph.range([height_pitch_graph, 0]);
  svg_pitch_graph
    .attr("width", width_pitch_graph)
    .attr("height", height_pitch_graph + bottom_padding_pitch_graph);
  axis_pitch_graph
    .attr("transform", "translate(0," + height_pitch_graph + ")");
  path_pitch_graph.attr("transform", "translate(" + x_pitch_graph(now_pitch_graph - (limit_pitch_graph - 1)*duration_pitch_graph) + ")");
}