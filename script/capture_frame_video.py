import numpy as np 
import cv2 
import sys

def CaptureFrame(video_url):
	print(video_url)
	cap = cv2.VideoCapture(video_url)


	pre_name = video_url.split('/')[-1].split('.')[0]
	print(pre_name)

	# Initialize frame counter
	cnt = 0

	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret==True:
			cv2.imshow('frame',frame)

			k = cv2.waitKey(20)

			if k == ord('c'):
				fileName = "/media/dannv5/DATA/Video/data_test_traffic/" + pre_name + "_" + str(cnt) + ".jpg"
				cv2.imwrite(fileName, frame)

			if k == ord('q'):
				break
								
		else:
			break

		cnt+=1

	cap.release()
	cv2.destroyAllWindows()

def main():
	video_url = sys.argv[1]
	print(video_url)

	CaptureFrame(video_url)


if __name__ == "__main__":
    main()