var presence_value = 0;
var qr_recorded_array = []; // Array of dictionary of recorded users.
var qr_scanner = null; // QR scanner JavaScript object.
var qr_still = 120; // In second.

function presence_detection_onload () {
  qr_scanner = new Instascan.Scanner({
    backgroundScan:true,
    video:document.getElementById("video")
  });

  Instascan.Camera.getCameras()
    .catch(function (e) {
      console.log(e);
    })
    .then(function (c) { // `c` is an array of available web cams.
      if (c.length) {
        qr_scanner.start(c[0]); // Use the first available web cam in the array.
      }
      else {
        console.error("no web cam found");
      }
    });
}

function presence_detection_loop () {
  var result = qr_scanner.scan();

  // Decrease `countdown` value.
  increase_value_in_array_of_dictionary(
    qr_recorded_array,
    "countdown",
    -1
  );
  remove_value_lower_equal_than_in_array_of_dictionary(
    qr_recorded_array,
    "countdown",
    0
  );

  // Assign new `client_name` or reset `countdown` value.
  if (result) {
    // Check if `result.content` already listed as `client_name`.
    var qr_recorded = search_value_in_array_of_dictionary(
      qr_recorded_array,
      "client_name",
      result.content
    );
    if (qr_recorded) {
      // If `result.content` is already in the array reset the `countdown`.
      qr_recorded["countdown"] = qr_still;
    }
    else {
      qr_recorded = {};
      qr_recorded["client_name"] = result.content;
      qr_recorded["countdown"] = qr_still;
      qr_recorded_array.push(qr_recorded);
    }
  }

  // Print into `document.getElementById()`.
  presence_value = print_value_in_array_of_dictionary(
    qr_recorded_array,
    "client_name"
  );
  if (presence_value) {
    document.getElementById("presence_value").innerHTML = presence_value;
  }
}

function increase_value_in_array_of_dictionary (_array, _key, _inc) {
  for (var i = 0; i < _array.length; i ++) {
    if (_array[i].hasOwnProperty(_key)) {
      _array[i][_key] += _inc;
    }
  }
}

function print_value_in_array_of_dictionary (_array, _key) {
  var print = "";
  for (var i = 0; i < _array.length; i ++) {
    if (_array[i].hasOwnProperty(_key)) {
      print += _array[i][_key] + ", ";
    }
  }

  // If `print` valid remove two last characters.
  if (print) {
    print = print.substring(0, print.length - 2);
  }

  return print;
}

function remove_value_lower_equal_than_in_array_of_dictionary (_array, _key, _value) {
  for (var i = 0; i < _array.length; i ++) {
    if (_array[i].hasOwnProperty(_key)) {
      if (_array[i][_key] <= _value) {
        _array.splice(i, 1);
      }
    }
  }
}

function search_value_in_array_of_dictionary (_array, _key, _value) {
  for (var i = 0; i < _array.length; i ++) {
    if (_array[i].hasOwnProperty(_key)) {
      if (_array[i][_key] == _value) {
        return _array[i];
      }
    }
  }

  return null;
}