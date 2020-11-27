import numpy as np 
import cv2 

video_path = "FaceReg_video_1.mp4"

cap = cv2.VideoCapture(video_path)

# Initialize frame counter
cnt = 0

# Some characteristics from the original video
w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

# Here you can define your croping values
x,y,w,h = 300,0,900,1080

# output
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('result.mp4', fourcc, fps, (w, h))

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret==True:
        crop_frame = frame[y:y+h, x:x+w]

        out.write(crop_frame)
        cv2.imshow('croped',crop_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
