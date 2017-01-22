var clientCircleList = [];
var simulateClientCircleList = [];

var clientCircleRadius = d3DimensionSmallest/24;
var clientCircleRadiusBiggest = d3DimensionSmallest/12;
var linearScalePitch;

var degreeTargetList = [];
var simulateDegreeTargetList = [];

var simulateLinearScalePitch = d3.scaleLinear()
    .domain([0, 2500])
    .range([0, 0.9]);
var simulateLinearScaleVolume = d3.scaleLinear()
    .domain([0, 0.1])
    .range([clientCircleRadius, clientCircleRadiusBiggest]);

// Global function.
function ClientCircleAnimation(){

    d3.selectAll(".real-circle").remove();
    d3.selectAll(".real-line").remove();

    for(var i = 0; i < clientCircleList.length; i ++){

        // Check if this client circle will be deleted.
        if(!clientCircleList[i].willBeDeleted && clientCircleList[i] !== null && clientCircleList[i] !== undefined){

            // Move the client circle clock wise.
            if(
                (clientCircleList[i].degreeCurrent > clientCircleList[i].degreeTarget) &&
                (clientCircleList[i].degreeSaved > clientCircleList[i].degreeTarget)
            ){

                //console.log(clientCircleList[i]);
                //console.log(clientCircleList[i].cX);
                //console.log(clientCircleList[i].degreeCurrent);
                //console.log(clientCircleList[i].degreeSaved);
                //console.log(clientCircleList[i].degreeTarget);

                var degreeStep = -80;
                //var degreeStep = -1*(Math.abs(clientCircleList[i].degreeSaved - clientCircleList[i].degreeTarget)/100);
                //console.log(clientCircleList[i].cX);

                clientCircleList[i].degreeCurrent = Math.EaseInExpo(clientCircleList[i].time, clientCircleList[i].degreeCurrent, degreeStep, 32*clientCircleList.length);
                clientCircleList[i].cX = mainCircleRadius * Math.cos(Math.Radian(clientCircleList[i].degreeCurrent));
                clientCircleList[i].cY = mainCircleRadius * Math.sin(Math.Radian(clientCircleList[i].degreeCurrent));
                clientCircleList[i].time ++;

                /*
                d3.selectAll(".circle " + clientCircleList[i].client.name).remove();
                d3.selectAll(".line " + clientCircleList[i].client.name).remove();
                for(var j = 0; j < clientCircleList[i].client.latestIRCodeClientCircle.length; j ++){

                    d3.selectAll(".circle " + clientCircleList[i].client.latestIRCodeClientCircle[j].client.name).remove();

                }
                */

                //console.log(clientCircleList[i]);
                //console.log(clientCircleList[i].cX);
                //console.log(clientCircleList[i].cY);
                //console.log(clientCircleList[i].degreeCurrent);
                //console.log(mainCircleRadius);
                //console.log(Math.sin(Math.Radian(clientCircleList[i].degreeCurrent)));

                if(clientCircleList[i].circle.style("opacity") < 1){

                    var opacityStep = Number(clientCircleList[i].circle.style("opacity")) + 0.05;
                    opacityStep = (opacityStep > 1) ? 1 : opacityStep;

                    clientCircleList[i].circle
                        .transition()
                        .attr("cx", clientCircleList[i].cX)
                        .attr("cy", clientCircleList[i].cY)
                        .style("opacity", opacityStep)
                        .duration(0.1)
                        .on("end", ClientCircleAnimation);

                }
                else{

                    clientCircleList[i].circle
                        .transition()
                        .attr("cx", clientCircleList[i].cX)
                        .attr("cy", clientCircleList[i].cY)
                        .duration(0.1)
                        .on("end", ClientCircleAnimation);

                }

            }
            // Move counter clock wise.
            else if(
                (clientCircleList[i].degreeCurrent < clientCircleList[i].degreeTarget) &&
                (clientCircleList[i].degreeSaved < clientCircleList[i].degreeTarget)
            ){

                //console.log(clientCircleList[i]);
                //console.log(clientCircleList[i].cX);
                //console.log(clientCircleList[i].degreeCurrent);
                //console.log(clientCircleList[i].degreeSaved);
                //console.log(clientCircleList[i].degreeTarget);

                var degreeStep = 80;
                //var degreeStep = Math.abs(clientCircleList[i].degreeSaved - clientCircleList[i].degreeTarget)/100;

                clientCircleList[i].degreeCurrent = Math.EaseInExpo(clientCircleList[i].time, clientCircleList[i].degreeCurrent, degreeStep, 32*clientCircleList.length);
                clientCircleList[i].cX = mainCircleRadius * Math.cos(Math.Radian(clientCircleList[i].degreeCurrent));
                clientCircleList[i].cY = mainCircleRadius * Math.sin(Math.Radian(clientCircleList[i].degreeCurrent));
                clientCircleList[i].time ++;

                /*
                d3.selectAll(".circle " + clientCircleList[i].client.name).remove();
                d3.selectAll(".line " + clientCircleList[i].client.name).remove();
                for(var j = 0; j < clientCircleList[i].client.latestIRCodeClientCircle.length; j ++){

                    d3.selectAll(".circle " + clientCircleList[i].client.latestIRCodeClientCircle[j].client.name).remove();

                }
                */

                //console.log(clientCircleList[i].cX);

                if(clientCircleList[i].circle.style("opacity") < 1){

                    var opacityStep = Number(clientCircleList[i].circle.style("opacity")) + 0.05;

                    clientCircleList[i].circle
                        .transition()
                        .attr("cx", clientCircleList[i].cX)
                        .attr("cy", clientCircleList[i].cY)
                        .style("opacity", opacityStep)
                        .duration(0.1)
                        .on("end", ClientCircleAnimation);

                }
                else{

                    clientCircleList[i].circle
                        .transition()
                        .attr("cx", clientCircleList[i].cX)
                        .attr("cy", clientCircleList[i].cY)
                        .duration(0.1)
                        .on("end", ClientCircleAnimation);

                }

            }
            else{

                /*
                d3.selectAll(".circle " + clientCircleList[i].client.name).remove();
                d3.selectAll(".line " + clientCircleList[i].client.name).remove();
                for(var j = 0; j < clientCircleList[i].client.latestIRCodeClientCircle.length; j ++){

                    d3.selectAll(".circle " + clientCircleList[i].client.latestIRCodeClientCircle[j].client.name).remove();

                }
                */

                //console.log(clientCircleList[i]);
                //console.log(clientCircleList[i].cX);

                clientCircleList[i].degreeCurrent = clientCircleList[i].degreeTarget;
                clientCircleList[i].degreeSaved = clientCircleList[i].degreeCurrent;
                clientCircleList[i].cX = mainCircleRadius * Math.cos(Math.Radian(clientCircleList[i].degreeCurrent));
                clientCircleList[i].cY = mainCircleRadius * Math.sin(Math.Radian(clientCircleList[i].degreeCurrent));
                clientCircleList[i].time = 0;

                if(clientCircleList[i] === null || clientCircleList[i] === undefined){ console.log(clientCircleList[i].cX); }

                //console.log(clientCircleList[i].cX);

                if(clientCircleList[i].circle.style("opacity") < 1){

                    var opacityStep = Number(clientCircleList[i].circle.style("opacity")) + 0.05;

                    clientCircleList[i].circle
                        .transition()
                        .attr("cx", clientCircleList[i].cX)
                        .attr("cy", clientCircleList[i].cY)
                        .style("opacity", opacityStep)
                        .duration(0.1)
                        .on("end", ClientCircleAnimation);

                }
                else{

                    clientCircleList[i].circle
                        .transition()
                        .attr("cx", clientCircleList[i].cX)
                        .attr("cy", clientCircleList[i].cY)
                        .duration(0.1);

                }

            }

        }
        else if(clientCircleList[i].willBeDeleted && clientCircleList[i] !== null && clientCircleList[i] !== undefined){

            /*
            d3.selectAll(".circle " + clientCircleList[i].client.name).remove();
            d3.selectAll(".line " + clientCircleList[i].client.name).remove();
            for(var j = 0; j < clientCircleList[i].client.latestIRCodeClientCircle.length; j ++){

                d3.selectAll(".circle " + clientCircleList[i].client.latestIRCodeClientCircle[j].client.name).remove();

            }
            */

            clientCircleList[i].time = 0;

            if(clientCircleList[i].circle.style("opacity") > 0){

                var opacityStep = Number(clientCircleList[i].circle.style("opacity")) - 0.05;

                clientCircleList[i].circle
                    .transition()
                    .style("opacity", opacityStep)
                    .duration(0.1)
                    .on("end", ClientCircleAnimation);

            }
            else{

                var clientCircleTemp = clientCircleList[i];

                clientCircleList[i].circle.remove();

                var index = clientCircleList.indexOf(clientCircleList[i]);
                if(index > -1){ clientCircleList.splice(index, 1); }

                clientCircleTemp.client.clientCircle = null;
                clientCircleTemp.client = null;
                delete clientCircleTemp;

                //SimulateDetermineDegreeTargetList(clientCircleList.length);
                //for(var j = 0; j < clientCircleList.length; j ++){

                //    clientCircleList[j].degreeSaved = clientCircleList[j].degreeCurrent;
                //    clientCircleList[j].RotateAuto();

                //}

            }

        }

    }

}
// Global function.
function SimulateClientCircleAnimation(){

    d3.selectAll(".simulate-circle").remove();
    d3.selectAll(".simulate-line").remove();

    for(var i = 0; i < simulateClientCircleList.length; i ++){

        // Check if this client circle will be deleted.
        if(!simulateClientCircleList[i].willBeDeleted && simulateClientCircleList[i] !== null && simulateClientCircleList[i] !== undefined){

            // Move the client circle clock wise.
            if(
                (simulateClientCircleList[i].degreeCurrent > simulateClientCircleList[i].degreeTarget) &&
                (simulateClientCircleList[i].degreeSaved > simulateClientCircleList[i].degreeTarget)
            ){

                //console.log(simulateClientCircleList[i]);
                //console.log(simulateClientCircleList[i].cX);
                //console.log(simulateClientCircleList[i].degreeCurrent);
                //console.log(simulateClientCircleList[i].degreeSaved);
                //console.log(simulateClientCircleList[i].degreeTarget);

                var degreeStep = -80;
                //var degreeStep = -1*(Math.abs(simulateClientCircleList[i].degreeSaved - simulateClientCircleList[i].degreeTarget)/100);
                //console.log(simulateClientCircleList[i].cX);

                simulateClientCircleList[i].degreeCurrent = Math.EaseInExpo(simulateClientCircleList[i].time, simulateClientCircleList[i].degreeCurrent, degreeStep, 32*simulateClientCircleList.length);
                simulateClientCircleList[i].cX = mainCircleRadius * Math.cos(Math.Radian(simulateClientCircleList[i].degreeCurrent));
                simulateClientCircleList[i].cY = mainCircleRadius * Math.sin(Math.Radian(simulateClientCircleList[i].degreeCurrent));
                simulateClientCircleList[i].time ++;

                /*
                d3.selectAll(".circle " + simulateClientCircleList[i].client.name).remove();
                d3.selectAll(".line " + simulateClientCircleList[i].client.name).remove();
                for(var j = 0; j < simulateClientCircleList[i].client.latestIRCodeClientCircle.length; j ++){

                    d3.selectAll(".circle " + simulateClientCircleList[i].client.latestIRCodeClientCircle[j].client.name).remove();

                }
                */

                //console.log(simulateClientCircleList[i]);
                //console.log(simulateClientCircleList[i].cX);
                //console.log(simulateClientCircleList[i].cY);
                //console.log(simulateClientCircleList[i].degreeCurrent);
                //console.log(mainCircleRadius);
                //console.log(Math.sin(Math.Radian(simulateClientCircleList[i].degreeCurrent)));

                if(simulateClientCircleList[i].circle.style("opacity") < 1){

                    var opacityStep = Number(simulateClientCircleList[i].circle.style("opacity")) + 0.05;
                    opacityStep = (opacityStep > 1) ? 1 : opacityStep;

                    simulateClientCircleList[i].circle
                        .transition()
                        .attr("cx", simulateClientCircleList[i].cX)
                        .attr("cy", simulateClientCircleList[i].cY)
                        .style("opacity", opacityStep)
                        .duration(0.1)
                        .on("end", SimulateClientCircleAnimation);

                }
                else{

                    simulateClientCircleList[i].circle
                        .transition()
                        .attr("cx", simulateClientCircleList[i].cX)
                        .attr("cy", simulateClientCircleList[i].cY)
                        .duration(0.1)
                        .on("end", SimulateClientCircleAnimation);

                }

            }
            // Move counter clock wise.
            else if(
                (simulateClientCircleList[i].degreeCurrent < simulateClientCircleList[i].degreeTarget) &&
                (simulateClientCircleList[i].degreeSaved < simulateClientCircleList[i].degreeTarget)
            ){

                //console.log(simulateClientCircleList[i]);
                //console.log(simulateClientCircleList[i].cX);
                //console.log(simulateClientCircleList[i].degreeCurrent);
                //console.log(simulateClientCircleList[i].degreeSaved);
                //console.log(simulateClientCircleList[i].degreeTarget);

                var degreeStep = 80;
                //var degreeStep = Math.abs(simulateClientCircleList[i].degreeSaved - simulateClientCircleList[i].degreeTarget)/100;

                simulateClientCircleList[i].degreeCurrent = Math.EaseInExpo(simulateClientCircleList[i].time, simulateClientCircleList[i].degreeCurrent, degreeStep, 32*simulateClientCircleList.length);
                simulateClientCircleList[i].cX = mainCircleRadius * Math.cos(Math.Radian(simulateClientCircleList[i].degreeCurrent));
                simulateClientCircleList[i].cY = mainCircleRadius * Math.sin(Math.Radian(simulateClientCircleList[i].degreeCurrent));
                simulateClientCircleList[i].time ++;

                /*
                d3.selectAll(".circle " + simulateClientCircleList[i].client.name).remove();
                d3.selectAll(".line " + simulateClientCircleList[i].client.name).remove();
                for(var j = 0; j < simulateClientCircleList[i].client.latestIRCodeClientCircle.length; j ++){

                    d3.selectAll(".circle " + simulateClientCircleList[i].client.latestIRCodeClientCircle[j].client.name).remove();

                }
                */

                //console.log(simulateClientCircleList[i].cX);

                if(simulateClientCircleList[i].circle.style("opacity") < 1){

                    var opacityStep = Number(simulateClientCircleList[i].circle.style("opacity")) + 0.05;

                    simulateClientCircleList[i].circle
                        .transition()
                        .attr("cx", simulateClientCircleList[i].cX)
                        .attr("cy", simulateClientCircleList[i].cY)
                        .style("opacity", opacityStep)
                        .duration(0.1)
                        .on("end", SimulateClientCircleAnimation);

                }
                else{

                    simulateClientCircleList[i].circle
                        .transition()
                        .attr("cx", simulateClientCircleList[i].cX)
                        .attr("cy", simulateClientCircleList[i].cY)
                        .duration(0.1)
                        .on("end", SimulateClientCircleAnimation);

                }

            }
            else{

                /*
                d3.selectAll(".circle " + simulateClientCircleList[i].client.name).remove();
                d3.selectAll(".line " + simulateClientCircleList[i].client.name).remove();
                for(var j = 0; j < simulateClientCircleList[i].client.latestIRCodeClientCircle.length; j ++){

                    d3.selectAll(".circle " + simulateClientCircleList[i].client.latestIRCodeClientCircle[j].client.name).remove();

                }
                */

                //console.log(simulateClientCircleList[i]);
                //console.log(simulateClientCircleList[i].cX);

                simulateClientCircleList[i].degreeCurrent = simulateClientCircleList[i].degreeTarget;
                simulateClientCircleList[i].degreeSaved = simulateClientCircleList[i].degreeCurrent;
                simulateClientCircleList[i].cX = mainCircleRadius * Math.cos(Math.Radian(simulateClientCircleList[i].degreeCurrent));
                simulateClientCircleList[i].cY = mainCircleRadius * Math.sin(Math.Radian(simulateClientCircleList[i].degreeCurrent));
                simulateClientCircleList[i].time = 0;

                if(simulateClientCircleList[i] === null || simulateClientCircleList[i] === undefined){ console.log(simulateClientCircleList[i].cX); }

                //console.log(simulateClientCircleList[i].cX);

                if(simulateClientCircleList[i].circle.style("opacity") < 1){

                    var opacityStep = Number(simulateClientCircleList[i].circle.style("opacity")) + 0.05;

                    simulateClientCircleList[i].circle
                        .transition()
                        .attr("cx", simulateClientCircleList[i].cX)
                        .attr("cy", simulateClientCircleList[i].cY)
                        .style("opacity", opacityStep)
                        .duration(0.1)
                        .on("end", SimulateClientCircleAnimation);

                }
                else{

                    simulateClientCircleList[i].circle
                        .transition()
                        .attr("cx", simulateClientCircleList[i].cX)
                        .attr("cy", simulateClientCircleList[i].cY)
                        .duration(0.1);

                }

            }

        }
        else if(simulateClientCircleList[i].willBeDeleted && simulateClientCircleList[i] !== null && simulateClientCircleList[i] !== undefined){

            /*
            d3.selectAll(".circle " + simulateClientCircleList[i].client.name).remove();
            d3.selectAll(".line " + simulateClientCircleList[i].client.name).remove();
            for(var j = 0; j < simulateClientCircleList[i].client.latestIRCodeClientCircle.length; j ++){

                d3.selectAll(".circle " + simulateClientCircleList[i].client.latestIRCodeClientCircle[j].client.name).remove();

            }
            */

            simulateClientCircleList[i].time = 0;

            if(simulateClientCircleList[i].circle.style("opacity") > 0){

                var opacityStep = Number(simulateClientCircleList[i].circle.style("opacity")) - 0.05;

                simulateClientCircleList[i].circle
                    .transition()
                    .style("opacity", opacityStep)
                    .duration(0.1)
                    .on("end", SimulateClientCircleAnimation);

            }
            else{

                var clientCircleTemp = simulateClientCircleList[i];

                simulateClientCircleList[i].circle.remove();

                var index = simulateClientCircleList.indexOf(simulateClientCircleList[i]);
                if(index > -1){ simulateClientCircleList.splice(index, 1); }

                clientCircleTemp.client.clientCircle = null;
                clientCircleTemp.client = null;
                delete clientCircleTemp;

                SimulateDetermineDegreeTargetList(simulateClientCircleList.length);
                for(var j = 0; j < simulateClientCircleList.length; j ++){

                    simulateClientCircleList[j].degreeSaved = simulateClientCircleList[j].degreeCurrent;
                    simulateClientCircleList[j].RotateAuto();

                }

            }

        }

    }

}

function DetermineDegreeTargetList(_length){

    // Determine the target list.
    degreeTargetList = [];
    for(var i = 0; i < _length; i ++){

        var degreeTargetTemporary = (((i/_length) * 360) + 180)%360;
        degreeTargetList.push(degreeTargetTemporary);

    }

}
function SimulateDetermineDegreeTargetList(_length){

    // Determine the target list.
    simulateDegreeTargetList = [];
    for(var i = 0; i < _length; i ++){

        var degreeTargetTemporary = (((i/_length) * 360) + 180)%360;
        simulateDegreeTargetList.push(degreeTargetTemporary);

    }

}

function ClientCircle(_client, _degree){

    //console.log("test");

    this.client = _client;
    this.degreeCurrent = _degree;

    if(this.client.simulate){ simulateClientCircleList.push(this); }
    else{ clientCircleList.push(this); }


    this.client.clientCircle = this;

    //console.log(this);
    //console.log(this.client);
    //console.log(this.client.clientCircle);

    this.cX = mainCircleRadius * Math.sin(Math.Radian(this.degreeCurrent));
    this.cY = mainCircleRadius * Math.cos(Math.Radian(this.degreeCurrent));

    //console.log(mainCircleRadius);
    //console.log(mainCircleRadius);
    //console.log(Math.cos(Math.Radian(this.degreeCurrent)));
    //console.log(Math.Radian(this.degreeCurrent));
    //console.log(Math.sin(Math.Radian(this.degreeCurrent)));
    //console.log(this.cX);
    //console.log(this.cY);
    //console.log(this.degreeCurrent);

    this.degreeSaved = this.degreeCurrent;
    this.degreeTarget = this.degreeCurrent;

    this.time = 0;
    this.willBeDeleted = false;

    var mainD3SVG = this.client.simulate ? simulateD3SVG : d3SVG;

    this.radius = clientCircleRadius;
    this.circle = mainD3SVG.append("circle")
        .attr("cx", this.cX)
        .attr("cy", this.cY)
        .attr("id", this.client.clientName)
        .attr("r", this.radius)
        .attr(
            "transform",
            "translate(" + d3DimensionTranslate.x + ", " + d3DimensionTranslate.y + ")"
        )
        .style("fill", this.client.clientCircleColor)
        .style("opacity", 1)
        .style("stroke", this.client.clientCircleColor)
        .style("stroke-width", 5);

    //console.log(this.circle);
    //console.log(this.cX);
    //console.log(this.cY);
    //console.log(this.radius);

}
ClientCircle.prototype.constructor = ClientCircle;