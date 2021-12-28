import os,cv2

import tensorflow as tf

import numpy as np

model = tf.keras.models.load_model('model.h5')

img = cv2.imread(os.path.join('gtsrb','40', '00000_00010.ppm'))
img = cv2.resize(img, (30, 30))
img = np.array([img])
# print(img)
print(np.argmax(model.predict(img)[0]))