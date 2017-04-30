$("#qr_activate").click(function () {
  $("#qr_activate").html("active");
  $("#qr_activate").addClass("glowing");
  init_qr_code();
  client_recording = true;
});

$("#qr_deactivate").click(function () {
  $("#qr_activate").html("activate");
  $("#qr_activate").removeClass("glowing");
  client_recording = false;
});

$("#qr_generate").click(function () {
  init_qr_code();
});

$("#qr_value")
  .keypress(function (e) {
    if (e.keyCode == 13) { // If ENTER just pressed down.
      init_qr_code();
    }
  })
  .on("blur", function () {
    init_qr_code();
  });