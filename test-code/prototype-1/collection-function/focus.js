var focus = (function(){

    var key = {

        hidden: "visibilitychange",
        mozHidden: "mozvisibilitychange",
        msHidden: "msvisibilitychange",
        webkitHidden: "webkitvisibilitychange"

    };
    var keyEvent;
    var keyState;

    for(keyState in key){

        if(keyState in document){

            keyEvent = key[keyState];
            break;

        }

    }

    return function(_callback){

        if(_callback){

            document.addEventListener(keyEvent, _callback);

        }
        return !document[keyState];

    }

})();