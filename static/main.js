for(var i = 0; i < simulateClientNameIRCodeList.length; i ++){

    var client = new Client(
        simulateClientNameIRCodeList[i][0],
        simulateClientNameIRCodeList[i][1]
    );
    clientCircle = new ClientCircle(client, 270);

    //console.log(client);
    //console.log(client.clientName);
    //console.log(client.clientIRCode);
    //console.log(client.DebugShowLatest());

}
DetermineDegreeTargetList(clientCircleList.length);
for(var i = 0; i < clientCircleList.length; i ++){

    clientCircleList[i].RotateAuto();

}

setInterval(function(){

    //console.log("1 second just passed");
    //console.log(focus());

    if(focus()){

        var currentDate = new Date();

        for(var i = 0; i < clientList.length; i ++){

            clientList[i].SimulateCheckOnline();

        }

        for(var i = 0; i < clientList.length; i ++){

            if(!clientList[i].online && clientList[i].clientCircle !== null){

                clientList[i].clientCircle.willBeDeleted = true;
                DetermineDegreeTargetList(clientCircleList.length);
                for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }

            }
            else if(clientList[i].online && clientList[i].clientCircle == null){

                if(clientCircleList.length == 0){

                    new ClientCircle(clientList[i], 0);
                    DetermineDegreeTargetList(clientCircleList.length);
                    for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }

                }
                else if(clientCircleList.length == 1){

                    new ClientCircle(clientList[i], 180);
                    DetermineDegreeTargetList(clientCircleList.length);
                    for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }

                }
                else{

                    DetermineDegreeTargetList(clientCircleList.length + 1);
                    for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }
                    new ClientCircle(clientList[i], degreeTargetList[0]);

                }

            }

            clientList[i].Simulate(currentDate);
            //console.log(clientList[i].DebugShowLatest());
            d3.selectAll(".circle").remove();
            d3.selectAll(".line").remove();

        }

        for(var i = 0; i < clientList.length; i ++){

            for(var j = 0; j < clientList[i].latestIRCodeClientCircle.length; j ++){

                if(clientList[i].clientCircle !== null && clientList[i].clientCircle !== undefined){

                    if(
                        (clientList[i].clientCircle.degreeCurrent == clientList[i].clientCircle.degreeTarget) &&
                        (clientList[i].latestIRCodeClientCircle[j].degreeCurrent == clientList[i].latestIRCodeClientCircle[j].degreeTarget)
                    ){

                        var cX1 = Number(clientList[i].clientCircle.circle.attr("cx"));
                        var cY1 = Number(clientList[i].clientCircle.circle.attr("cy"));
                        var cX2 = Number(clientList[i].latestIRCodeClientCircle[j].circle.attr("cx"));
                        var cY2 = Number(clientList[i].latestIRCodeClientCircle[j].circle.attr("cy"));
                        var r1 = clientList[i].clientCircle.radius;
                        var r2 = clientList[i].latestIRCodeClientCircle[j].radius;

                        var radian = Math.atan2(cY2 - cY1, cX2 - cX1);

                        var x1 = cX1 + (r1 * Math.cos(radian));
                        var y1 = cY1 + (r1 * Math.sin(radian));
                        var x2 = cX2 - (r2 * Math.cos(radian));
                        var y2 = cY2 - (r2 * Math.sin(radian));

                        //console.log("test");

                        d3SVG.append("line")
                            .attr("class", "line " + clientList[i].name + " " + clientList[i].latestIRCodeClientCircle[j].client.name)
                            .attr("x1", x1)
                            .attr("y1", y1)
                            .attr("x2", x2)
                            .attr("y2", y2)
                            .attr(
                                "transform",
                                "translate(" + d3DimensionTranslate.x + ", " + d3DimensionTranslate.y + ")"
                            )
                            .style("opacity", 0.5)
                            .style("stroke", clientList[i].clientCircleColor)
                            .style("stroke-width", 5);

                        d3SVG.append("circle")
                            .attr("class", "circle " + clientList[i].name + " " + clientList[i].latestIRCodeClientCircle[j].client.name)
                            .attr("cx", x2)
                            .attr("cy", y2)
                            .attr("r", 5)
                            .attr(
                                "transform",
                                "translate(" + d3DimensionTranslate.x + ", " + d3DimensionTranslate.y + ")"
                            )
                            .style("fill", clientList[i].clientCircleColor)
                            .style("stroke", "no-stroke");

                        //this.latestIRCodeClientLine.push(line);

                    }

                }

            }

        }

    }

}, 1000);