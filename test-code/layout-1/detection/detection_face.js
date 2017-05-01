var detection_face           = new tracking.ObjectTracker("face");
var video                    = document.getElementById("video");
var face_value               = 0;
var video_track_face         = document.getElementById("video_track_face");
var video_track_face_context = video_track_face.getContext("2d");

function init_detection_face () {
  detection_face.setInitialScale(4);
  detection_face.setStepSize(2);
  detection_face.setEdgesDensity(0.1);

  tracking.track("#video", detection_face, { camera:true });

  detection_face.on("track", function (e) {
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