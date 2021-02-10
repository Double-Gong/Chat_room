# import pandas
# import numpy as np
# import matplotlib.pyplot as plt
# import cv2
# import time
#
# from PIL import Image
#
# starttime=time.time()
# img01=plt.imread(r'E:\softstone\chat_room\Chat_room\apps\static\test.png','0')
# print(img01.shape)
# h,w,c=img01.shape
# plt.imsave(r'E:\softstone\chat_room\Chat_room\apps\static\01.png',img01[0:int(h/2),:,:])
# print(time.time()-starttime)
# starttime=time.time()
#
# img02=cv2.imread(r'E:\softstone\chat_room\Chat_room\apps\static\test.png')
# print(img02.shape)
# img02=cv2.cvtColor(img02,cv2.COLOR_BGR2RGB)
# h,w,c=img02.shape
# cv2.imwrite(r'E:\softstone\chat_room\Chat_room\apps\static\02.png',img02[0:int(h/2),:,:])
# print(time.time()-starttime)
#
# # h,w,c=img02.shape
# starttime=time.time()
# img03=Image.open(r'E:\softstone\chat_room\Chat_room\apps\static\test.png')
# print(img03.size)
# w,h=img03.size
# b=min(w,h)
# step=int(b/4)
# order=1
# for i in range(4):
#     for j in range(4):
#         img04=img03.crop((i*step,j*step,(i+1)*step,(j+1)*step))
#         img04.save(r'E:\softstone\chat_room\Chat_room\apps\static\{}-{}.png'.format(i,j))
#
#
# print(time.time()-starttime)

import numpy as np
step=4
choice=range(step**2)

# print(range(step**2))
def get_data():
    data=range(step**2)
    for i in range(step):
        print()
get_data()