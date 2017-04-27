var face_detection           = new tracking.ObjectTracker("face");
var video                    = document.getElementById("video");
var face_value               = 0;
var video_track_face         = document.getElementById("video_track_face");
var video_track_face_context = video_track_face.getContext("2d");

function face_detection_onload () {
  face_detection.setInitialScale(4);
  face_detection.setStepSize(2);
  face_detection.setEdgesDensity(0.1);

  tracking.track("#video", face_detection, { camera:true });

  face_detection.on("track", function (e) {
    face_value = e.data.length;
    document.getElementById("face_value").innerHTML = face_value;

    video_track_face_context.clearRect(0, 0, video_track_face.width, video_track_face.height);
    e.data.forEach(function (r) {
      video_track_face_context.lineWidth = 5;
      video_track_face_context.strokeStyle = "rgba(255, 0, 0, 0.5)";
      video_track_face_context.strokeRect(video_track_face.width - r.width - r.x, r.y, r.width, r.height);
    });
  });
}