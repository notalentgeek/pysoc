for(var i = 0; i < simulateClientNameIRCodeList.length; i ++){

    var clientTemporary = new Client(
        simulateClientNameIRCodeList[i],
        true
    );
    new ClientCircle(clientTemporary, 180);

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
    //console.log(clientCircleList);
    console.log(receivedData);
    //if(receivedData !== null && receivedData !== undefined){ console.log(receivedData[0]["pitch"] + " " + receivedData[0]["volume"]); }

    socket.emit("latestInputRequest");

    if(focus()){

        if(receivedData !== null && receivedData !== undefined){

            d3.selectAll(".real-circle").remove();
            d3.selectAll(".real-line").remove();

            // Set all `clientList[x].online` into `false`.
            // As well as to set `clientList[x].latestIRCodeClientNameRaw`
            // to null.
            for(var i = 0; i < clientList.length; i ++){

                clientList[i].latestIRCodeClientNameRaw = null;
                clientList[i].online                    = false;

            }

            //console.log(receivedData);

            // Check all received data.
            for(var i = 0; i < receivedData.length; i ++){

                // Temporary variable for current received
                // client.
                var clientReceived = null;

                //console.log(receivedData[i])
                //console.log(typeof(receivedData[i]))

                // Check if there is a client list with the same
                // name in the `receivedData[i]`.
                var clientReceivedName                = String(receivedData[i]["client_name"]);
                var clientReceivedAmountFace          = Number(receivedData[i]["faces"]);
                var clientReceivedAmountPitch         = Number(receivedData[i]["pitch"]);
                var clientReceivedAmountVolume        = Number(receivedData[i]["volume"]);
                var clientReceivedIrCodeClientNameRaw = (String(receivedData[i]["ir_code"]) == "undefined") ? null : String(receivedData[i]["ir_code"]);

                //console.log(clientReceived + " " + clientReceivedName)

                for(var j = 0; j < clientList.length; j ++){

                    // In this case there is already a client listed
                    // in the clientList array. This means that this
                    // received client used to be online in this
                    // local session.

                    //console.log(clientList[j].name + " " + clientReceivedName);
                    //console.log(clientList[j].name == clientReceivedName);

                    if(clientList[j].name == clientReceivedName){

                        // Assign the found client into
                        // `clientReceived`. And mark its
                        // `online` status into `true`.

                        console.log(clientReceivedName);

                        clientReceived                           = clientList[j];
                        clientReceived.latestAmountFace          = clientReceivedAmountFace
                        clientReceived.latestAmountPitch         = clientReceivedAmountPitch
                        clientReceived.latestAmountVolume        = clientReceivedAmountVolume
                        clientReceived.latestIRCodeClientNameRaw = clientReceivedIrCodeClientNameRaw
                        clientReceived.online                    = true;
                        clientReceived.AddLatest();
                        if(
                            clientReceived.latestIRCodeClientNameRaw !== null &&
                            clientReceived.latestIRCodeClientNameRaw !== undefined
                        ){

                            for(var k = 0; k < clientReceived.latestIRCodeClientNameRaw.length; k ++){

                                clientReceived.latestIRCodeClientName.push(clientReceived.latestIRCodeClientNameRaw[k]);

                                var clientTemporary;
                                for(var l = 0; l < clientList.length; l ++){

                                    if(clientList[l].name == clientReceived.latestIRCodeClientNameRaw[k]){

                                        clientTemporary = clientList[l];
                                        break;

                                    }

                                }

                                if(
                                    clientTemporary.clientCircle !== null &&
                                    clientTemporary.clientCircle !== undefined
                                ){

                                    clientReceived.latestIRCodeClientCircle.push(clientTemporary.clientCircle);
                                    clientReceived.latestIRCodeClientName.push(clientReceived.latestIRCodeClientNameRaw[k]);

                                }

                            }

                        }

                        break;

                    }

                }

                //console.log(i);
                //console.log(clientReceived);
                //console.log(clientReceived === undefined);
                //console.log(clientReceived === null || clientReceived === undefined);

                // This will happen if the client is completely new in
                // this local session.
                if(
                    clientReceived === null ||
                    clientReceived === undefined
                ){

                    //console.log("new client")

                    clientReceived                           = new Client(clientReceivedName, false);
                    clientReceived.latestAmountFace          = clientReceivedAmountFace
                    clientReceived.latestAmountPitch         = clientReceivedAmountPitch
                    clientReceived.latestAmountVolume        = clientReceivedAmountVolume
                    clientReceived.latestIRCodeClientNameRaw = clientReceivedIrCodeClientNameRaw
                    clientReceived.online                    = true;
                    clientReceived.AddLatest();
                    if(
                        clientReceived.latestIRCodeClientNameRaw !== null &&
                        clientReceived.latestIRCodeClientNameRaw !== undefined
                    ){

                        for(var j = 0; j < clientReceived.latestIRCodeClientNameRaw.length; j ++){

                            var clientTemporary;
                            for(var k = 0; k < clientList.length; k ++){

                                if(clientList[k].name == clientReceived.latestIRCodeClientNameRaw[j]){

                                    clientTemporary = clientList[k];
                                    break;

                                }

                            }

                            if(
                                clientTemporary.clientCircle !== null &&
                                clientTemporary.clientCircle !== undefined
                            ){

                                clientReceived.latestIRCodeClientCircle.push(clientTemporary.clientCircle);
                                clientReceived.latestIRCodeClientName.push(clientReceived.latestIRCodeClientNameRaw[j]);

                            }

                        }

                    }

                    //console.log("test");
                    //console.log(clientReceived);

                }

            }

            for(var i = 0; i < clientList.length; i ++){

                if(
                    !clientList[i].online &&
                    (
                        clientList[i].clientCircle !== null ||
                        clientList[i].clientCircle !== undefined
                    )
                ){

                    console.log(clientList[i].name)
                    clientList[i].clientCircle.willBeDeleted = true;

                }

                // After that check if the current
                // inspected client has its `clientCircle`.
                if(
                    clientList[i].online &&
                    (
                        clientList[i].clientCircle === null ||
                        clientList[i].clientCircle === undefined
                    )
                ){

                    DetermineDegreeTargetList(clientCircleList.length + 1);
                    for(var j = 0; j < clientCircleList.length; j ++){

                        if(clientCircleList[j].client.online){

                            clientCircleList[j].RotateAuto();

                        }

                    }

                    new ClientCircle(clientList[i], degreeTargetList[0]).RotateAuto();

                }

            }

            DetermineDegreeTargetList(clientCircleList.length);
            for(var i = 0; i < clientCircleList.length; j ++){

                if(clientCircleList[i].client.online){

                    clientCircleList[i].RotateAuto();

                }

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