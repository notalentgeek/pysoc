var pitch_max  = 5000;
var volume_max = 0.1;

function insert_from_url_dt () {
  var dt_value = String(window.location.href).split("?dt=")[1];
  dt_value = (dt_value === undefined) ? undefined : dt_value.split("?")[0];
  if (dt_value !== undefined) {
    $("#dt_value").val(dt_value);
    $("#dt_go_to").click();
  }
  $("#qr_value").blur();
}