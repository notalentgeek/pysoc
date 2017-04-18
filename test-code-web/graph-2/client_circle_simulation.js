var d3_dimension = { height:480,width:480 };
var d3_dimension_smallest = (d3_dimension.height < d3_dimension.width) ? d3_dimension.height : d3_dimension.width
var d3_dimension_translate = { x:d3_dimension.width/2, y:d3_dimension.height/2 }
var d3_padding = d3_dimension_smallest/8;

var client_circle_degree_target_array = [];
var client_circle_radius = (d3_dimension_smallest/2) - d3_padding;
var client_circle_radius_biggest = client_circle_radius/6;
var client_circle_radius_smallest = client_circle_radius/12;
var client_circle_simulation_array = [];
var scale_linear_pitch = d3.scaleLinear()
  .domain([0, 5000])
  .range([0, 1]);
var scale_linear_volume = d3.scaleLinear()
  .domain([0, 0.1])
  .range([client_circle_radius_smallest, client_circle_radius_biggest]);

var graph_demo_svg = d3.select("#graph_demo").append("svg")
    .attr("height", d3_dimension.height)
    .attr("id", "graph_demo_svg")
    .attr("width", d3_dimension.width);

function animation_for_client_circle_simulation(){

    d3.selectAll(".simulate-circle").remove();
    d3.selectAll(".simulate-line").remove();

    for(var i = 0; i < client_circle_simulation_array.length; i ++){

        // Check if this client circle will be deleted.
        if(!client_circle_simulation_array[i].will_be_deleted && client_circle_simulation_array[i] !== null && client_circle_simulation_array[i] !== undefined){

            // Move the client circle clock wise.
            if(
                (client_circle_simulation_array[i].degree_current > client_circle_simulation_array[i].degree_target) &&
                (client_circle_simulation_array[i].degree_saved > client_circle_simulation_array[i].degree_target)
            ){

                //console.log(client_circle_simulation_array[i]);
                //console.log(client_circle_simulation_array[i].c_x);
                //console.log(client_circle_simulation_array[i].degree_current);
                //console.log(client_circle_simulation_array[i].degree_saved);
                //console.log(client_circle_simulation_array[i].degree_target);

                var degree_step = -120;
                //var degree_step = -1*(Math.abs(client_circle_simulation_array[i].degree_saved - client_circle_simulation_array[i].degree_target)/100);
                //console.log(client_circle_simulation_array[i].c_x);

                client_circle_simulation_array[i].degree_current = Math.EaseInExpo(client_circle_simulation_array[i].time, client_circle_simulation_array[i].degree_current, degree_step, 32*client_circle_simulation_array.length);
                client_circle_simulation_array[i].c_x = client_circle_radius * Math.cos(Math.Radian(client_circle_simulation_array[i].degree_current));
                client_circle_simulation_array[i].c_y = client_circle_radius * Math.sin(Math.Radian(client_circle_simulation_array[i].degree_current));
                client_circle_simulation_array[i].time ++;

                /*
                d3.selectAll(".circle " + client_circle_simulation_array[i].client.name).remove();
                d3.selectAll(".line " + client_circle_simulation_array[i].client.name).remove();
                for(var j = 0; j < client_circle_simulation_array[i].client.latestIRCodeClientCircle.length; j ++){

                    d3.selectAll(".circle " + client_circle_simulation_array[i].client.latestIRCodeClientCircle[j].client.name).remove();

                }
                */

                //console.log(client_circle_simulation_array[i]);
                //console.log(client_circle_simulation_array[i].c_x);
                //console.log(client_circle_simulation_array[i].c_y);
                //console.log(client_circle_simulation_array[i].degree_current);
                //console.log(client_circle_radius);
                //console.log(Math.sin(Math.Radian(client_circle_simulation_array[i].degree_current)));

                if(client_circle_simulation_array[i].circle.style("opacity") < 1){

                    var opacity_step = Number(client_circle_simulation_array[i].circle.style("opacity")) + 0.1;
                    opacity_step = (opacity_step > 1) ? 1 : opacity_step;

                    client_circle_simulation_array[i].circle
                        .transition()
                        .attr("cx", client_circle_simulation_array[i].c_x)
                        .attr("cy", client_circle_simulation_array[i].c_y)
                        .style("opacity", opacity_step)
                        .duration(0.1)
                        .on("end", animation_for_client_circle_simulation);

                }
                else{

                    client_circle_simulation_array[i].circle
                        .transition()
                        .attr("cx", client_circle_simulation_array[i].c_x)
                        .attr("cy", client_circle_simulation_array[i].c_y)
                        .duration(0.1)
                        .on("end", animation_for_client_circle_simulation);

                }

            }
            // Move counter clock wise.
            else if(
                (client_circle_simulation_array[i].degree_current < client_circle_simulation_array[i].degree_target) &&
                (client_circle_simulation_array[i].degree_saved < client_circle_simulation_array[i].degree_target)
            ){

                //console.log(client_circle_simulation_array[i]);
                //console.log(client_circle_simulation_array[i].c_x);
                //console.log(client_circle_simulation_array[i].degree_current);
                //console.log(client_circle_simulation_array[i].degree_saved);
                //console.log(client_circle_simulation_array[i].degree_target);

                var degree_step = 120;
                //var degree_step = Math.abs(client_circle_simulation_array[i].degree_saved - client_circle_simulation_array[i].degree_target)/100;

                client_circle_simulation_array[i].degree_current = Math.EaseInExpo(client_circle_simulation_array[i].time, client_circle_simulation_array[i].degree_current, degree_step, 32*client_circle_simulation_array.length);
                client_circle_simulation_array[i].c_x = client_circle_radius * Math.cos(Math.Radian(client_circle_simulation_array[i].degree_current));
                client_circle_simulation_array[i].c_y = client_circle_radius * Math.sin(Math.Radian(client_circle_simulation_array[i].degree_current));
                client_circle_simulation_array[i].time ++;

                /*
                d3.selectAll(".circle " + client_circle_simulation_array[i].client.name).remove();
                d3.selectAll(".line " + client_circle_simulation_array[i].client.name).remove();
                for(var j = 0; j < client_circle_simulation_array[i].client.latestIRCodeClientCircle.length; j ++){

                    d3.selectAll(".circle " + client_circle_simulation_array[i].client.latestIRCodeClientCircle[j].client.name).remove();

                }
                */

                //console.log(client_circle_simulation_array[i].c_x);

                if(client_circle_simulation_array[i].circle.style("opacity") < 1){

                    var opacity_step = Number(client_circle_simulation_array[i].circle.style("opacity")) + 0.1;

                    client_circle_simulation_array[i].circle
                        .transition()
                        .attr("cx", client_circle_simulation_array[i].c_x)
                        .attr("cy", client_circle_simulation_array[i].c_y)
                        .style("opacity", opacity_step)
                        .duration(0.1)
                        .on("end", animation_for_client_circle_simulation);

                }
                else{

                    client_circle_simulation_array[i].circle
                        .transition()
                        .attr("cx", client_circle_simulation_array[i].c_x)
                        .attr("cy", client_circle_simulation_array[i].c_y)
                        .duration(0.1)
                        .on("end", animation_for_client_circle_simulation);

                }

            }
            else{

                /*
                d3.selectAll(".circle " + client_circle_simulation_array[i].client.name).remove();
                d3.selectAll(".line " + client_circle_simulation_array[i].client.name).remove();
                for(var j = 0; j < client_circle_simulation_array[i].client.latestIRCodeClientCircle.length; j ++){

                    d3.selectAll(".circle " + client_circle_simulation_array[i].client.latestIRCodeClientCircle[j].client.name).remove();

                }
                */

                //console.log(client_circle_simulation_array[i]);
                //console.log(client_circle_simulation_array[i].c_x);

                client_circle_simulation_array[i].degree_current = client_circle_simulation_array[i].degree_target;
                client_circle_simulation_array[i].degree_saved = client_circle_simulation_array[i].degree_current;
                client_circle_simulation_array[i].c_x = client_circle_radius * Math.cos(Math.Radian(client_circle_simulation_array[i].degree_current));
                client_circle_simulation_array[i].c_y = client_circle_radius * Math.sin(Math.Radian(client_circle_simulation_array[i].degree_current));
                client_circle_simulation_array[i].time = 0;

                if(client_circle_simulation_array[i] === null || client_circle_simulation_array[i] === undefined){ console.log(client_circle_simulation_array[i].c_x); }

                //console.log(client_circle_simulation_array[i].c_x);

                if(client_circle_simulation_array[i].circle.style("opacity") < 1){

                    var opacity_step = Number(client_circle_simulation_array[i].circle.style("opacity")) + 0.1;

                    client_circle_simulation_array[i].circle
                        .transition()
                        .attr("cx", client_circle_simulation_array[i].c_x)
                        .attr("cy", client_circle_simulation_array[i].c_y)
                        .style("opacity", opacity_step)
                        .duration(0.1)
                        .on("end", animation_for_client_circle_simulation);

                }
                else{

                    client_circle_simulation_array[i].circle
                        .transition()
                        .attr("cx", client_circle_simulation_array[i].c_x)
                        .attr("cy", client_circle_simulation_array[i].c_y)
                        .duration(0.1);

                }

            }

        }
        else if(client_circle_simulation_array[i].will_be_deleted && client_circle_simulation_array[i] !== null && client_circle_simulation_array[i] !== undefined){

            /*
            d3.selectAll(".circle " + client_circle_simulation_array[i].client.name).remove();
            d3.selectAll(".line " + client_circle_simulation_array[i].client.name).remove();
            for(var j = 0; j < client_circle_simulation_array[i].client.latestIRCodeClientCircle.length; j ++){

                d3.selectAll(".circle " + client_circle_simulation_array[i].client.latestIRCodeClientCircle[j].client.name).remove();

            }
            */

            client_circle_simulation_array[i].time = 0;

            if(client_circle_simulation_array[i].circle.style("opacity") > 0){

                var opacity_step = Number(client_circle_simulation_array[i].circle.style("opacity")) - 0.1;

                client_circle_simulation_array[i].circle
                    .transition()
                    .style("opacity", opacity_step)
                    .duration(0.1)
                    .on("end", animation_for_client_circle_simulation);

            }
            else{

                var clientCircleTemp = client_circle_simulation_array[i];

                client_circle_simulation_array[i].circle.remove();

                var index = client_circle_simulation_array.indexOf(client_circle_simulation_array[i]);
                if(index > -1){ client_circle_simulation_array.splice(index, 1); }

                clientCircleTemp.client.clientCircle = null;
                clientCircleTemp.client = null;
                delete clientCircleTemp;

                console.log(client_circle_simulation_array.length);
                console.log(client_circle_degree_target_array);
                determine_target_for_client_circle_simulation(client_circle_simulation_array.length);
                for(var j = 0; j < client_circle_simulation_array.length; j ++){

                    client_circle_simulation_array[j].degree_saved = client_circle_simulation_array[j].degree_current;
                    client_circle_simulation_array[j].rotate_auto();

                }

            }

        }

    }

}

function determine_target_for_client_circle_simulation (_length) {
  client_circle_degree_target_array = [];
  for (var i = 0; i < _length; i ++) {
    var client_circle_degree_target = (((i/_length) * 360) + 180)%360;
    client_circle_degree_target_array.push(client_circle_degree_target);
  }
}

function client_circle_simulation (_client, _degree) {
  this.client = _client;
  this.client.client_circle = this;
  this.degree_current = _degree;
  this.degree_saved = this.degree_current;
  this.degree_target = this.degree_current;
  this.radius = client_circle_radius_biggest;
  this.time = 0;
  this.will_be_deleted = false;

  client_circle_simulation_array.push(this);

  this.c_x = client_circle_radius * Math.sin(Math.Radian(this.degree_current));
  this.c_y = client_circle_radius * Math.cos(Math.Radian(this.degree_current));

  this.circle = d3.select("#graph_demo_svg").append("circle")
    .attr("cx", this.c_x)
    .attr("cy", this.c_y)
    .attr("id", this.client.client_name)
    .attr("r", this.radius)
    .attr(
      "transform",
      "translate(" + d3_dimension_translate.x + ", " + d3_dimension_translate.y + ")"
    )
    .style("fill", this.client.client_circle_color)
    .style("opacity", 1)
    .style("stroke", this.client.client_circle_color)
    .style("stroke-width", 5);
}
client_circle_simulation.prototype.constructor = client_circle_simulation;
client_circle_simulation.prototype.rotate = function (_degree) {
  this.degree_target = _degree;
  this.time = 0;
  animation_for_client_circle_simulation();
}
client_circle_simulation.prototype.rotate_auto = function () {
  var degree_shortest = null;
  var client_circle_degree_target_array_temp = client_circle_degree_target_array;
  for (var i = 0; i < client_circle_degree_target_array_temp.length; i ++) {
    if (
      degree_shortest !== null &&
      degree_shortest !== undefined
    ) {
      degree_shortest = client_circle_degree_target_array_temp[i];
    }

    if (
      Math.abs(this.degree_current - client_circle_degree_target_array_temp[i]) <= degree_shortest
    ) {
      degree_shortest = client_circle_degree_target_array_temp[i];
    }
  }

  var index = client_circle_degree_target_array_temp.indexOf(degree_shortest);
  if (index > -1) {
    client_circle_degree_target_array_temp.splice(index, 1);
  }

  if(!isNaN(degree_shortest)){
    console.log("test");
    console.log(degree_shortest);
    console.log("test");
    this.rotate(degree_shortest);
  }
}