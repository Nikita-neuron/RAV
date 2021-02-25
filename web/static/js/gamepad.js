

function deepCompare() {
    // FROM https://stackoverflow.com/a/1144249
    var i, l, leftChain, rightChain;

    function compare2Objects(x, y) {
        var p;

        // remember that NaN === NaN returns false
        // and isNaN(undefined) returns true
        if (isNaN(x) && isNaN(y) && typeof x === 'number' && typeof y === 'number') {
            return true;
        }

        // Compare primitives and functions.     
        // Check if both arguments link to the same object.
        // Especially useful on the step where we compare prototypes
        if (x === y) {
            return true;
        }

        // Works in case when functions are created in constructor.
        // Comparing dates is a common scenario. Another built-ins?
        // We can even handle functions passed across iframes
        if ((typeof x === 'function' && typeof y === 'function') ||
            (x instanceof Date && y instanceof Date) ||
            (x instanceof RegExp && y instanceof RegExp) ||
            (x instanceof String && y instanceof String) ||
            (x instanceof Number && y instanceof Number)) {
            return x.toString() === y.toString();
        }

        // At last checking prototypes as good as we can
        if (!(x instanceof Object && y instanceof Object)) {
            return false;
        }

        if (x.isPrototypeOf(y) || y.isPrototypeOf(x)) {
            return false;
        }

        if (x.constructor !== y.constructor) {
            return false;
        }

        if (x.prototype !== y.prototype) {
            return false;
        }

        // Check for infinitive linking loops
        if (leftChain.indexOf(x) > -1 || rightChain.indexOf(y) > -1) {
            return false;
        }

        // Quick checking of one object being a subset of another.
        // todo: cache the structure of arguments[0] for performance
        for (p in y) {
            if (y.hasOwnProperty(p) !== x.hasOwnProperty(p)) {
                return false;
            }
            else if (typeof y[p] !== typeof x[p]) {
                return false;
            }
        }

        for (p in x) {
            if (y.hasOwnProperty(p) !== x.hasOwnProperty(p)) {
                return false;
            }
            else if (typeof y[p] !== typeof x[p]) {
                return false;
            }

            switch (typeof (x[p])) {
                case 'object':
                case 'function':

                    leftChain.push(x);
                    rightChain.push(y);

                    if (!compare2Objects(x[p], y[p])) {
                        return false;
                    }

                    leftChain.pop();
                    rightChain.pop();
                    break;

                default:
                    if (x[p] !== y[p]) {
                        return false;
                    }
                    break;
            }
        }

        return true;
    }

    if (arguments.length < 1) {
        return true; //Die silently? Don't know how to handle such case, please help...
        // throw "Need two or more arguments to compare";
    }

    for (i = 1, l = arguments.length; i < l; i++) {

        leftChain = []; //Todo: this can be cached
        rightChain = [];

        if (!compare2Objects(arguments[0], arguments[i])) {
            return false;
        }
    }

    return true;
}

function bidirect_object(o) {
    for (key in o) {
        value = o[key]
        if (value in o) {
            console.log('key clash', key, value)
        }
        console.log(key, value)
        o[value] = key
    }
    return o
}

let GAMEPAD_BUTTONS = bidirect_object([
    "br", // Правые кнопки
    "rr", // 
    "lr", //
    "tr", //__________________________
    "lb", // Кнопки сзади
    "rb", // 
    "lt", //
    "rt", //__________________________
    "cl", // Кнопки в центре
    "cr", //__________________________
    "lstick", // Кнопки НАЖАТИЯ стиков
    "rstick", // _____________________
    "tl", // Левые кнопки
    "bl", // 
    "ll", //
    "rl", //__________________________
    "cc", // Самая центральная кнопка
])



let gamepad = null
window.addEventListener("gamepadconnected", function(e) {
    gamepad = e.gamepad
    console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
        e.gamepad.index, e.gamepad.id,
        e.gamepad.buttons.length, e.gamepad.axes.length, e);
});
window.addEventListener('gamepaddisconnected', function(e) {
    gamepad = null
})
function getGamepadSticks() {
    if (gamepad === null) {
        return null
    }
    let axes = gamepad.axes
    return {
        'left': [axes[0], axes[1]],
        'right': [axes[2], axes[3]]
    }
}
function getGamepadButtons() {
    if (gamepad === null) {
        return null
    }
    let buttons = {}
    for (const [i, btn] of gamepad.buttons.entries()) {
        buttons[GAMEPAD_BUTTONS[i]] = {'value': btn.value, 'pressed': btn.pressed}
    }
    let axes = gamepad.axes
    return buttons
}
function getGamepadValues() {
    if (gamepad === null) {
        return null
    }
    return {
        'buttons': getGamepadButtons(),
        'sticks': getGamepadSticks()
    }
}
function getGamepadIfChanged() {
    let gamepad_values = getGamepadValues()
    if (!deepCompare(gamepad_values, this.last_values)) {
        this.last_values = gamepad_values
        return gamepad_values
    }
    return null
}
