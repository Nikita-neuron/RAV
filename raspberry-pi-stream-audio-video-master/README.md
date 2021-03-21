# Deprecation Notice

*NOTE*: This repo has been deprecated and the functionality is now fully absorbed into my other project:

https://github.com/srinathava/raspberry-pi-sleep-monitor

Please be advised that I am no longer actively maintaining this.

# Streaming Live Video and Audio from a Raspberry Pi to a browser

This setup shows how to a stream a live video/audio stream from a Rasbperry Pi to any browser with a pretty low latency. This setup was tested with a Logitech C270 camera connected to a Raspberry Pi 2. 

## Setup
### Upgrade Raspberry Pi
Depending on how old your Raspberry Pi is, you might need to do an apt-get update/upgrade in order to be able to compile Janus (which is not available on apt as of this writing). On a terminal:

    sudo apt-get update
    sudo apt-get upgrade
    
This takes a while, so be patient.

### Setup gstreamer
This should be pretty simple since its available on apt. You can do:

    sudo apt-get install gstreamer-1.0
    
to install it.

### Setup Janus
Janus provides a way to convert an audio-stream obtained from the webcam into a WebRTC stream which is understood by many modern browsers. Unfortunately, Janus is not available as a debian package as of now. Following the instructions from [here](https://www.rs-online.com/designspark/building-a-raspberry-pi-2-webrtc-camera), you need to do:

     sudo aptitude install libmicrohttpd-dev libjansson-dev \
        libnice-dev libssl-dev libsrtp-dev libsrtp2-dev libsofia-sip-ua-dev \
        libglib2.0-dev libopus-dev libogg-dev libini-config-dev \
        libcollection-dev pkg-config gengetopt libtool automake dh-autoreconf
     cd ~
     mkdir janus && cd janus
     git clone https://github.com/meetecho/janus-gateway.git
     cd janus-gateway
     sh autogen.sh
     ./configure --disable-websockets --disable-data-channels \
        --disable-rabbitmq --disable-docs --disable-mqtt --prefix=/opt/janus
     make
     sudo make install
     sudo make configs

Next modify `/opt/janus/etc/janus/janus.plugin.streaming.cfg` to include the sample from this repo:

     https://github.com/srinathava/raspberry-pi-stream-audio-video/blob/master/janus.plugin.streaming.cfg
     
## Setup nginx

    sudo apt-get install nginx
    
Modify the file `/etc/nginx/sites-enabled/default` to include the lines:

	location ~ ^/~(.+?)(/.*)?$ {
	    alias /home/$1/www$2;
	    autoindex on;
	}

in one of the server sections. Restart nginx

    sudo service nginx restart
         
## Use this repo

Now download this repo

     cd ~
     mkdir www && cd www
     git clone https://github.com/srinathava/raspberry-pi-stream-audio-video.git
     cd raspberry-pi-stream-audio-video
     
Now open three terminals (with this as the pwd) and run the following commands

     # start Janus
     ./start_janus.sh
     # Start mpeg_server.py
     ./mpeg_server.py
     # Start gstreamer
     ./gstream_audio_video.sh
     
NOTE: The order of starting mpeg_server.py and gstreamer is important. 

Now from any other computer in the local network, navigate to:

     http://ip.of.your.rpi/~pi/raspberry-pi-stream-audio-video/streamingtest.html
     
     

     
     




     
