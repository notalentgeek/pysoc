for(var i = 0; i < simulateClientNameIRCodeList.length; i ++){

    var client = new Client(
        simulateClientNameIRCodeList[i],
        true
    );
    clientCircle = new ClientCircle(client, 180);

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

        socket.emit("latestInputRequest");

        if(receivedData !== null && receivedData !== undefined){

            // Set all `clientList[x].online` into `false`.
            for(var i = 0; i < clientList.length; i ++){

                clientList[i].online = false;

            }
            //console.log(receivedData);
            for(var i = 0; i < receivedData.length; i ++){

                console.log(receivedData[i]);
                console.log(typeof(receivedData[i]));

                // Check if there is a client object with this
                // name in the `clientList` if not then make
                // a new one.
                var clientName = String(receivedData[i]["client_name"]);
                var clientTemporary;
                console.log(clientName);
                for(var i = 0; i < clientList.length; i ++){

                    if(clientList[i].clientName == clientName){

                        clientTemporary = clientList[i];
                        clientTemporary.online = true;
                        break;

                    }

                }
                if(clientTemporary !== null && clientTemporary !== undefined){

                    clientTemporary = new Client();

                }

                console.log(receivedData[i]["faces"]);
                console.log(receivedData[i]["ir_code"]);
                console.log(receivedData[i]["pitch"]);
                console.log(receivedData[i]["volume"]);

            }

            receivedData = null;

        }

        var currentDate = new Date();

        for(var i = 0; i < simulateClientList.length; i ++){

            simulateClientList[i].SimulateCheckOnline();

        }

        for(var i = 0; i < simulateClientList.length; i ++){

            if(!simulateClientList[i].online && simulateClientList[i].clientCircle !== null){

                simulateClientList[i].clientCircle.willBeDeleted = true;
                DetermineDegreeTargetList(clientCircleList.length);
                for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }

            }
            else if(simulateClientList[i].online && simulateClientList[i].clientCircle == null){

                if(clientCircleList.length == 0){

                    new ClientCircle(simulateClientList[i], 0);
                    DetermineDegreeTargetList(clientCircleList.length);
                    for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }

                }
                else if(clientCircleList.length == 1){

                    new ClientCircle(simulateClientList[i], 180);
                    DetermineDegreeTargetList(clientCircleList.length);
                    for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }

                }
                else{

                    DetermineDegreeTargetList(clientCircleList.length + 1);
                    for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }
                    new ClientCircle(simulateClientList[i], simulateDegreeTargetList[0]);

                }

            }

            simulateClientList[i].Simulate(currentDate);
            //console.log(simulateClientList[i].DebugShowLatest());
            d3.selectAll(".circle").remove();
            d3.selectAll(".line").remove();

        }

        for(var i = 0; i < simulateClientList.length; i ++){

            for(var j = 0; j < simulateClientList[i].latestIRCodeClientCircle.length; j ++){

                if(simulateClientList[i].clientCircle !== null && simulateClientList[i].clientCircle !== undefined){

                    if(
                        (simulateClientList[i].clientCircle.degreeCurrent == simulateClientList[i].clientCircle.degreeTarget) &&
                        (simulateClientList[i].latestIRCodeClientCircle[j].degreeCurrent == simulateClientList[i].latestIRCodeClientCircle[j].degreeTarget)
                    ){

                        var cX1 = Number(simulateClientList[i].clientCircle.circle.attr("cx"));
                        var cY1 = Number(simulateClientList[i].clientCircle.circle.attr("cy"));
                        var cX2 = Number(simulateClientList[i].latestIRCodeClientCircle[j].circle.attr("cx"));
                        var cY2 = Number(simulateClientList[i].latestIRCodeClientCircle[j].circle.attr("cy"));
                        var r1 = simulateClientList[i].clientCircle.radius;
                        var r2 = simulateClientList[i].latestIRCodeClientCircle[j].radius;

                        var radian = Math.atan2(cY2 - cY1, cX2 - cX1);

                        var x1 = cX1 + (r1 * Math.cos(radian));
                        var y1 = cY1 + (r1 * Math.sin(radian));
                        var x2 = cX2 - (r2 * Math.cos(radian));
                        var y2 = cY2 - (r2 * Math.sin(radian));

                        //console.log("test");

                        simulateD3SVG.append("line")
                            .attr("class", "line " + simulateClientList[i].name + " " + simulateClientList[i].latestIRCodeClientCircle[j].client.name)
                            .attr("x1", x1)
                            .attr("y1", y1)
                            .attr("x2", x2)
                            .attr("y2", y2)
                            .attr(
                                "transform",
                                "translate(" + d3DimensionTranslate.x + ", " + d3DimensionTranslate.y + ")"
                            )
                            .style("opacity", 0.5)
                            .style("stroke", simulateClientList[i].clientCircleColor)
                            .style("stroke-width", 5);

                        simulateD3SVG.append("circle")
                            .attr("class", "circle " + simulateClientList[i].name + " " + simulateClientList[i].latestIRCodeClientCircle[j].client.name)
                            .attr("cx", x2)
                            .attr("cy", y2)
                            .attr("r", 5)
                            .attr(
                                "transform",
                                "translate(" + d3DimensionTranslate.x + ", " + d3DimensionTranslate.y + ")"
                            )
                            .style("fill", simulateClientList[i].clientCircleColor)
                            .style("stroke", "no-stroke");

                        //this.latestIRCodeClientLine.push(line);

                    }

                }

            }

        }

    }

}, 1000);