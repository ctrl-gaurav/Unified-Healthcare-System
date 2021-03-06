from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np


model=load_model('weights/pneumonia/pneumonia.h5')

class run_model():
    def __init__(self) -> None:
        pass

    def model_predict(self, img_path):
        print(img_path)
        img=image.load_img(str(img_path),target_size=(224,224))

        x=image.img_to_array(img)
        x=np.expand_dims(x, axis=0)
        img_data=preprocess_input(x)
        classes=model.predict(img_data)
        result=int(classes[0][0])
        print(classes)
        print(int(classes[0][0]))
        print(int(classes[0][1]))

        if result==0:
            return "Person is Affected By PNEUMONIA"
        else:
            return "Result is Normal"        