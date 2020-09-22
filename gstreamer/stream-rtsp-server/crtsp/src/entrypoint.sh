# compile code
gcc -o stream  stream.c  `pkg-config --cflags --libs gstreamer-rtsp-server-1.0`

# execute code
./stream "( filesrc location=/home/vsmart/Videos/GR2.mp4 ! qtdemux ! h265parse ! rtph265pay name=pay0 pt=96 )"
