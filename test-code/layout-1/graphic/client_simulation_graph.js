var simulation_client_array                     = [];
var simulation_client_graph_array               = [];
var simulation_client_graph_degree_target_array = [];
var simulation_client_name_array                = ["carl", "chris", "dennet", "neil", "richard", "sam"];
var simulation_client_online_chance_step        = 0.01;
var simulation_client_online_count              = 0;
var simulation_dimension                        = { height:320,width:320 };
var simulation_dimension_smallest               = simulation_dimension.height <= simulation_dimension.width ? simulation_dimension.height : simulation_dimension.width;
var simulation_padding                          = simulation_dimension_smallest/8;
var simulation_radius_main                      = simulation_dimension_smallest/2 - simulation_padding;
var simulation_radius_biggest                   = simulation_radius_main/6;
var simulation_radius_smallest                  = simulation_radius_main/12;
var simulation_scale_linear_pitch               = d3.scaleLinear().domain([0,pitch_max]).range([0,1]);
var simulation_scale_linear_volume              = d3.scaleLinear().domain([0,volume_max]).range([simulation_radius_smallest,simulation_radius_biggest]);
var simulation_translate                        = { x:simulation_dimension.width/2,y:simulation_dimension.height/2 };

var graph_demo_svg = d3.select("#graph_demo_svg_container").append("svg")
  .attr("height", "100%")
  .attr("id", "graph_demo_svg")
  .attr("width", "100%");

function simulation_client_graph (_client, _degree) {
  simulation_client_graph_array.push(this);
  this.client       = _client;
  this.client.graph = this;
  this.circle       = graph_demo_svg.append("circle")
    .attr ("class"       , "simulation_client_graph_circle")
    .attr ("cx"          , simulation_radius_main*Math.cos(Math.Radian(_degree)))
    .attr ("cy"          , simulation_radius_main*Math.sin(Math.Radian(_degree)))
    .attr ("degree"      , _degree)
    .attr ("id"          , this.client.name)
    .attr ("r"           , simulation_radius_biggest)
    .attr ("transform"   , "translate(" + simulation_translate.x + "," + simulation_translate.y + ")")
    .style("fill"        , this.client.graph_color)
    .style("stroke"      , this.client.graph_color)
    .style("stroke-width", "5px");
  simulation_client_graph_rotate_auto();
}
function simulation_client_graph_degree_target_determine () {
  simulation_client_graph_degree_target_array = [];
  for (var i = 0; i < simulation_client_graph_array.length; i ++) {
    var simulation_client_graph_degree_target_temp = (i/simulation_client_graph_array.length)*360;
    simulation_client_graph_degree_target_array.push(simulation_client_graph_degree_target_temp);
  }
}
function simulation_client_graph_pitch (_simulation_client_graph) {
  _simulation_client_graph.client.latest.pitch = (Math.random()*pitch_max).toFixed(3);
  _simulation_client_graph.circle.style(
    "fill",
    ShadeRGBColor(
      "rgb(" +
        HexRGB(_simulation_client_graph.client.graph_color).r + ", " +
        HexRGB(_simulation_client_graph.client.graph_color).g + ", " +
        HexRGB(_simulation_client_graph.client.graph_color).b +
      ")",
      simulation_scale_linear_pitch(
        _simulation_client_graph.client.latest.pitch
      )
    )
  );
}
function simulation_client_graph_presence () {
  for (var i = 0; i < simulation_client_graph_array.length; i ++) {
    var simulation_client_graph_temp = simulation_client_graph_array[i];
    for (var j = 0; j < simulation_client_graph_temp.client.latest.presence.length; j ++) {
      var simulation_client_temp = simulation_client_graph_temp.client.latest.presence[j];
      if (simulation_client_temp.latest.online) {
        var c_x_1    = Number(simulation_client_graph_temp.circle.attr("cx"));
        var c_x_2    = Number(simulation_client_temp.graph.circle.attr("cx"));
        var c_y_1    = Number(simulation_client_graph_temp.circle.attr("cy"));
        var c_y_2    = Number(simulation_client_temp.graph.circle.attr("cy"));
        var r_1      = Number(simulation_client_graph_temp.circle.attr("r" ));
        var r_2      = Number(simulation_client_temp.graph.circle.attr("r" ));
        var distance = Math.atan2(c_y_2 - c_y_1, c_x_2 - c_x_1);
        var x_1      = c_x_1 + (r_1*Math.cos(distance));
        var x_2      = c_x_2 - (r_2*Math.cos(distance));
        var y_1      = c_y_1 + (r_1*Math.sin(distance));
        var y_2      = c_y_2 - (r_2*Math.sin(distance));
        graph_demo_svg.append("circle")
          .attr("class", "simulation_presence_circle")
          .attr("cx", x_2)
          .attr("cy", y_2)
          .attr("r", 5)
          .attr(
            "transform",
            "translate(" +
              simulation_translate.x + ", " +
              simulation_translate.y +
            ")"
          )
          .style("opacity", 1)
          .style("fill", simulation_client_graph_temp.client.graph_color)
          .style("stroke", "no-stroke");
        graph_demo_svg.append("line")
          .attr("class", "simulation_presence_line")
          .attr("x1", x_1)
          .attr("y1", y_1)
          .attr("x2", x_2)
          .attr("y2", y_2)
          .attr(
            "transform",
            "translate(" +
              simulation_translate.x + ", " +
              simulation_translate.y +
            ")"
          )
          .style("opacity", 0.5)
          .style("stroke", simulation_client_graph_temp.client.graph_color)
          .style("stroke-width", "5px");
      }
    }
  }
}
function simulation_client_graph_rotate (_simulation_client_graph, _degree) {
  _simulation_client_graph.circle
    .attr("cx"    , simulation_radius_main*Math.cos(Math.Radian(_degree)))
    .attr("cy"    , simulation_radius_main*Math.sin(Math.Radian(_degree)))
    .attr("degree", _degree);
}
function simulation_client_graph_rotate_auto () {
  simulation_client_graph_degree_target_determine();
  for (var i = 0; i < simulation_client_graph_array.length; i ++) {
    var simulation_client_graph_temp = simulation_client_graph_array[i];
    simulation_client_graph_rotate(simulation_client_graph_temp, simulation_client_graph_degree_target_array[0])
    simulation_client_graph_degree_target_array.splice(0, 1);
  }
}
function simulation_client_graph_volume (_simulation_client_graph) {
  _simulation_client_graph.client.latest.volume = (Math.random()*volume_max).toFixed(3);
  _simulation_client_graph.circle.attr("r", simulation_scale_linear_volume(_simulation_client_graph.client.latest.volume));
}
function simulation_client (_name) {
  simulation_client_array.push(this);
  simulation_client_online_count ++;

  this.name = _name;
  this.graph_color = INTRGB(HashCode(this.name));
  this.latest = {
    face    :0,
    pitch   :0,
    volume  :0,
    online  :true,
    presence:[]
  };
  this.online_chance = 1;

  // Let `this` fully initiated first before creating the corresponding graph.
  this.graph = new simulation_client_graph(this, 180);
}
function simulation_client_all () {
  d3.selectAll(".simulation_presence_circle").remove();
  d3.selectAll(".simulation_presence_line"  ).remove();

  simulation_client_online();

  var debug_online   = "";
  var debug_pitch    = "";
  var debug_presence = "";
  var debug_volume   = "";

  for (var i = 0; i < simulation_client_array.length; i ++) {
    var simulation_client_temp = simulation_client_array[i];
    simulation_client_face(simulation_client_temp);
    simulation_client_pitch(simulation_client_temp);
    simulation_client_presence(simulation_client_temp);
    simulation_client_volume(simulation_client_temp);

    debug_online   += simulation_client_debug_online(simulation_client_temp)   + " ";
    debug_pitch    += simulation_client_debug_pitch(simulation_client_temp)    + " ";
    debug_volume   += simulation_client_debug_volume(simulation_client_temp)   + " ";
  }

  simulation_client_graph_presence();

  //console.log("=========================");
  //console.log(debug_online);
  //console.log(debug_pitch);
  //console.log(debug_presence);
  //console.log(debug_volume);
  //console.log("=========================");
}
function simulation_client_debug_online   (_simulation_client) { return _simulation_client.name + ":" + _simulation_client.latest.online; }
function simulation_client_debug_pitch    (_simulation_client) { return _simulation_client.name + ":" + _simulation_client.latest.pitch; }
function simulation_client_debug_presence (_simulation_client) { return _simulation_client.name + ":" + _simulation_client.latest.presence.length; }
function simulation_client_debug_volume   (_simulation_client) { return _simulation_client.name + ":" + _simulation_client.latest.volume; }
function simulation_client_face (_simulation_client) {
  if (_simulation_client.latest.online) {
    _simulation_client.latest.face = Math.ceil(
      Math.random()*simulation_client_online_count
    );
  }
}
function simulation_client_init () {
  for (var i = 0; i < simulation_client_name_array.length; i ++) {
    var simulation_client_name_temp = simulation_client_name_array[i];
    new simulation_client(simulation_client_name_temp);
  }
}
function simulation_client_online () {
  for (var i = 0; i < simulation_client_array.length; i ++) {
    var simulation_client_temp = simulation_client_array[i];
    var random = Math.random();

    if (random < simulation_client_temp.online_chance) {
      if (!simulation_client_temp.latest.online) {
        simulation_client_online_count ++;

        // Remove the graph of online client.
        simulation_client_temp.graph = new simulation_client_graph(simulation_client_temp, 180);
        // Re - position.
        simulation_client_graph_rotate_auto();

        simulation_client_temp.latest.online = true;
        simulation_client_temp.online_chance = 1;
      }
      else {
        simulation_client_temp.online_chance -= simulation_client_online_chance_step;
      }
    }
    else {
      if (simulation_client_temp.latest.online) {
        simulation_client_online_count --;

        // Remove the graph of offline client.
        simulation_client_temp.graph.circle.remove();
        simulation_client_graph_array.splice(simulation_client_graph_array.indexOf(simulation_client_temp.graph), 1);
        simulation_client_temp.graph = null;
        // Re - position.
        simulation_client_graph_rotate_auto();

        simulation_client_temp.latest.online = false;
        simulation_client_temp.online_chance = 0;
      }
      else {
        simulation_client_temp.online_chance += simulation_client_online_chance_step;
      }
    }
  }
}
function simulation_client_pitch (_simulation_client) {
  if (_simulation_client.latest.online) {
    _simulation_client.latest.pitch = (Math.random()*pitch_max).toFixed(3);
    simulation_client_graph_pitch(_simulation_client.graph);
  }
}
function simulation_client_presence (_simulation_client) {
  _simulation_client.latest.presence = [];
  if (_simulation_client.latest.online) {
    for (var i = 0; i < simulation_client_array.length; i ++) {
      var simulation_client_temp = simulation_client_array[i];
      if (
        (simulation_client_temp.name  != _simulation_client.name) &&
        (simulation_client_temp.latest.online) &&
        (Math.random() < 0.8)
      ) {
        _simulation_client.latest.presence.push(simulation_client_temp);
      }
    }
  }
}
function simulation_client_volume (_simulation_client) {
  if (_simulation_client.latest.online) {
    _simulation_client.latest.volume = (Math.random()*volume_max).toFixed(3);
    simulation_client_graph_volume(_simulation_client.graph);
  }
}