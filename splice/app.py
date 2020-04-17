import os
import shutil

from ModelToSQL.settings import BASE_DIR
from App.detect_project.predict_my import func_predict
from offlineTask.models import SingleImageInfo


def storgeSplice(singleImage):
    singleImage.is_splice = True
    file = singleImage.imagePreprocessPath.split('/')[-1]

    preprocess_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', singleImage.imagePreprocessPath)
    splice_relafolder = '%s/%s/%s/' % (singleImage.title, singleImage.overDate, 'splice')
    splice_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', splice_relafolder)

    if not os.path.exists(splice_folder):
        os.makedirs(splice_folder)

    shutil.copy(preprocess_folder, splice_folder + file)
    singleImage.imageSplicePath = splice_relafolder + file
    singleImage.save()

def handleSplice(user):
    singleImages = SingleImageInfo.objects.all()
    for singleImage in singleImages:
        if singleImage.overDate == user.overDate and singleImage.is_splice is False:
            fname = BASE_DIR + "/static/upload/" + singleImage.imagePreprocessPath
            predict_result = func_predict(str(fname))
            if predict_result is 0 or 1:
                storgeSplice(singleImage)