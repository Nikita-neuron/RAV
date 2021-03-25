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

const getDeviceType = () => {
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

vrButton.addEventListener('click', () => {
  // run vr
  if (!video.classList.contains("play-video")) {
    alert("Run the video");
  } else {
    console.log("Run VR");
    webglviewer.style.display = "block";
    noVR.style.display = "none";
    orientationsend_selection();
    start();
    playVR = true;
  }
});

// window.addEventListener("deviceorientation", event => {
//   // get and send orientation data
//   console.log({
//     "absolute": event.absolute,
//     "alpha":    event.alpha,
//     "beta":     event.beta,
//     "gamma":    event.gamma
//   })
//   if (playVR) {
//     socket.emit("gyroscopeData", {
//       "absolute": event.absolute,
//       "alpha":    event.alpha,
//       "beta":     event.beta,
//       "gamma":    event.gamma
//     });
//   }
// }, true);

function handleOrientation(event) {
  var data = {
    "do": {
      "alpha": event.alpha.toFixed(1), // In degree in the range [0,360]
      "beta": event.beta.toFixed(1), // In degree in the range [-180,180]
      "gamma": event.gamma.toFixed(1), // In degree in the range [-90,90]
      "absolute": event.absolute
    }
  };
    console.log(data);
    socket.emit("gyroscopeData", data);
}

function handleGyronorm(data) {
  // Process:
  // data.do.alpha    ( deviceorientation event alpha value )
  // data.do.beta     ( deviceorientation event beta value )
  // data.do.gamma    ( deviceorientation event gamma value )
  // data.do.absolute ( deviceorientation event absolute value )

  // data.dm.x        ( devicemotion event acceleration x value )
  // data.dm.y        ( devicemotion event acceleration y value )
  // data.dm.z        ( devicemotion event acceleration z value )

  // data.dm.gx       ( devicemotion event accelerationIncludingGravity x value )
  // data.dm.gy       ( devicemotion event accelerationIncludingGravity y value )
  // data.dm.gz       ( devicemotion event accelerationIncludingGravity z value )

  // data.dm.alpha    ( devicemotion event rotationRate alpha value )
  // data.dm.beta     ( devicemotion event rotationRate beta value )
  // data.dm.gamma    ( devicemotion event rotationRate gamma value )
  if (playVR) {
    socket.emit("gyroscopeData", data);
  }
}

function orientationsend_selection() {
  console.log("gyronorm.js library found!");
  if (gn) {
    gn.setHeadDirection();
    return;
  }
  try {
    gn = new GyroNorm();
  } catch (e) {
    console.log(e);
    return;
  }
  var args = {
    frequency: 60, // ( How often the object sends the values - milliseconds )
    gravityNormalized: true, // ( If the gravity related values to be normalized )
    orientationBase: GyroNorm.GAME, // ( Can be GyroNorm.GAME or GyroNorm.WORLD. gn.GAME returns orientation values with respect to the head direction of the device. gn.WORLD returns the orientation values with respect to the actual north direction of the world. )
    decimalCount: 1, // ( How many digits after the decimal point will there be in the return values )
    logger: null, // ( Function to be called to log messages from gyronorm.js )
    screenAdjusted: false            // ( If set to true it will return screen adjusted values. )
  };
  gn.init(args).then(function () {
    gn.start(handleGyronorm);
    gn.setHeadDirection(); // only with gn.GAME
  }).catch(function (e) {
    console.log("DeviceOrientation or DeviceMotion might not be supported by this browser or device");
    window.addEventListener('deviceorientation', handleOrientation, true);
  });
  if (!gn) {
    window.addEventListener('deviceorientation', handleOrientation, true);
    console.log("gyronorm.js library not found, using defaults");
  }
}

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
  sign.onload = () => {
    signalsSVG[sign.classList[1]] = sign.getSVGDocument();
                
    loaded = true;

    setUltrasonicData(distance);
  }
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

function update()
{
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
