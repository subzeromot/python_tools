- Create RTP stream:
	node ai -r "rtsp://admin:123456aA@192.168.10.121/cam/realmonitor?channel=1&subtype=01"
- Create .sdp file from ai.js
- Play RTP Stream in Gstreamer: 
	gst-launch-1.0 playbin uri="sdp://$PWD/video.sdp"
	gst-launch-1.0 filesrc location=video.sdp ! sdpdemux ! decodebin ! nvvidconv ! video/x-raw\(memory:NVMM\), format=NV12 ! nvoverlaysink

