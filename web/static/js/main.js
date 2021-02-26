
var socket = io();

var sensorsMemoryPercent = document.querySelector();
var sensorsMemoryTotal = document.querySelector(".sensors-memory-total");
var sensorsMemoryFree = document.querySelector(".sensors-memory-free");
var sensorsDiskPercent = document.querySelector(".sensors-disk-percent");

let sensorsSystemData = {
    "memory": {
        "memoryFree": ".sensors-memory-percent",
        "memoryTotal": ,
        "memoryPercent":
    },
    "disk": {
        "diskFree": ,
        "diskTotal": ,
        "diskPercent": 
    }
}


let keys = {
    'w': false,
    'a': false,
    's': false,
    'd': false
}

function update_motors() {
	console.log('update', keys)
	socket.emit('keys', keys)
}

document.addEventListener('keydown', (event) => {
    if (!(event.key in keys)) {
        return
    }
    let needs_update = !keys[event.key]
    keys[event.key] = true
    if (needs_update) {
        update_motors()
    }
})
document.addEventListener('keyup', (event) => {
    if (!(event.key in keys)) {
        return
    }
    keys[event.key] = false
    update_motors()
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

// loop();
