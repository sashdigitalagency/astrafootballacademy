(function () {
  var FRAME_MATCH_TEXT = "Astra United Motion";
  var MIN_SCROLL_DISTANCE = 1.15;
  var frame = null;
  var started = false;

  function clamp(value) {
    return Math.min(1, Math.max(0, value));
  }

  function pageTop(element) {
    var top = 0;
    var node = element;
    while (node) {
      top += node.offsetTop || 0;
      node = node.offsetParent;
    }
    return top;
  }

  function findFrame() {
    if (frame && document.documentElement.contains(frame)) return frame;
    var frames = Array.prototype.slice.call(document.querySelectorAll("iframe"));
    frame = frames.find(function (candidate) {
      var title = candidate.getAttribute("title") || "";
      var name = candidate.getAttribute("name") || "";
      var src = candidate.getAttribute("src") || "";
      return title.indexOf(FRAME_MATCH_TEXT) > -1 ||
        name.indexOf(FRAME_MATCH_TEXT) > -1 ||
        src.indexOf(FRAME_MATCH_TEXT) > -1;
    }) || frames[0] || null;
    if (frame) {
      frame.style.pointerEvents = "none";
    }
    return frame;
  }

  function sendProgress() {
    var target = findFrame();
    if (target && target.contentWindow) {
      var container = target.parentElement || target;
      var sectionTop = pageTop(container);
      var sectionDistance = Math.max(0, container.offsetHeight - window.innerHeight);
      var fallbackDistance = target.offsetHeight * MIN_SCROLL_DISTANCE;
      var distance = Math.max(sectionDistance, fallbackDistance, window.innerHeight * 0.7);
      var progress = clamp((window.scrollY - sectionTop) / distance);
      target.contentWindow.postMessage({
        type: "astra-scroll-progress",
        progress: progress
      }, "*");
    }
  }

  function loop() {
    sendProgress();
    window.requestAnimationFrame(loop);
  }

  function start() {
    if (started) return;
    started = true;
    sendProgress();
    window.requestAnimationFrame(loop);
    window.addEventListener("scroll", sendProgress, { passive: true });
    window.addEventListener("resize", sendProgress);
    window.setInterval(sendProgress, 120);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
