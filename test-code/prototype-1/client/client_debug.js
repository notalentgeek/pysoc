Client.prototype.DebugShowLatest = function(){

    return (
        FixBoolString(this.online) + "-" +

        this.latestYear +
        FixDateString(this.latestMonth) +
        FixDateString(this.latestDay) + "-" +
        FixDateString(this.latestHour) +
        FixDateString(this.latestMinute) +
        FixDateString(this.latestSecond) + "-" +
        simulateLatestTimeZone + "-" +

        this.irCode + "-" +
        this.name + "-" +

        this.latestAmountFace + "-" +
        this.latestAmountPitch + "-" +
        this.latestAmountVolume + "-" +
        FixListString(this.latestIRCodeClientName)
    )

};