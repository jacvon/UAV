from ModelToSQL.celery import app
import os
import shutil

from ModelToSQL.settings import BASE_DIR
from offlineTask.models import SingleImagePreprocessInfo, SingleImageIdentifyInfo


def storgeIdentify(singleImage):
    print('enter storgeIdentify')

    singleImageIdentifys = SingleImageIdentifyInfo.objects.all()
    if singleImageIdentifys:
        for singleImageIdentify in singleImageIdentifys:
            if singleImageIdentify.singleImageId == singleImage.id \
                    and singleImageIdentify.is_identify == True:
                return

    singleImageIdentify = SingleImageIdentifyInfo()
    singleImageIdentify.singleImageId = singleImage.id
    singleImageIdentify.title = singleImage.title
    singleImageIdentify.is_identify = True
    singleImageIdentify.overDate = singleImage.overDate
    singleImageIdentify.imagePreprocessPath = singleImage.imagePreprocessPath

    file = singleImage.imagePreprocessPath.split('/')[-1]
    preprocess_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', singleImage.imagePreprocessPath)
    identify_relafolder = '%s/%s/%s/' % (singleImage.title, singleImage.overDate, 'identify')
    identify_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload',identify_relafolder)

    if not os.path.exists(identify_folder):
        os.makedirs(identify_folder)

    shutil.copy(preprocess_folder, identify_folder + file)
    singleImageIdentify.imageIdentifyPath = identify_relafolder + file
    singleImageIdentify.save()
    print('>---任务结束11111---<')

@app.task(name='identify.tasks.handleIdentify')
def handleIdentify(user):
    print('--->>开始执行任务11111<<---')
    singleImages = SingleImagePreprocessInfo.objects.all()
    singleImageIdentifyInfos = SingleImageIdentifyInfo.objects.all()
    for singleImage in singleImages:
        if singleImage.overDate == user.overDate:
           fname = BASE_DIR + "/static/upload/" + singleImage.imagePreprocessPath
           #predict_result = func_predict(str(fname))
           predict_result = 0
           if predict_result is 0 or 1:
              storgeIdentify(singleImage)
