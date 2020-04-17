import os
import shutil

from django.apps import AppConfig

from ModelToSQL.settings import BASE_DIR
from App.detect_project.predict_my import func_predict
from offlineTask.models import SingleImageInfo


def storgeIdentify(singleImage):
    singleImage.is_identify = True
    file = singleImage.imagePreprocessPath.split('/')[-1]
    preprocess_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', singleImage.imagePreprocessPath)
    identify_relafolder = '%s/%s/%s/' % (singleImage.title, singleImage.overDate, 'identify')
    identify_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload',identify_relafolder)

    if not os.path.exists(identify_folder):
        os.makedirs(identify_folder)

    shutil.copy(preprocess_folder, identify_folder + file)
    singleImage.imageIdentifyPath = identify_relafolder + file
    singleImage.save()

def handleIdentify(user):
    singleImages = SingleImageInfo.objects.all()
    for singleImage in singleImages:
        if singleImage.overDate == user.overDate and singleImage.is_identify == False:
            fname = BASE_DIR + "/static/upload/" + singleImage.imagePreprocessPath
            predict_result = func_predict(str(fname))
            if predict_result is 0 or 1:
                storgeIdentify(singleImage)