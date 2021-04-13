function orientation_init() {
  window.addEventListener('deviceorientation', handleOrientation);
}

function checkNull(data) {
  for (key in data) {
    if (data[key] == null) {
      return false;
    }
  }
  return true;
}

let orientationData = null;


function handleOrientation(event) {
  orientationData = {
      "alpha": event.alpha, // In degree in the range [0,360]
      "beta": event.beta, // In degree in the range [-180,180]
      "gamma": event.gamma, // In degree in the range [-90,90]
  };
  console.log(orientationData);
}

function getOrientation() {
  if (checkNull(orientationData)) {
    console.log(orientationData);
    return orientationData;    
  }
  return null;
}