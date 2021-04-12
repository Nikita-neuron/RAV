import {start} from "./vr.js"

const vrButton = document.querySelector(".vr_button");
const webglviewer = document.querySelector("#webglviewer");
const video = document.querySelector("#videoremote");
const noVR = document.querySelector(".no-vr");

const getDeviceType = () => {
  const ua = navigator.userAgent;
  if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
    return "tablet";
  }
  if (
    /Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(
      ua
    )
  ) {
    return "mobile";
  }
  return "desktop";
};

vrButton.addEventListener('click', () => {
  // console.log(video.isPlay);
  if (!video.classList.contains("play-video")) {
    alert("Run the video");
  } else {
    webglviewer.style.display = "block";
    noVR.style.display = "none";
    start();
  }
});