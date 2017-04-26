var axis_volume_graph           = null;
var bottom_padding_volume_graph = null;
var div_container_volume_graph  = "";
var duration_volume_graph       = null;
var has_inited_volume_graph     = false;
var height_volume_graph         = null;
var limit_volume_graph          = null;
var line_volume_graph           = null;
var now_volume_graph            = null;
var path_data_volume_graph      = null;
var path_volume_graph           = null;
var svg_volume_graph            = null;
var wait_start_volume_graph     = false;
var wait_volume_graph           = 0;
var width_volume_graph          = null;
var x_volume_graph              = null;
var y_volume_graph              = null;
function volume_graph_init () {
  bottom_padding_volume_graph = $(div_container_volume_graph).height()/6;
  duration_volume_graph = 750;
  height_volume_graph = $(div_container_volume_graph).height() - bottom_padding_volume_graph;
  limit_volume_graph = 60;
  width_volume_graph = $(div_container_volume_graph).width();
  now_volume_graph = new Date(Date.now() - duration_volume_graph);

  path_data_volume_graph = {
    volume:{
      color:"goldenrod",
      data:d3.range(limit_volume_graph).map(function () {
        return 0;
      }),
      value:0
    }
  };

  x_volume_graph = d3.scaleTime()
    .domain([now_volume_graph - (limit_volume_graph - 2), now_volume_graph - duration_volume_graph])
    .range([0, width_volume_graph]);
  y_volume_graph = d3.scaleLinear()
    .domain([0, 0.1])
    .range([height_volume_graph, 0]);

  line_volume_graph = d3.line()
    .curve(d3.curveBasis)
    .x(function (d, i) {
      return x_volume_graph(now_volume_graph - (limit_volume_graph - 1 - i)*duration_volume_graph);
    })
    .y(function (d) {
      return y_volume_graph(d);
    });

  svg_volume_graph = d3.select(div_container_volume_graph).append("svg")
    .attr("class", "chart")
    .attr("width", width_volume_graph)
    .attr("height", height_volume_graph + bottom_padding_volume_graph);

  axis_volume_graph = svg_volume_graph.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height_volume_graph + ")")
    .call(x_volume_graph.axis = d3.axisBottom().scale(x_volume_graph));

  path_volume_graph = svg_volume_graph.append("g")

  path_data_volume_graph["volume"].path = path_volume_graph.append("path")
    .data([path_data_volume_graph["volume"].data])
    .attr("class", "volume path")
    .style("stroke", path_data_volume_graph["volume"].color);

  volume_graph_loop();
}
function volume_graph_loop () {
  now_volume_graph = new Date();

  path_data_volume_graph["volume"].data.push(volume_value);
  path_data_volume_graph["volume"].path.attr("d", line_volume_graph);

  x_volume_graph.domain([
    now_volume_graph - (limit_volume_graph - 2)*duration_volume_graph,
    now_volume_graph - duration_volume_graph
  ]);

  axis_volume_graph
    .transition()
    .duration(duration_volume_graph)
    .ease(d3.easeLinear)
    .call(x_volume_graph.axis);

  path_volume_graph.attr("transform", null)
    .transition()
    .attr("transform", "translate(" + x_volume_graph(now_volume_graph - (limit_volume_graph - 1)*duration_volume_graph) + ")")
    .duration(duration_volume_graph)
    .ease(d3.easeLinear)
    .on("end", volume_graph_loop);

  //Remove oldest data point from each groups.
  path_data_volume_graph["volume"].data.shift();
}
// Function to re - adjust the position and size of this graph.
function volume_graph_resize () {
  bottom_padding_volume_graph = $(div_container_volume_graph).height()/6;
  height_volume_graph = $(div_container_volume_graph).height() - bottom_padding_volume_graph;
  width_volume_graph = $(div_container_volume_graph).width();
  x_volume_graph.range([0, width_volume_graph]);
  y_volume_graph.range([height_volume_graph, 0]);
  svg_volume_graph
    .attr("width", width_volume_graph)
    .attr("height", height_volume_graph + bottom_padding_volume_graph);
  axis_volume_graph
    .attr("transform", "translate(0," + height_volume_graph + ")");
  path_volume_graph.attr("transform", "translate(" + x_volume_graph(now_volume_graph - (limit_volume_graph - 1)*duration_volume_graph) + ")");
}