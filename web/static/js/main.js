var socket = io();

import {start} from "./vr.js"

const vrButton    = document.querySelector(".vr_button");
const webglviewer = document.querySelector("#webglviewer");
const video       = document.querySelector("#videoremote");
const noVR        = document.querySelector(".no-vr");
const signals     = document.querySelectorAll(".signal-img");

var loaded        = false;
var playVR        = false;
var gn            = null;

const signalsSVG  = {
  "signal-upleft": null,
  "signal-upright": null,
  "signal-left": null,
  "signal-right": null,
  "signal-down": null
}

function getDeviceType() {
  // get device type
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

orientation_init();

vrButton.addEventListener('click', () => {
  // orientationsend_selection();
  // run vr
  if (!video.classList.contains("play-video")) {
    alert("Run the video");
  } else {
    console.log("Run VR");
    webglviewer.style.display = "block";
    noVR.style.display = "none";
    
    start();
    if (getDeviceType() == "mobile") {
      orientation_init();
    }
    playVR = true;
  }
});

let sensorsSystemData = {
    "memory": {
        "memoryFree":       3343,
        "memoryTotal":      4196,
        "memoryPercent":    19
    },
    "disk": {
        "diskFree":         4,
        "diskTotal":        5,
        "diskPercent":      6
    },
    "cpu":                  7,
    "temperature":          8
};

let motorsSystemData = {
    "memory": {
        "memoryFree":       9,
        "memoryTotal":      10,
        "memoryPercent":    11
    },
    "disk": {
        "diskFree":         12,
        "diskTotal":        13,
        "diskPercent":      14
    },
    "cpu":                  15,
    "temperature":          16
};

set_system_data({
    "sensors": sensorsSystemData,
    "motors": motorsSystemData
});

function set_system_data(systemData) {
  // show system data
    for (let device in systemData) {
      let data = systemData[device];

      for (let key in data) {
        if (typeof(data[key]) == "object") {
          for (let k in data[key]) {
            document.querySelector(`.${device}-${k}`).innerHTML = data[key][k];
          }        
        } else {
          document.querySelector(`.${device}-${key}`).innerHTML = data[key];
        }
      }
    }
}

var distance = {
  "upleft": 200,
  "upright": 300,
  "down": 400,
  "left": 100,
  "right": 50
}

signals.forEach((sign) => {
  sign.addEventListener('load', () => {
    signalsSVG[sign.classList[1]] = sign.getSVGDocument();
                
    loaded = true;

    console.log(distance);

    setUltrasonicData(distance);
  });
});

function setUltrasonicData(distance) {
  // show ultrasonic data
  const maxDistance = 400;
  if (loaded) {
    for(var key in distance) {
      if (signalsSVG[`signal-${key}`] != null) {
        let signalSVG = signalsSVG[`signal-${key}`];
        let signalSVGComponents = signalSVG.querySelectorAll('path[id^="_"]');

        signalSVGComponents.forEach(signal => {
          signal.style.display = "block";
        });

        let signalDistance = maxDistance / signalSVGComponents.length;
        let signalCount = ~~(distance[key] / signalDistance);

        for (let i = signalSVGComponents.length - 1; i > signalCount; i--) {
          signalSVGComponents[i].style.display = "none";
        }
      }  
    }
  }
}


// let keys = {
//     'w': false,
//     'a': false,
//     's': false,
//     'd': false
// }

// function update_motors() {
// 	console.log('update', keys)
// 	socket.emit('keys', keys)
// }

// document.addEventListener('keydown', (event) => {
//     if (!(event.key in keys)) {
//         return
//     }
//     let needs_update = !keys[event.key]
//     keys[event.key] = true
//     if (needs_update) {
//         update_motors()
//     }
// })
// document.addEventListener('keyup', (event) => {
//     if (!(event.key in keys)) {
//         return
//     }
//     keys[event.key] = false
//     update_motors()
// })

socket.on('systemData', function(data) {
  // get system data
  let name = data.name;
  let sensorsSystemData;
  let motorsSystemData;
  delete data.name;

  if (name == "raspberryPIMotors") sensorsSystemData = data;
  if (name == "raspberryPISensors") motorsSystemData = data;

  set_system_data({
    "sensors": motorsSystemData,
    "motors": sensorsSystemData
  });
});

socket.on('ultrasonic', data => {
  // get ultrasonic data
  delete data.name;
  setUltrasonicData(data);
});

function sendOrientation() {
  let orientation_value = getOrientation();
  if (orientation_value === null) return;

  socket.emit('gyroscopeData', orientation_value);
}

function update()
{
  sendOrientation();

  let gamepad_value = getGamepadIfChanged();
	if (gamepad_value === null) {
		return;
	}
  socket.emit('joystick', gamepad_value);
}

function loop()
{
	requestAnimationFrame(loop);
	update();
}

loop();
