var demo_client_array                     = [];
var demo_client_graph_array               = [];
var demo_client_graph_degree_target_array = [];
var demo_client_name_array                = ["carl", "chris", "dennet", "neil", "richard", "sam"];
var demo_client_online_chance_step        = 0.01;
var demo_client_online_count              = 0;
var demo_dimension                        = { height:320,width:320 };
var demo_dimension_smallest               = demo_dimension.height <= demo_dimension.width ? demo_dimension.height : demo_dimension.width;
var demo_padding                          = demo_dimension_smallest/8;
var demo_radius_main                      = demo_dimension_smallest/2 - demo_padding;
var demo_radius_main_prev                 = demo_radius_main;
var demo_radius_biggest                   = demo_radius_main/6;
var demo_radius_smallest                  = demo_radius_main/12;
var demo_scale_linear_pitch               = d3.scaleLinear().domain([0,pitch_max]).range([0,1]);
var demo_scale_linear_volume              = d3.scaleLinear().domain([0,volume_max]).range([demo_radius_smallest,demo_radius_biggest]);
var demo_translate                        = { x:demo_dimension.width/2,y:demo_dimension.height/2 };

var graph_demo_svg = d3.select("#graph_demo_svg_container").append("svg")
  .attr("height", demo_dimension.height)
  .attr("id", "graph_demo_svg")
  .attr("width", demo_dimension.width);

function demo_client_graph (_client, _degree) {
  demo_client_graph_array.push(this);
  this.client       = _client;
  this.client.graph = this;
  this.circle       = graph_demo_svg.append("circle")
    .attr ("class"       , "demo_client_graph_circle")
    .attr ("cx"          , demo_radius_main*Math.cos(Math.Radian(_degree)))
    .attr ("cy"          , demo_radius_main*Math.sin(Math.Radian(_degree)))
    .attr ("degree"      , _degree)
    .attr ("id"          , this.client.name)
    .attr ("r"           , demo_radius_biggest)
    .attr ("transform"   , "translate(" + demo_translate.x + "," + demo_translate.y + ")")
    .style("fill"        , this.client.graph_color)
    .style("stroke"      , this.client.graph_color)
    .style("stroke-width", 5);
  demo_client_graph_rotate_auto();
}
function demo_client_graph_degree_target_determine () {
  demo_client_graph_degree_target_array = [];
  for (var i = 0; i < demo_client_graph_array.length; i ++) {
    var demo_client_graph_degree_target_temp = (i/demo_client_graph_array.length)*360;
    demo_client_graph_degree_target_array.push(demo_client_graph_degree_target_temp);
  }
}
function demo_client_graph_pitch (_demo_client_graph) {
  _demo_client_graph.client.latest.pitch = (Math.random()*pitch_max).toFixed(3);
  _demo_client_graph.circle.style(
    "fill",
    ShadeRGBColor(
      "rgb(" +
        HexRGB(_demo_client_graph.client.graph_color).r + ", " +
        HexRGB(_demo_client_graph.client.graph_color).g + ", " +
        HexRGB(_demo_client_graph.client.graph_color).b +
      ")",
      demo_scale_linear_pitch(
        _demo_client_graph.client.latest.pitch
      )
    )
  );
}
function demo_client_graph_presence () {
  for (var i = 0; i < demo_client_graph_array.length; i ++) {
    var demo_client_graph_temp = demo_client_graph_array[i];
    for (var j = 0; j < demo_client_graph_temp.client.latest.presence.length; j ++) {
      var demo_client_temp = demo_client_graph_temp.client.latest.presence[j];
      if (demo_client_temp.latest.online) {
        var c_x_1    = Number(demo_client_graph_temp.circle.attr("cx"));
        var c_x_2    = Number(demo_client_temp.graph.circle.attr("cx"));
        var c_y_1    = Number(demo_client_graph_temp.circle.attr("cy"));
        var c_y_2    = Number(demo_client_temp.graph.circle.attr("cy"));
        var r_1      = Number(demo_client_graph_temp.circle.attr("r" ));
        var r_2      = Number(demo_client_temp.graph.circle.attr("r" ));
        var distance = Math.atan2(c_y_2 - c_y_1, c_x_2 - c_x_1);
        var x_1      = c_x_1 + (r_1*Math.cos(distance));
        var x_2      = c_x_2 - (r_2*Math.cos(distance));
        var y_1      = c_y_1 + (r_1*Math.sin(distance));
        var y_2      = c_y_2 - (r_2*Math.sin(distance));
        graph_demo_svg.append("circle")
          .attr("class", "demo_presence_circle")
          .attr("cx", x_2)
          .attr("cy", y_2)
          .attr("r", 5)
          .attr(
            "transform",
            "translate(" +
              demo_translate.x + ", " +
              demo_translate.y +
            ")"
          )
          .style("opacity", 1)
          .style("fill", demo_client_graph_temp.client.graph_color)
          .style("stroke", "no-stroke");
        graph_demo_svg.append("line")
          .attr("class", "demo_presence_line")
          .attr("x1", x_1)
          .attr("y1", y_1)
          .attr("x2", x_2)
          .attr("y2", y_2)
          .attr(
            "transform",
            "translate(" +
              demo_translate.x + ", " +
              demo_translate.y +
            ")"
          )
          .style("opacity", 0.5)
          .style("stroke", demo_client_graph_temp.client.graph_color)
          .style("stroke-width", 5);
      }
    }
  }
}
function demo_client_graph_resize () {
  demo_dimension                 = { height:$("#graph_demo_svg_container").height(),width:$("#graph_demo_svg_container").width() };
  demo_dimension_smallest        = demo_dimension.height <= demo_dimension.width ? demo_dimension.height : demo_dimension.width;
  demo_padding                   = demo_dimension_smallest/8;

  // Make sure the resize happens only when there is a change in size.
  if (demo_radius_main != demo_dimension_smallest/2 - demo_padding) {
    d3.selectAll(".demo_presence_circle").remove();
    d3.selectAll(".demo_presence_line"  ).remove();

    demo_radius_main_prev        = demo_radius_main;

    demo_radius_main             = demo_dimension_smallest/2 - demo_padding;
    demo_radius_biggest          = demo_radius_main/6;
    demo_radius_smallest         = demo_radius_main/12;
    demo_scale_linear_pitch      = d3.scaleLinear().domain([0,pitch_max]).range([0,1]);
    demo_scale_linear_volume     = d3.scaleLinear().domain([0,volume_max]).range([demo_radius_smallest,demo_radius_biggest]);
    demo_translate               = { x:demo_dimension.width/2,y:demo_dimension.height/2 };

    graph_demo_svg
      .attr("height", demo_dimension.height)
      .attr("width" , demo_dimension.width);

    for (var i = 0; i < demo_client_graph_array.length; i ++) {
      var demo_client_graph_temp = demo_client_graph_array[i];
      var degree                       = Number(demo_client_graph_temp.circle.attr("degree"));
      var radius_prev                  = Number(demo_client_graph_temp.circle.attr("r"));
      var radius_proportion            = (demo_radius_main/demo_radius_main_prev < 1) ? 1 : (demo_radius_main/demo_radius_main_prev);
      var radius                       = radius_proportion*radius_prev;
      demo_client_graph_temp.circle
        .attr("cx"       , demo_radius_main*Math.cos(Math.Radian(degree)))
        .attr("cy"       , demo_radius_main*Math.sin(Math.Radian(degree)))
        .attr("r"        , demo_radius_biggest)
        .attr("transform", "translate(" + demo_translate.x + "," + demo_translate.y + ")");
    }
  }
}
function demo_client_graph_rotate (_demo_client_graph, _degree) {
  _demo_client_graph.circle
    .attr("cx"    , demo_radius_main*Math.cos(Math.Radian(_degree)))
    .attr("cy"    , demo_radius_main*Math.sin(Math.Radian(_degree)))
    .attr("degree", _degree);
}
function demo_client_graph_rotate_auto () {
  demo_client_graph_degree_target_determine();
  if (demo_client_graph_array.length == 1){
    demo_client_graph_array[0].circle
      .attr("cx"    , 0)
      .attr("cy"    , 0)
      .attr("degree", 0);
  }
  else{
    for (var i = 0; i < demo_client_graph_array.length; i ++) {
      var demo_client_graph_temp = demo_client_graph_array[i];
      demo_client_graph_rotate(demo_client_graph_temp, demo_client_graph_degree_target_array[0])
      demo_client_graph_degree_target_array.splice(0, 1);
    }
  }
}
function demo_client_graph_volume (_demo_client_graph) {
  _demo_client_graph.client.latest.volume = (Math.random()*volume_max).toFixed(3);
  _demo_client_graph.circle.attr("r", demo_scale_linear_volume(_demo_client_graph.client.latest.volume));
}
function demo_client (_name) {
  demo_client_array.push(this);
  demo_client_online_count ++;

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
  this.graph = new demo_client_graph(this, 180);
}
function demo_client_all () {
  d3.selectAll(".demo_presence_circle").remove();
  d3.selectAll(".demo_presence_line"  ).remove();

  demo_client_online();

  var debug_online   = "";
  var debug_pitch    = "";
  var debug_presence = "";
  var debug_volume   = "";

  for (var i = 0; i < demo_client_array.length; i ++) {
    var demo_client_temp = demo_client_array[i];
    demo_client_face(demo_client_temp);
    demo_client_pitch(demo_client_temp);
    demo_client_presence(demo_client_temp);
    demo_client_volume(demo_client_temp);

    debug_online   += demo_client_debug_online(demo_client_temp)   + " ";
    debug_pitch    += demo_client_debug_pitch(demo_client_temp)    + " ";
    debug_volume   += demo_client_debug_volume(demo_client_temp)   + " ";
  }

  demo_client_graph_presence();

  //console.log("=========================");
  //console.log(debug_online);
  //console.log(debug_pitch);
  //console.log(debug_presence);
  //console.log(debug_volume);
  //console.log("=========================");
}
function demo_client_debug_online   (_demo_client) { return _demo_client.name + ":" + _demo_client.latest.online; }
function demo_client_debug_pitch    (_demo_client) { return _demo_client.name + ":" + _demo_client.latest.pitch; }
function demo_client_debug_presence (_demo_client) { return _demo_client.name + ":" + _demo_client.latest.presence.length; }
function demo_client_debug_volume   (_demo_client) { return _demo_client.name + ":" + _demo_client.latest.volume; }
function demo_client_face (_demo_client) {
  if (_demo_client.latest.online) {
    _demo_client.latest.face = Math.ceil(
      Math.random()*demo_client_online_count
    );
  }
}
function demo_client_init () {
  for (var i = 0; i < demo_client_name_array.length; i ++) {
    var demo_client_name_temp = demo_client_name_array[i];
    new demo_client(demo_client_name_temp);
  }
}
function demo_client_online () {
  for (var i = 0; i < demo_client_array.length; i ++) {
    var demo_client_temp = demo_client_array[i];
    var random = Math.random();

    if (random < demo_client_temp.online_chance) {
      if (!demo_client_temp.latest.online) {
        demo_client_online_count ++;

        // Remove the graph of online client.
        demo_client_temp.graph = new demo_client_graph(demo_client_temp, 180);
        // Re - position.
        demo_client_graph_rotate_auto();

        demo_client_temp.latest.online = true;
        demo_client_temp.online_chance = 1;
      }
      else {
        demo_client_temp.online_chance -= demo_client_online_chance_step;
      }
    }
    else {
      if (demo_client_temp.latest.online) {
        demo_client_online_count --;

        // Remove the graph of offline client.
        demo_client_temp.graph.circle.remove();
        demo_client_graph_array.splice(demo_client_graph_array.indexOf(demo_client_temp.graph), 1);
        demo_client_temp.graph = null;
        // Re - position.
        demo_client_graph_rotate_auto();

        demo_client_temp.latest.online = false;
        demo_client_temp.online_chance = 0;
      }
      else {
        demo_client_temp.online_chance += demo_client_online_chance_step;
      }
    }
  }
}
function demo_client_pitch (_demo_client) {
  if (_demo_client.latest.online) {
    _demo_client.latest.pitch = (Math.random()*pitch_max).toFixed(3);
    demo_client_graph_pitch(_demo_client.graph);
  }
}
function demo_client_presence (_demo_client) {
  _demo_client.latest.presence = [];
  if (_demo_client.latest.online) {
    for (var i = 0; i < demo_client_array.length; i ++) {
      var demo_client_temp = demo_client_array[i];
      if (
        (demo_client_temp.name  != _demo_client.name) &&
        (demo_client_temp.latest.online) &&
        (Math.random() < 0.8)
      ) {
        _demo_client.latest.presence.push(demo_client_temp);
      }
    }
  }
}
function demo_client_volume (_demo_client) {
  if (_demo_client.latest.online) {
    _demo_client.latest.volume = (Math.random()*volume_max).toFixed(3);
    demo_client_graph_volume(_demo_client.graph);
  }
}