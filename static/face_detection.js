var face_value = 0;
function face_detection_onload () {
  var video = document.getElementById("video");
  var face_detection = new tracking.ObjectTracker("face");
  face_detection.setInitialScale(4);
  face_detection.setStepSize(2);
  face_detection.setEdgesDensity(0.1);

  tracking.track("#video", face_detection, { camera:true });

  face_detection.on("track", function (e) {
    face_value = e.data.length;
    document.getElementById("face_detected_value").innerHTML = face_value;
  });
}