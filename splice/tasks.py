from ModelToSQL.celery import app
import os
import shutil

from ModelToSQL.settings import BASE_DIR
#from App.detect_project.predict_my import func_predict
from offlineTask.models import SingleImagePreprocessInfo, SingleImageSpliceInfo


def storgeSplice(singleImage):
    print('enter storgeSplice')

    singleImageSplices = SingleImageSpliceInfo.objects.all()
    if singleImageSplices:
        for singleImageSplice in singleImageSplices:
            if singleImageSplice.singleImageId == singleImage.id \
                and singleImageSplice.is_splice == True:
                return

    singleImageSplice = SingleImageSpliceInfo()
    singleImageSplice.singleImageId = singleImage.id
    singleImageSplice.is_splice = True
    singleImageSplice.imagePreprocessPath = singleImage.imagePreprocessPath
    singleImageSplice.overDate = singleImage.overDate


    file = singleImage.imagePreprocessPath.split('/')[-1]

    preprocess_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', singleImage.imagePreprocessPath)
    splice_relafolder = '%s/%s/%s/' % (singleImage.title, singleImage.overDate, 'splice')
    splice_folder = '%s/%s/%s' % (BASE_DIR, 'static/upload', splice_relafolder)

    if not os.path.exists(splice_folder):
        os.makedirs(splice_folder)

    shutil.copy(preprocess_folder, splice_folder + file)
    singleImageSplice.imageSplicePath = splice_relafolder + file
    singleImageSplice.save()
    print('>---比对结束22222---<')

@app.task(name='splice.tasks.handleSplice')
def handleSplice(user):
    print('--->>开始比对任务222222<<---')
    singleImages = SingleImagePreprocessInfo.objects.all()
    print('--->>开始比对任务333333<<---')
    singleImageSpliceInfos = SingleImageSpliceInfo.objects.all()
    print('--->>开始比对任务444444<<---')
    for singleImage in singleImages:
        if singleImage.overDate == user.overDate:
            fname = BASE_DIR + "/static/upload/" + singleImage.imagePreprocessPath
            #predict_result = func_predict(str(fname))
            predict_result = 1
            if predict_result is 0 or 1:
               storgeSplice(singleImage)