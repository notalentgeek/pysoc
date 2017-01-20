for(var i = 0; i < simulateClientNameIRCodeList.length; i ++){

    var clientTemporary = new Client(
        simulateClientNameIRCodeList[i],
        true
    );
    new ClientCircle(clientTemporary, 180);

    //console.log(clientTemporary);
    //console.log(clientTemporary.clientName);
    //console.log(clientTemporary.clientIRCode);
    //console.log(clientTemporary.DebugShowLatest());

}
SimulateDetermineDegreeTargetList(simulateClientCircleList.length);
for(var i = 0; i < simulateClientCircleList.length; i ++){

    simulateClientCircleList[i].RotateAuto();

}

setInterval(function(){

    //console.log("1 second just passed");
    //console.log(focus());
    //console.log(receivedData);
    //if(receivedData !== null && receivedData !== undefined){ console.log(receivedData[0]["pitch"] + " " + receivedData[0]["volume"]); }

    socket.emit("latestInputRequest");

    if(focus()){

        if(receivedData !== null && receivedData !== undefined){

            // Set all `clientList[x].online` into `false`.
            for(var i = 0; i < clientList.length; i ++){

                clientList[i].latestIRCodeClientNameRaw = null;
                clientList[i].online = false;

            }
            console.log(receivedData);
            for(var i = 0; i < receivedData.length; i ++){

                //console.log(receivedData[i]);
                //console.log(typeof(receivedData[i]));

                // Check if there is a client object with this
                // name in the `clientList` if not then make
                // a new one.
                var clientName = String(receivedData[i]["client_name"]);
                var clientTemporary;
                //console.log(clientName);
                for(var j = 0; j < clientList.length; j ++){

                    console.log("client exist");

                    if(clientList[j].name == clientName){

                        clientTemporary = clientList[j];
                        clientTemporary.online = true;
                        break;

                    }

                }
                if(clientTemporary === null || clientTemporary === undefined){


                    console.log("client does not exist")

                    DetermineDegreeTargetList(clientCircleList.length + 1);
                    for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }
                    clientTemporary = new Client(clientName, false);
                    new ClientCircle(clientTemporary, degreeTargetList[0]).RotateAuto();

                    console.log(clientTemporary);

                }

                for(var j = 0; j < clientList.length; j ++){

                    console.log(clientList[j]);

                    if(!clientList[j].online){


                        clientList[j].AddLatest();
                        clientList[j].clientCircle.willBeDeleted = true;

                    }

                }

                //console.log(clientList);

                var amountFace = Number(receivedData[i]["faces"]);
                clientTemporary.latestAmountFace = amountFace;
                //console.log(amountFace);

                var irCodeClientNameRaw = (String(receivedData[i]["ir_code"]) == "undefined") ? null : String(receivedData[i]["ir_code"]);
                clientTemporary.latestIRCodeClientNameRaw = irCodeClientNameRaw;
                //console.log(irCodeClientNameRaw);

                var amountPitch = Number(receivedData[i]["pitch"]);
                clientTemporary.latestAmountPitch = amountPitch;
                console.log(amountPitch);

                var amountVolume = Number(receivedData[i]["volume"]);
                clientTemporary.latestAmountVolume = amountVolume;
                //console.log(amountVolume);

                console.log(clientList);

            }
            for(var i = 0; i < clientList.length; i ++){

                clientList[i].AddLatest();

                if(clientList[i].latestIRCodeClientNameRaw !== null && clientList[i].latestIRCodeClientNameRaw !== undefined){

                    //console.log(clientList[i].latestIRCodeClientNameRaw);
                    //console.log(typeof(clientList[i].latestIRCodeClientNameRaw));

                    var latestIRCodeClientNameRawTemporary = clientList[i].latestIRCodeClientNameRaw.split(",");
                    for(var j = 0; j < latestIRCodeClientNameRawTemporary.length; j ++){

                        clientList[i].latestIRCodeClientName.push(latestIRCodeClientNameRawTemporary[j]);

                        var clientTemporary;
                        for(var k = 0; k < clientList.length; k ++){

                            if(clientList[k].name == latestIRCodeClientNameRawTemporary[j]){

                                clientTemporary = clientList[k];
                                break;

                            }

                        }

                        clientList[i].latestIRCodeClientCircle.push(clientTemporary.clientCircle);

                    }

                }

            }

            //DetermineDegreeTargetList(clientCircleList.length);
            //for(var i = 0; i < clientCircleList.length; i ++){ clientCircleList[i].RotateAuto(); }

            d3.selectAll(".real-circle").remove();
            d3.selectAll(".real-line").remove();

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
                                .attr("class", "real-line")
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
                                .attr("class", "real-circle")
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
            DetermineDegreeTargetList(clientCircleList.length);
            for(var j = 0; j < clientCircleList.length; j ++){ clientCircleList[j].RotateAuto(); }

            receivedData = null;

        }

        var currentDate = new Date();

        for(var i = 0; i < simulateClientList.length; i ++){

            simulateClientList[i].SimulateCheckOnline();

        }

        for(var i = 0; i < simulateClientList.length; i ++){

            if(!simulateClientList[i].online && simulateClientList[i].clientCircle !== null){

                simulateClientList[i].clientCircle.willBeDeleted = true;
                SimulateDetermineDegreeTargetList(simulateClientCircleList.length);
                for(var j = 0; j < simulateClientCircleList.length; j ++){ simulateClientCircleList[j].RotateAuto(); }

            }
            else if(simulateClientList[i].online && simulateClientList[i].clientCircle == null){

                SimulateDetermineDegreeTargetList(simulateClientCircleList.length + 1);
                for(var j = 0; j < simulateClientCircleList.length; j ++){ simulateClientCircleList[j].RotateAuto(); }
                new ClientCircle(simulateClientList[i], simulateDegreeTargetList[0]).RotateAuto();

            }

            simulateClientList[i].Simulate(currentDate);
            //console.log(simulateClientList[i].DebugShowLatest());
            d3.selectAll(".simulate-circle").remove();
            d3.selectAll(".simulate-line").remove();

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
                            .attr("class", "simulate-line")
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
                            .attr("class", "simulate-circle")
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