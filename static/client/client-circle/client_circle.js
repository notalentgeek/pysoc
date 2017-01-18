var clientCircleList = [];
var clientCircleRadius = d3DimensionSmallest/24;
var clientCircleRadiusBiggest = d3DimensionSmallest/12;
var linearScalePitch;

var degreeTargetList = [];
var simulateDegreeTargetList = [];

var simulateLinearScaleVolume = d3.scaleLinear()
    .domain([0.001, 0.05])
    .range([clientCircleRadius, clientCircleRadiusBiggest]);
var simulateLinearScalePitchFill = d3.scaleLinear()
    .domain([200, 5000])
    .range([0, 0.9]);

// Global function.
function ClientCircleListRotate(){

    d3.selectAll(".circle").remove();
    d3.selectAll(".line").remove();

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
                        .on("end", ClientCircleListRotate);

                }
                else{

                    clientCircleList[i].circle
                        .transition()
                        .attr("cx", clientCircleList[i].cX)
                        .attr("cy", clientCircleList[i].cY)
                        .duration(0.1)
                        .on("end", ClientCircleListRotate);

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
                        .on("end", ClientCircleListRotate);

                }
                else{

                    clientCircleList[i].circle
                        .transition()
                        .attr("cx", clientCircleList[i].cX)
                        .attr("cy", clientCircleList[i].cY)
                        .duration(0.1)
                        .on("end", ClientCircleListRotate);

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
                        .on("end", ClientCircleListRotate);

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
                    .on("end", ClientCircleListRotate);

            }
            else{

                var clientCircleTemp = clientCircleList[i];

                clientCircleList[i].circle.remove();

                var index = clientCircleList.indexOf(clientCircleList[i]);
                if(index > -1){ clientCircleList.splice(index, 1); }

                clientCircleTemp.client.clientCircle = null;
                clientCircleTemp.client = null;
                delete clientCircleTemp;

                DetermineDegreeTargetList(clientCircleList.length);
                for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }

            }

        }

    }

}

function DetermineDegreeTargetList(_length){

    // Determine the target list.
    simulateDegreeTargetList = [];
    for(var i = 0; i < _length; i ++){

        var degreeTargetTemporary = (((i/_length) * 360) + 180)%360;
        simulateDegreeTargetList.push(degreeTargetTemporary);

    }

    degreeTargetList = [];
    for(var i = 0; i < degreeTargetList.length; i ++){

        var degreeTargetTemporary = (((i/degreeTargetList.length) * 360) + 180)%360;
        simulateDegreeTargetList.push(degreeTargetTemporary);

    }

}

function ClientCircle(_client, _degree){

    //console.log("test");

    clientCircleList.push(this);

    this.client = _client;
    this.degreeCurrent = _degree;

    this.client.clientCircle = this;

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

    this.radius = clientCircleRadius;
    this.circle = simulateD3SVG.append("circle")
        .attr("cx", this.cX)
        .attr("cy", this.cY)
        .attr("id", this.client.clientName)
        .attr("r", this.radius)
        .attr(
            "transform",
            "translate(" + d3DimensionTranslate.x + ", " + d3DimensionTranslate.y + ")"
        )
        .style("fill", this.client.clientCircleColor)
        .style("opacity", 0)
        .style("stroke", this.client.clientCircleColor)
        .style("stroke-width", 5);

    //console.log(this.circle);
    //console.log(this.cX);
    //console.log(this.cY);
    //console.log(this.radius);

}
ClientCircle.prototype.constructor = ClientCircle;