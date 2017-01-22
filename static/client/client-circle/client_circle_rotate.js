ClientCircle.prototype.Rotate = function(_degree){

    this.degreeTarget = _degree;
    this.time = 0;

    if(this.client.simulate){ SimulateClientCircleAnimation(); }
    else{ ClientCircleAnimation(); }

};
ClientCircle.prototype.RotateAuto = function(){

    degreeTargetTemp = this.client.simulate ? simulateDegreeTargetList : degreeTargetList;

    var degreeShortest;
    for(var i = 0; i < degreeTargetTemp.length; i ++){

        if(degreeShortest === undefined){ degreeShortest = degreeTargetTemp[i]; }
        if(Math.abs(this.degreeCurrent - degreeTargetTemp[i]) <= degreeShortest){ degreeShortest = degreeTargetTemp[i]; }


    }

    var index = degreeTargetTemp.indexOf(degreeShortest);
    if(index > -1){ degreeTargetTemp.splice(index, 1); }

    console.log(degreeShortest);

    this.Rotate(degreeShortest);

};