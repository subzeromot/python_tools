const net = require("net");
const transform = require("sdp-transform");
const spawn = require("child_process").spawn;
const readline = require("readline");
class FFmpegClient  {
    constructor(o) {
        this.dgram = require('dgram').createSocket("udp6");
        this.rtsp = o.rtsp;
        this.ffmpeg_path = '/usr/bin/ffmpeg';
        this.sdp = null;
    }

    ffmpeg_video_args(){
        /**sử dụng các tham số của ffmpeg để đưa ra các package rtp */
        let ffmpeg_arg = ["-fflags", "nobuffer", "-avioflags", "direct"];
        if (this.rtsp.match(/^rtsp:/)){
            ffmpeg_arg.push("-rtsp_transport", "tcp");
            ffmpeg_arg.push("-i", this.rtsp, "-flags:v", "+global_header+low_delay");
        }
        else ffmpeg_arg.push("-vn");
        ffmpeg_arg.push("-vcodec", "copy");
        ffmpeg_arg.push("-an");
        ffmpeg_arg.push("-f", "rtp", "-pkt_size", "64000", `rtp://127.0.0.1:1234`);
        return ffmpeg_arg;
    }
    ffmpeg_turn_on(){
        const video_args=this.ffmpeg_video_args();
        this.ffmpeg  = spawn(this.ffmpeg_path,video_args);
        console.log(`FFMPEG RUN PID: ${this.ffmpeg.pid}, RTP_PORT: 1234`);
        this.ffmpeg.on("close", (err)=>{
            this.ffmpeg_turn_off(err);
        });
        this.ffmpeg.on("error", (err)=> {
            console.log("eror", `Encoder child error ${err.stack}`);
            this.ffmpeg_turn_off(err);
        });
        this.ffmpeg.stdout.on("data", (data)=> {
            this.str_sdp += data.toString().replace(/\r\n/g, "\n").replace(/\na=tool:[^\n]+\n/, "\na=tool:VSMCDN\n").replace(/\ns=[^\n]+\n/, `
      s='cctv channel'
      `);
            console.log(this.str_sdp);
        });
        let line = readline.createInterface({
            input:  this.ffmpeg.stderr
        });
        line.on("line", function(line) {
           // logger.info(line);
        });
    }
    ffmpeg_restart(err){
        /** Nếu lỗi thì 4e3ms thử lại */
        console.log(`Encoder child error ${err}`);
        setTimeout(this.ffmpeg_turn_on.bind(this),4e3);
    }
    ffmpeg_turn_off(){
        this.ffmpeg.kill('SIGKILL');
    }
}
var argv = require('minimist')(process.argv.slice(2));
let ffmpegClient = new FFmpegClient({'rtsp': argv.r});
ffmpegClient.ffmpeg_turn_on();