var client_name = "";
var client_name_default = "client_test";
var client_recording = false;
function qr_code_generate () {
  var qr_code_height = document.getElementById("qr_code").clientHeight;
  var qr_code_width = document.getElementById("qr_code").clientWidth;
  var qr_code_dimension = qr_code_height < qr_code_width ? qr_code_height : qr_code_width;
  var qr_value = document.getElementById("qr_value");

  // If value in `qr_value` is invalid.
  if (!qr_value.value) {
    qr_value.focus();
    return;
  }

  // If value in `qr_value` is valid.
  // Remove previous QR code.
  $("#qr_code > canvas").remove();
  $("#qr_code > img").remove();

  // Set new QR code.
  new QRCode(document.getElementById("qr_code"), {
    height:qr_code_dimension,
    width:qr_code_dimension,
    text:qr_value.value
  });

  client_name = qr_value.value;
}
function qr_code_insert_from_url () {
    var name_value = String(window.location.href).split("?name=")[1];
    name_value = (name_value === undefined) ? undefined : name_value.split("?")[0];
    if (name_value !== undefined) {
      $("#qr_value").val(name_value);
      $("#qr_generate").click();
    }
    else {
      $("#qr_value").val(client_name_default);
      $("#qr_generate").click();
    }
    $("#qr_value").blur();
}