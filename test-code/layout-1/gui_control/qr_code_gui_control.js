$("#qr_activate").click(function () {
  $("#qr_activate").html("active");
  $("#qr_activate").addClass("glowing");
  qr_code_generate();
  client_recording = true;
});

$("#qr_deactivate").click(function () {
  $("#qr_activate").html("activate");
  $("#qr_activate").removeClass("glowing");
  client_recording = false;
});

$("#qr_generate").click(function () {
  qr_code_generate();
});

$("#qr_value")
  .keypress(function (e) {
    if (e.keyCode == 13) { // If ENTER just pressed down.
      qr_code_generate();
    }
  })
  .on("blur", function () {
    qr_code_generate();
  });