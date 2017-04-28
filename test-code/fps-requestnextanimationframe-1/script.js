var fps, fpsInterval, startTime, now, then, elapsed;
tracking.trackVideo_ = function(element, tracker) {
  var canvas = document.createElement('canvas');
  var context = canvas.getContext('2d');
  var width;
  var height;

  var resizeCanvas_ = function() {
    width = element.offsetWidth;
    height = element.offsetHeight;
    canvas.width = width;
    canvas.height = height;
  };
  resizeCanvas_();
  element.addEventListener('resize', resizeCanvas_);

  var requestId;
  var requestAnimationFrame_ = function() {
    requestId = window.requestAnimationFrame(function() {
      now = Date.now();
      elapsed = now - then;
      if (elapsed > fpsInterval) {
        then = now - (elapsed % fpsInterval);
        if (element.readyState === element.HAVE_ENOUGH_DATA) {
          try {
            // Firefox v~30.0 gets confused with the video readyState firing an
            // erroneous HAVE_ENOUGH_DATA just before HAVE_CURRENT_DATA state,
            // hence keep trying to read it until resolved.
            context.drawImage(element, 0, 0, width, height);
          } catch (err) {}
          tracking.trackCanvasInternal_(canvas, tracker);
        }
      }
      requestAnimationFrame_();
    });
  };

  var task = new tracking.TrackerTask(tracker);
  task.on('stop', function() {
    window.cancelAnimationFrame(requestId);
  });
  task.on('run', function() {
    fpsInterval = 1000 / 10;
    then = Date.now();
    startTime = then;
    requestAnimationFrame_();
  });
  return task.run();
};