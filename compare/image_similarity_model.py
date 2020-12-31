import os
import numpy as np
import cv2  # opencv-python==3.4.2.16, opencv-contrib-python==3.4.2.16
from PIL import Image

# 避免CUDNN_STATUS_ALLOC_FAILED与CUDA_ERROR_OUT_OF_MEMORY
from tensorflow import ConfigProto, Session
config = ConfigProto(allow_soft_placement=True)
config.gpu_options.allow_growth = True
sess = Session(config=config)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 运行环境：RTX2060 + CUDA 9.2 + cuDNN 7.2 + tensorflow-gpu 1.12.0 (必须用conda安装)
# from tensorflow.python.keras.applications.mobilenet import MobileNet, preprocess_input
from tensorflow.python.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.python.keras.preprocessing import image as process_image
from tensorflow.python.keras.utils.data_utils import Sequence
from tensorflow.python.keras.layers import GlobalAveragePooling2D
from tensorflow.python.keras.models import Model

class DeepModel():
    def __init__(self):
        self._model = self._define_model()
        print('Loading MobileNet.')

    @staticmethod
    def _define_model(output_layer=-1):
        dir_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        # base_model = MobileNet(input_shape=(224, 224, 3), weights=dir_path + '/mobilenet_1_0_224_tf_no_top.h5', include_top=False)
        base_model = MobileNetV2(input_shape=(224, 224, 3), weights=dir_path + '/mobilenet_v2_1.0_224_no_top.h5', include_top=False)
        output = base_model.layers[output_layer].output
        output = GlobalAveragePooling2D()(output)
        model = Model(inputs=base_model.input, outputs=output)
        return model

    @staticmethod
    def preprocess_image(img):  # 将原输入图像缩放，并将BGR转换为RGB
        x = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
        x = Image.fromarray(cv2.cvtColor(x, cv2.COLOR_BGR2RGB))
        x = process_image.img_to_array(x)
        x = preprocess_input(x)
        return x

    def extract_feature(self, generator):
        features = self._model.predict_generator(generator)
        return features


class DataSequence(Sequence):

    def __init__(self, img, boxs, generation, batch_size=32):
        self.img = img
        self.list_of_boxs = boxs
        self.data_generation = generation
        self.batch_size = batch_size

    def __len__(self):
        '''The number of batches per epoch.'''
        return int(np.ceil(len(self.list_of_boxs) / self.batch_size))

    def __getitem__(self, idx):
        '''Generate one batch of data.'''
        batch_boxs = self.list_of_boxs[idx * self.batch_size: (idx + 1) * self.batch_size]
        batch_img = self.data_generation(self.img, batch_boxs)
        return np.array(batch_img)


class ImageSimilarity():

    def __init__(self):
        self._batch_size = 32
        self._model = DeepModel()

    @property
    def batch_size(self):
        '''Batch size of model prediction.'''
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size):
        self._batch_size = batch_size

    def _cosine_distance(self, features1, features2):
        numerator = np.sum(features1 * features2, axis=1)
        denominator = np.sum(np.linalg.norm(features1, axis=1, keepdims=True) * np.linalg.norm(features2, axis=1, keepdims=True), axis=1)
        return numerator / denominator

    def _img_batch_generation(self, img, boxs):
        img_batch = []
        for box in boxs:
            x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            img_region = img[y:y + h, x:x + w]
            img_region = DeepModel.preprocess_image(img_region)
            img_batch.append(img_region)
        return img_batch

    def _data_generator(self, img, boxs):
        return DataSequence(img, boxs, self._img_batch_generation, batch_size=self._batch_size)

    def compare_images(self, img1, img2, boxs):
        generator = self._data_generator(img1, boxs)
        print(generator,type(generator))
        features1 = self._model.extract_feature(generator)

        generator = self._data_generator(img2, boxs)
        features2 = self._model.extract_feature(generator)
        distances = self._cosine_distance(features1, features2)
        return distances