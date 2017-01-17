// Function to change "true" into "true ".
function FixBoolString(_bool){

    var string = _bool;
    if(_bool == true){ string = " " + string }
    return string

}
// Function to change x into "0x" for x lower than 10.
function FixDateString(_int){

    var string = _int;
    if(_int < 10){ string = "0" + string }
    return string

}
// Function to list all element in a string
// into proper string.
function FixListString(_list){

    var string = _list;
    if(_list.length == 0){ string = "[]"; }
    else{

        string = "[";
        for(_l of _list){ string = string + _l + ", "; }
        string = string.slice(0, -2);
        string = string + "]";


    }
    return string;

}