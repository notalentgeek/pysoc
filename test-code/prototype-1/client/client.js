var clientList = [];
var simulateClientList = [];

var tableClientName = "client_name";
var simulateLatestTimeZone = "europe-amsterdam";

function Client(_name, _simulate){

    this.name = _name;
    this.simulate = _simulate;

    if(this.simulate){ simulateClientList.push(this); }
    else{ clientList.push(this); }

    this.clientCircle;
    this.clientCircleColor = INTRGB(HashCode(this.name));

    //console.log(this.clientCircleColor);

    this.online = false;
    this.onlineChance = 1.0;

    this.latestAmountFace = 0;
    this.latestAmountPitch = 0;
    this.latestAmountVolume = 0;
    this.latestIRCodeClientCircle = [];
    this.latestIRCodeClientName = [];
    this.latestIRCodeClientNameRaw;

    this.latestYear;
    this.latestMonth;
    this.latestDay;
    this.latestHour;
    this.latestMinute;
    this.latestSecond;
    this.latestTimeZone;

    this.tableCam = tableClientName + "_cam";
    this.tableIR = tableClientName + "_ir";
    this.tableMic = tableClientName + "_mic";

}
Client.prototype.constructor = Client;