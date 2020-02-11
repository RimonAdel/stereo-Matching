# stereo-Matching
This repo implements and tests some simple stereo algorithms discussed in computer vision for undergradates class. In each case the script will take two images Il and Ir (a left and a right image) and compute the horizontal disparity (ie., shift) of pixels along each scanline. This is the so-called baseline stereo case, where the images are taken with a forward-facing camera, and the translation between cameras is along the horizontal axis.

**may part in this project was implementing stereo-Matching using dynamic programming.**

### how to Run the script
  1- to run the dynamic programming part $python stereo_Matching_DB.py <path_for_left_image> <path_for_right_image> 
  (i.e. $python stereo_Matching_DB.py images/left2.png images/right2.png)\
  
  2 to run the block_Matching part $python stereo_Matching_DB.py <path_for_left_image> <path_for_right_image> <window_size>
  (i.e. $python block_Matching.py tsukuba_l.png tsukuba_R.png 9)
 
