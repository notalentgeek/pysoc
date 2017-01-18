Client.prototype.AddLatest = function(){

    this.AddLatestInputMic();

};
Client.prototype.AddLatestInputMic = function(){

    if(this.clientCircle !== null && this.clientCircle !== undefined){

        var fillTem = ShadeRGBColor(
            "rgb(" + HexRGB(this.clientCircleColor).r + ", " + HexRGB(this.clientCircleColor).g + ", " + HexRGB(this.clientCircleColor).b + ")",
            simulateLinearScalePitch(this.latestAmountPitch)
        );
        this.clientCircle.radius = simulateLinearScaleVolume(this.latestAmountVolume);

        //console.log("=========================");
        //console.log(this.latestAmountPitch);
        //console.log(this.latestAmountVolume);
        //console.log(this.clientCircle.radius + " " + clientCircleRadiusBiggest);
        //console.log("=========================");

        this.clientCircle.radius = this.clientCircle.radius > clientCircleRadiusBiggest ? clientCircleRadiusBiggest : this.clientCircle.radius;

        this.clientCircle.circle.attr("r", this.clientCircle.radius).style("fill", fillTem);

    }

};