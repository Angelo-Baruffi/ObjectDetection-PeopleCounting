

import matplotlib.pyplot as plt

plt.ion()
for i in range(100):
    x = range(i)
    y = range(i)
    # plt.gca().cla() # optionally clear axes
    plt.plot(x, y)
    plt.title(str(i))
    plt.draw()
    plt.pause(0.1)











exit()
import numpy as np

im_width = 320
im_height = 320

boxes = np.array([[[3.08453500, 1.13429725, 9.95616257, 7.75868893],
  [6.58643723, 7.94705749, 9.75090384, 2.76296526],
  [6.99952364, 7.10584968, 9.84597325, 2.23881513],
  [1.15719587, 2.84510851, 9.82112646, 5.48157454]]])

scores = np.array([[0.09751247,0.09135819,0.0832195,0.07824795]])

classes=np.array([[ 1,  1, 60,  1]])



indexs = np.where(scores[0] > 0.5)
print(indexs, 'First Step')
if(len(indexs[0])):


    indexs = np.array([index if result==1 else -1 for index, result in enumerate(classes[0][indexs])])
    #Tem os indexs que sao pessoas que passaram. Tem indexs nulos
    indexs = indexs[np.where(indexs >= 0)]
    print(indexs, 'Second Step')


    boxes = boxes[0][indexs]
    result = []
    for box in boxes:
        (ymin, xmin, ymax, xmax) = box
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                        ymin * im_height, ymax * im_height)
        result.append([left, right, top, bottom])

    print(result)