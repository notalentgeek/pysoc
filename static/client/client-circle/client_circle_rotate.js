ClientCircle.prototype.Rotate = function(_degree){

    this.degreeTarget = _degree;
    this.time = 0;
    ClientCircleListRotate();

};
ClientCircle.prototype.RotateAuto = function(){

    var degreeShortest;
    for(var i = 0; i < degreeTargetList.length; i ++){

        if(degreeShortest === undefined){ degreeShortest = degreeTargetList[i]; }
        if(Math.abs(this.degreeCurrent - degreeTargetList[i]) <= degreeShortest){ degreeShortest = degreeTargetList[i]; }


    }

    var index = degreeTargetList.indexOf(degreeShortest);
    if(index > -1){ degreeTargetList.splice(index, 1); }
    this.Rotate(degreeShortest);

};