
import os 
import sys
  
# Function to rename multiple files 
# README: rename all file .png in folder to [dst_path + dst_prefix + count + dst_extend_type]

def main(): 
	src_path = "/home/subzero/Documents/HandData/five"
	dst_path = "/home/subzero/Documents/HandData/five"
	dst_prefix = "five"
	dst_extend_type = ".png"
	count = 0

	files = []
	for r, d, f in os.walk(src_path):
	    for file in f:
	        if '.png' in file:
	            files.append(os.path.join(r, file))

	for filename in files:
		print("filename: ", filename)
		dst = dst_prefix + str(count) + dst_extend_type
		src = filename 
		dst = dst_path + "/" + dst 
          
		os.rename(src, dst) 
		count+=1
  
if __name__ == '__main__': 
    main() 
