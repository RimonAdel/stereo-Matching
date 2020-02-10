import numpy as np 
import cv2
import threading

SIGMA = 2
SKIPPING_COST = 7
THREADS_NUM = 1


def calc_desparity(point1,point2):
    return float(((int(point1) - int(point2))**2)/(SIGMA**2))

def disparity(imgL,imgR,disparity_map,start_index,end_index):
    print("s=",start_index ,"     end_index",end_index)
    print("range(start_index,end_index)=",range(start_index,end_index))
    for i in range(start_index,end_index):
        line_matrix = [[0 for i in range(len(imgL[0]))] for j in range(len(imgR[0]))]
        M = [[0 for i in range(len(imgL[0]))] for j in range(len(imgR[0]))]
        line_matrix[0][0] = calc_desparity(imgL[i][0],imgR[i][0])
        new_desparity_vector = [0 for i in range(len(imgL[i]))]
        d11 = line_matrix[0][0]
        for j in range(1,len(imgL[0])):
            line_matrix[j][0] = d11 + j * SKIPPING_COST

        for k in range(1,len(imgL[0])):
            line_matrix[0][k] = d11 + k * SKIPPING_COST

        for j in range(1,len(imgL[0])):
            for k in range(1,len(imgL[0])):
                min1 = line_matrix[j-1][k-1] + calc_desparity(imgL[i][j],imgR[i][k])
                min2 = line_matrix[j-1][k] + SKIPPING_COST
                min3 = line_matrix[j][k-1] + SKIPPING_COST
                finalMin = min(min1, min2, min3)
                line_matrix[j][k] = finalMin
                if min1 == finalMin:
                    M[j][k] = 1
                elif min2 == finalMin:
                    M[j][k] = 2
                elif min3 == finalMin:
                    M[j][k] = 3
        
        p = k
        q = k
        desparity = 0
        while p != 0 and q != 0:
            if M[p][q] == 1:
                disparity_map[i][p] = abs(p-q)*15
                p -= 1
                q -= 1
            elif M[p][q] == 2:
                disparity_map[i][p] = 0
                p -= 1
            elif M[p][q] == 3:
                disparity_map[i][p] = 0
                q -= 1


imgL = cv2.imread('images/left2.png',0)  # downscale images for faster processing
imgR = cv2.imread('images/right2.png',0)
disparity_map = imgL.copy()
thread_list = []
covered_range = 0
thread_range = int(len(imgR)/THREADS_NUM)

if thread_range < 20:
    thread_range = 20
    
while covered_range < len(imgR):
    if covered_range + thread_range < len(imgR):
        thread_list.append(threading.Thread(target=disparity,args=(imgL,imgR,disparity_map,covered_range,covered_range+thread_range)))
        covered_range += thread_range
        thread_list[len(thread_list)-1].start()
    else:
        thread_list.append(threading.Thread(target=disparity,args=(imgL,imgR,disparity_map,covered_range,len(imgR))))
        thread_list[len(thread_list)-1].start()
        break
        
for thread in thread_list:
    thread.join()


cv2.imwrite( "1.png", disparity_map)


cv2.imshow('left', imgL)
cv2.imshow('right', imgR)
cv2.imshow('disparity_map', disparity_map)
cv2.waitKey(0)
cv2.destroyAllWindows()
