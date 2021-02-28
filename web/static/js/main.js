var socket = io();

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
  // console.log('systemData', data)
})

function update()
{
    let gamepad_value = getGamepadIfChanged()
	if (gamepad_value === null) {
		return
	}
    socket.emit('joystick', gamepad_value)
}

function loop()
{
	requestAnimationFrame(loop);
	update();
}

loop();
