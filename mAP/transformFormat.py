import numpy as np
import pandas as pd
import cv2




name_class = 'person'

def transformPredicted(input_file, output_file, name_class):
    # imput format  -> (One file)       <id_frame> <left> <right> <top> <bottom> <confidence>
    # output format -> (N_frame Files)  <class_name> <confidence> <left> <top> <right> <bottom>

    np_imput = np.genfromtxt( input_file,delimiter=';')

    number_of_frames = int(np.max(np_imput[:,0]))

    for n in range(number_of_frames):
        predicts = np_imput[ np.where(np_imput[:,0] == n+1) ]

        #change the order
        predicts = predicts[:,[0,5,1,3,2,4]]

        predicts = pd.DataFrame(predicts)

        predicts.iloc[:,0] = predicts.iloc[:,0].astype(str) 
        predicts.iloc[:,0] = name_class
        
        predicts.to_csv('predicted/'+output_file+str(n+1)+'.txt', sep=' ', index=False, header=False)


def transformGroundTruth(input_file, output_file, name_class):
    # imput format  -> (One file)       <id_frame> <id_person> <left> <top> <width> <height> <conf> <x> <y> <z>
    # output format -> (N_frame Files)  <class_name> <left> <top> <right> <bottom>

    np_imput = np.genfromtxt( input_file,delimiter=',')
    np_imput = np.delete(np_imput, [1,6,7,8,9], axis=1)


    number_of_frames = int(np.max(np_imput[:,0]))

    for n in range(number_of_frames):
        predicts = np_imput[ np.where(np_imput[:,0] == n+1) ]

        aux = predicts[:,:5]
        aux[:,3] = predicts[:,1]+predicts[:,3]
        aux[:,4] = predicts[:,2]+predicts[:,4]
        predicts = aux
        del(aux)

        predicts = pd.DataFrame(predicts)

        predicts.iloc[:,0] = predicts.iloc[:,0].astype(str) 
        predicts.iloc[:,0] = name_class
        
        predicts.to_csv('ground-truth/'+output_file+str(n+1)+'.txt', sep=' ', index=False, header=False)

def video_to_images(input_file, output_file, name_class):
        
        cap = cv2.VideoCapture(input_file)
        success,frame = cap.read()
        count = 1
        while success:
                cv2.imwrite('images/'+output_file + str(count) + '.jpg', frame)     # save frame as JPEG file      
                success,frame = cap.read()
                count += 1

# ---------------------------GROUNT TRUTH--------------------------------

output_file = 'image_'

path_imput = ''
input_file = path_imput + 'MOC.txt'

#transformGroundTruth(input_file, output_file, name_class)

print('Finished - GROUNT TRUTH')
#----------------------------PREDICTION-------------------------------

output_file = 'image_'

path_imput = '../Object-detection/outputs/'
input_file = path_imput + 'output.csv'

transformPredicted(input_file, output_file, name_class)

print('Finished - PREDICTION')

#----------------------------GET IMAGES-------------------------------

output_file = 'image_'

path_imput = '../Object-detection/inputs/'
input_file = path_imput + 'MOC.mp4'

#video_to_images(input_file, output_file, name_class)

print('Finished - GET IMAGES')