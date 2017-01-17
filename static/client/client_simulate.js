Client.prototype.SimulateAddCurrentLatestDate = function(_date){

    this.latestYear = _date.getFullYear();
    this.latestMonth = _date.getMonth() + 1;
    this.latestDay = _date.getDay();
    this.latestHour = _date.getHours();
    this.latestMinute = _date.getMinutes();
    this.latestSecond = _date.getSeconds();

};
Client.prototype.SimulateCheckOnline = function(){

    var random = Math.random();
    if(random < this.onlineChance){

        if(!this.online){ this.online = true; this.onlineChance = 1.0; }
        else{ this.onlineChance -= 0.005; }

    }
    else if(random > this.onlineChance){

        if(this.online){ this.online = false; this.onlineChance = 0.0; }
        else{ this.onlineChance += 0.005; }

    }

};
Client.prototype.Simulate = function(_date){

    if(this.online){

        this.SimulateAddCurrentLatestDate(_date);
        this.SimulateAddLatestInput();

    }

};