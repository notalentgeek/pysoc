ClientCircle.prototype.Rotate = function(_degree){

    this.degreeTarget = _degree;
    this.time = 0;
    ClientCircleListRotate();

};
ClientCircle.prototype.RotateAuto = function(){

    var degreeShortest;
    for(var i = 0; i < simulateDegreeTargetList.length; i ++){

        if(degreeShortest === undefined){ degreeShortest = simulateDegreeTargetList[i]; }
        if(Math.abs(this.degreeCurrent - simulateDegreeTargetList[i]) <= degreeShortest){ degreeShortest = simulateDegreeTargetList[i]; }


    }

    var index = simulateDegreeTargetList.indexOf(degreeShortest);
    if(index > -1){ simulateDegreeTargetList.splice(index, 1); }
    this.Rotate(degreeShortest);

};