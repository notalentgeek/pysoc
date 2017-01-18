Client.prototype.SimulateAddLatestInput = function(){

    this.SimulateAddLatestInputCam();
    this.SimulateAddLatestInputIR();
    this.SimulateAddLatestInputMic();

};
Client.prototype.SimulateAddLatestInputCam = function(){

    this.latestAmountFace = 0;
    for(var i = 0; i < simulateClientList.length; i ++){

        if(
            (simulateClientList[i].name != this.name) &&
            (simulateClientList[i].online)
        ){

            //console.log(simulateClientList[i].name);
            this.latestAmountFace ++;
            //console.log(simulateClientList[i].name);

        }


   }

};
Client.prototype.SimulateAddLatestInputIR = function(){

    //console.log("test");

    this.latestIRCodeClientName = [];
    this.latestIRCodeClientCircle = [];

    //this.clientCircle.gLatestIRCodeClientLine = simulateD3SVG.append("g")
    //    .attr("id", "gLatestIRCodeClientLine" + this.client.clientName);

    for(var i = 0; i < simulateClientList.length; i ++){

        /*
        console.log("=========================");
        console.log(simulateClientList[i].name + " " + this.name);
        console.log(simulateClientList[i].name != this.name);
        console.log(simulateClientList[i].online);
        console.log(
            (simulateClientList[i].name != this.name) &&
            (simulateClientList[i].online)
        );
        console.log("=========================");
        */

        if(
            (simulateClientList[i].clientCircle !== null && simulateClientList[i].clientCircle !== undefined) &&
            (simulateClientList[i].name != this.name) &&
            (simulateClientList[i].online)
        ){

            this.latestIRCodeClientName.push(simulateClientList[i].name);
            this.latestIRCodeClientCircle.push(simulateClientList[i].clientCircle);
            //this.latestIRCodeClientName.push(simulateClientList[i].clientIRCode);
            //console.log(simulateClientList[i].clientCircle);

        }

    }

    //console.log(this.latestIRCodeClientName);
    //console.log(this.latestIRCodeClientCircle);
    //console.log(this.clientCircle.cX + " " + this.latestIRCodeClientCircle[0].cX);
    //console.log(this.clientCircle.cY + " " + this.latestIRCodeClientCircle[0].cY);
    //console.log(this.latestIRCodeClientLine);

};
Client.prototype.SimulateAddLatestInputMic = function(){

    this.latestAmountPitch = (Math.random()*10000.0).toFixed(3);
    this.latestAmountVolume = (Math.random()*0.01).toFixed(3);

    //console.log(this.clientCircle !== null && this.clientCircle !== undefined);
    //console.log(this.clientCircle);

    if(this.clientCircle !== null && this.clientCircle !== undefined){

        var fillTem = ShadeRGBColor(
            "rgb(" + HexRGB(this.clientCircleColor).r + ", " + HexRGB(this.clientCircleColor).g + ", " + HexRGB(this.clientCircleColor).b + ")",
            simulateLinearScalePitchFill(this.latestAmountPitch)
        );
        this.clientCircle.radius = simulateLinearScaleVolume(this.latestAmountVolume);

        this.clientCircle.circle.transition().attr("r", this.clientCircle.radius).style("fill", fillTem).duration(100);

    }

};