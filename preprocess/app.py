import datetime
import os
import shutil

from ModelToSQL.settings import BASE_DIR
from offlineTask.models import SingleImageInfo


def handlePreprocess(user, newItem):
    singleImage = SingleImageInfo()
    singleImage.title = user.title.mapNickName
    singleImage.imageOriginPath = newItem
    singleImage.overDate = user.overDate

    #新建预测文件夹并存储预处理后的图片，后续该逻辑应放入预处理模块中
    file = newItem.split('/')[-1]
    #overDate = datetime.datetime.now().strftime("%Y%m%d/%H%M%S")
    #利用绝对路径来拷贝图片
    origin_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', newItem)
    preprocess_folder = '%s/%s/%s/%s/%s/' % (BASE_DIR, 'static/upload', singleImage.title, user.overDate, 'preprocess')
    #在实际数据库中只存相对路径
    preprocess_relaFolder = '%s/%s/%s/' % (singleImage.title, user.overDate, 'preprocess')

    if not os.path.exists(preprocess_folder):
        os.makedirs(preprocess_folder)

    shutil.copy(origin_folder, preprocess_folder + file)
    singleImage.begin = datetime.datetime.now()
    singleImage.imagePreprocessPath = preprocess_relaFolder + file
    singleImage.save()