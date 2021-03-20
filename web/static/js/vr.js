import * as THREE from './libs/three.module.js';
import { StereoEffect } from './libs/StereoEffect.js';
// import { VRButton } from './js/VRButton.js';

  var scene,
      camera, 
      renderer,
      element,
      container,
      effect
  function start() {
    init();
    animate();
  }

      function init() {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(90, window.innerWidth / window.innerHeight, 0.001, 700);
        camera.position.set(0, 15, 0);
        scene.add(camera);

        renderer = new THREE.WebGLRenderer();
        renderer.xr.enabled = true;
        element = renderer.domElement;
        container = document.getElementById('webglviewer');
        container.appendChild(element);

        effect = new StereoEffect(renderer);
        effect.setSize( window.innerWidth, window.innerHeight );

        element.addEventListener('click', fullscreen, false);

        const video = document.querySelector("#remote-video");
        video.play();

        const texture     = new THREE.VideoTexture( video );

        var cameraPlane = new THREE.PlaneGeometry(512, 512);

        var cameraMesh = new THREE.Mesh(cameraPlane, new THREE.MeshBasicMaterial({
          color: 0xffffff, opacity: 1, map: texture
        }));
        cameraMesh.position.z = -200;

        scene.add(cameraMesh);

        // document.body.appendChild( VRButton.createButton( renderer ) );

        // animate();
      }

      function resize() {
        var width = container.offsetWidth;
        var height = container.offsetHeight;

        camera.aspect = width / height;
        camera.updateProjectionMatrix();

        renderer.setSize(width, height);
        effect.setSize(width, height);
      }

      function update(dt) {
        resize();

        camera.updateProjectionMatrix();
      }

      function animate() {
        renderer.setAnimationLoop( render );
      }

      function render(dt) {
        effect.render(scene, camera);
      }

      function fullscreen() {
        if (container.requestFullscreen) {
          container.requestFullscreen();
        } else if (container.msRequestFullscreen) {
          container.msRequestFullscreen();
        } else if (container.mozRequestFullScreen) {
          container.mozRequestFullScreen();
        } else if (container.webkitRequestFullscreen) {
          container.webkitRequestFullscreen();
        }
      }

export {start}