var signalling_server_hostname = "172.20.233.29"
var server_port = "8080"
var signalling_server_address = signalling_server_hostname + ':' + server_port;
var isFirefox = typeof InstallTrigger !== 'undefined';// Firefox 1.0+

var ws = null;
var pc;
var datachannel, localdatachannel;
var audio_video_stream;
var pcConfig = {/*sdpSemantics : "plan-b"*,*/ "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302", "stun:" + signalling_server_hostname + ":3478"]}
    ]};
var pcOptions = {
    optional: [
        // Deprecated:
        //{RtpDataChannels: false},
        //{DtlsSrtpKeyAgreement: true}
    ]
};
var mediaConstraints = {
    optional: [],
    mandatory: {
        OfferToReceiveAudio: true,
        OfferToReceiveVideo: true
    }
};
var remoteDesc = false;

var isPlay = false;

RTCPeerConnection = window.RTCPeerConnection || /*window.mozRTCPeerConnection ||*/ window.webkitRTCPeerConnection;
RTCSessionDescription = /*window.mozRTCSessionDescription ||*/ window.RTCSessionDescription;
RTCIceCandidate = /*window.mozRTCIceCandidate ||*/ window.RTCIceCandidate;
navigator.getUserMedia = navigator.getUserMedia || navigator.mozGetUserMedia || navigator.webkitGetUserMedia || navigator.msGetUserMedia;

function createPeerConnection() {
    try {
        var pcConfig_ = pcConfig;
        pc = new RTCPeerConnection(pcConfig_, pcOptions);
        pc.onicecandidate = onIceCandidate;
        if ('ontrack' in pc) {
            pc.ontrack = onTrack;
        } else {
            pc.onaddstream = onRemoteStreamAdded; // deprecated
        }
        pc.onremovestream = onRemoteStreamRemoved;
        pc.ondatachannel = onDataChannel;
        // console.log("peer connection successfully created!");
    } catch (e) {
        console.error("createPeerConnection() failed");
    }
}

function onDataChannel(event) {
    datachannel = event.channel;

    event.channel.onerror = function (error) {
        console.error("Data Channel Error:", error);
    };

    event.channel.onmessage = function (event) {
        console.log("Got Data Channel Message:", event.data);
    };

    event.channel.onclose = function () {
        datachannel = null;
    };
}

function onIceCandidate(event) {
    if (event.candidate) {
        var candidate = {
            sdpMLineIndex: event.candidate.sdpMLineIndex,
            sdpMid: event.candidate.sdpMid,
            candidate: event.candidate.candidate
        };
        var request = {
            what: "addIceCandidate",
            data: JSON.stringify(candidate)
        };
        ws.send(JSON.stringify(request));
    } else {
        // console.log("End of candidates.");
    }
}

function addIceCandidates() {
    iceCandidates.forEach(function (candidate) {
        pc.addIceCandidate(candidate,
            function () {
                // console.log("IceCandidate added: " + JSON.stringify(candidate));
            },
            function (error) {
                console.error("addIceCandidate error: " + error);
            }
        );
    });
    iceCandidates = [];
}

function onRemoteStreamAdded(event) {
    // console.log("Remote stream added:", event.stream);
    var remoteVideoElement = document.getElementById('remote-video');
    remoteVideoElement.srcObect = event.stream;
}

function onTrack(event) {
    // console.log("Remote track!");
    var remoteVideoElement = document.getElementById('remote-video');
    remoteVideoElement.srcObject = event.streams[0];
}

function onRemoteStreamRemoved(event) {
    var remoteVideoElement = document.getElementById('remote-video');
    remoteVideoElement.srcObject = null;
    remoteVideoElement.src = ''; // TODO: remove
}

function startWEBRTC() {
    if ("WebSocket" in window) {
        document.querySelector(".no_video").style.display = "none";
        document.querySelector(".video-player").style.display = "block";

        document.getElementById('remote-video').classList.add("play-video");
        isPlay = true;

        document.documentElement.style.cursor = 'wait';
        var server = signalling_server_address;

        var protocol = location.protocol === "https:" ? "wss:" : "ws:";
        ws = new WebSocket(protocol + '//' + server + '/stream/webrtc');

        function call(stream) {
            iceCandidates = [];
            remoteDesc = false;
            createPeerConnection();
            if (stream) {
                pc.addStream(stream);
            }
            var request = {
                what: "call",
                options: {
                    force_hw_vcodec: false,
                    vformat: "1280x720 30 fps, kbps min.800 max.4000 start1200",
                    trickle_ice: true
                }
            };
            ws.send(JSON.stringify(request));
            console.log("call(), request=" + JSON.stringify(request));
        }

        ws.onopen = function () {
            // console.log("onopen()");

            audio_video_stream = null;
            // var cast_mic = document.getElementById("cast_mic").checked;
            var cast_mic = false;
            // var cast_tab = document.getElementById("cast_tab") ? document.getElementById("cast_tab").checked : false;
            var cast_tab = false;
            // var cast_camera = document.getElementById("cast_camera").checked;
            var cast_camera = false;
            // var cast_screen = document.getElementById("cast_screen").checked;
            var cast_screen = false;
            // var cast_window = document.getElementById("cast_window").checked;
            var cast_window = false;
            // var cast_application = document.getElementById("cast_application").checked;
            var cast_application = false;
            // var echo_cancellation = document.getElementById("echo_cancellation").checked;
            var echo_cancellation = true;
            var localConstraints = {};
            if (cast_mic) {
                if (echo_cancellation)
                    localConstraints['audio'] = isFirefox ? {echoCancellation: true} : {optional: [{echoCancellation: true}]};
                else
                    localConstraints['audio'] = isFirefox ? {echoCancellation: false} : {optional: [{echoCancellation: false}]};
            } else if (cast_tab) {
                localConstraints['audio'] = {mediaSource: "audioCapture"};
            } else {
                localConstraints['audio'] = false;
            }
            if (cast_camera) {
                localConstraints['video'] = true;
            } else if (cast_screen) {
                if (isFirefox) {
                    localConstraints['video'] = {frameRate: {ideal: 30, max: 30},
                        //width: {min: 640, max: 960},
                        //height: {min: 480, max: 720},
                        mozMediaSource: "screen",
                        mediaSource: "screen"};
                } else {
                    // chrome://flags#enable-usermedia-screen-capturing
                    // document.getElementById("cast_mic").checked = false;
                    localConstraints['audio'] = false; // mandatory for chrome
                    localConstraints['video'] = {'mandatory': {'chromeMediaSource':'screen'}};
                }
            } else if (cast_window)
                localConstraints['video'] = {frameRate: {ideal: 30, max: 30},
                    //width: {min: 640, max: 960},
                    //height: {min: 480, max: 720},
                    mozMediaSource: "window",
                    mediaSource: "window"};
            else if (cast_application)
                localConstraints['video'] = {frameRate: {ideal: 30, max: 30},
                    //width: {min: 640, max: 960},
                    //height:  {min: 480, max: 720},
                    mozMediaSource: "application",
                    mediaSource: "application"};
            else
                localConstraints['video'] = false;

            // var localVideoElement = document.getElementById('local-video');
            if (localConstraints.audio || localConstraints.video) {
                if (navigator.getUserMedia) {
                    navigator.getUserMedia(localConstraints, function (stream) {
                        audio_video_stream = stream;
                        call(stream);
                        localVideoElement.muted = true;
                        localVideoElement.srcObject = stream;
                        localVideoElement.play();
                    }, function (error) {
                        stop();
                        alert("An error has occurred. Check media device, permissions on media and origin.");
                        console.error(error);
                    });
                } else {
                    console.log("getUserMedia not supported");
                }
            } else {
                call();
            }
        };

        ws.onmessage = function (evt) {
            var msg = JSON.parse(evt.data);
            if (msg.what !== 'undefined') {
                var what = msg.what;
                var data = msg.data;
            }

            switch (what) {
                case "offer":
                    pc.setRemoteDescription(new RTCSessionDescription(JSON.parse(data)),
                            function onRemoteSdpSuccess() {
                                remoteDesc = true;
                                addIceCandidates();
                                pc.createAnswer(function (sessionDescription) {
                                    pc.setLocalDescription(sessionDescription);
                                    var request = {
                                        what: "answer",
                                        data: JSON.stringify(sessionDescription)
                                    };
                                    ws.send(JSON.stringify(request));

                                }, function (error) {
                                    alert("Failed to createAnswer: " + error);

                                }, mediaConstraints);
                            },
                            function onRemoteSdpError(event) {
                                alert('Failed to set remote description (unsupported codec on this browser?): ' + event);
                                stop();
                            }
                    );
                    break;

                case "answer":
                    break;

                case "message":
                    alert(msg.data);
                    break;

                case "iceCandidate": // when trickle is enabled
                    if (!msg.data) {
                        // console.log("Ice Gathering Complete");
                        break;
                    }
                    var elt = JSON.parse(msg.data);
                    let candidate = new RTCIceCandidate({sdpMLineIndex: elt.sdpMLineIndex, candidate: elt.candidate});
                    iceCandidates.push(candidate);
                    if (remoteDesc)
                        addIceCandidates();
                    document.documentElement.style.cursor = 'default';
                    break;

                case "iceCandidates": // when trickle ice is not enabled
                    var candidates = JSON.parse(msg.data);
                    for (var i = 0; candidates && i < candidates.length; i++) {
                        var elt = candidates[i];
                        let candidate = new RTCIceCandidate({sdpMLineIndex: elt.sdpMLineIndex, candidate: elt.candidate});
                        iceCandidates.push(candidate);
                    }
                    if (remoteDesc)
                        addIceCandidates();
                    document.documentElement.style.cursor = 'default';
                    break;
            }
        };

        ws.onclose = function (evt) {
            if (pc) {
                pc.close();
                pc = null;
            }
            document.documentElement.style.cursor = 'default';
        };

        ws.onerror = function (evt) {
            alert("An error has occurred!");
            ws.close();
        };

    } else {
        alert("Sorry, this browser does not support WebSockets.");
    }
}

function stop() {
    var remoteVideo = document.getElementById('remote-video');
    if (datachannel) {
        console.log("closing data channels");
        datachannel.close();
        datachannel = null;
    }
    if (audio_video_stream) {
        try {
            if (audio_video_stream.getVideoTracks().length)
                audio_video_stream.getVideoTracks()[0].stop();
            if (audio_video_stream.getAudioTracks().length)
                audio_video_stream.getAudioTracks()[0].stop();
            audio_video_stream.stop(); // deprecated
        } catch (e) {
            for (var i = 0; i < audio_video_stream.getTracks().length; i++)
                audio_video_stream.getTracks()[i].stop();
        }
        audio_video_stream = null;
    }
    remoteVideo.srcObject = null;
    remoteVideo.src = ''; // TODO; remove
    if (pc) {
        pc.close();
        pc = null;
    }
    if (ws) {
        ws.close();
        ws = null;
    }
    document.documentElement.style.cursor = 'default';
    isPlay = false;
}

function start() {
    if (isPlay) {
        stop();
        document.querySelector(".no_video").style.display = "block";
        document.querySelector(".video-player").style.display = "none";
        document.getElementById('remote-video').classList.remove("play-video");
    } else {
        startWEBRTC();
    }
}