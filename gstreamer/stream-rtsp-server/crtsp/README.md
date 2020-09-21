Ref: https://medium.com/@pratik.mungekar/stream-video-using-gstreamer-rtsp-server-ca498f4a54bd
Docker: sudo docker run -d -p 8445:8445 dockerpratik/rtsp-server:v1

=== Recompile ===
# Install
sudo apt-get update
sudo apt-get install -y \
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev wget git vim python3-pip libgstrtspserver-1.0-0 \
    libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-pulseaudio libgstrtspserver-1.0-0

# Build RTSP
wget https://gstreamer.freedesktop.org/src/gst-rtsp-server/gst-rtsp-server-1.4.0.tar.xz
tar -xf gst-rtsp-server-1.4.0.tar.xz
cd gst-rtsp-server-1.4.0
./configure 
make
make check
make install
make installcheck

# Compile the code
gcc -o stream  stream.c  `pkg-config --cflags --libs gstreamer-rtsp-server-1.0`

# Execute
./stream "( filesrc location=$video_location ! qtdemux ! h264parse ! rtph264pay name=pay0 pt=96 )"
