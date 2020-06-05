import os
from ModelToSQL.celery import app
from multiprocessing import Process, Event, Queue
import cv2
from ModelToSQL.settings import BASE_DIR
from compare.image_compare_multiprocess import compare_handle
from splice.image_stitch_multiprocess import splice_handle
from preprocess.image_preprocess import preprocess_handle
from offlineTask.models import OfflineTask, OfflinePreprocessSet, SingleImageSpliceInfo
from preprocess.apps import load_process, enhance_process
from splice.apps import seam_process, transform_process

#@app.task(name='offlineTask.tasks.mosiac_handle')
def mosiac_handle(userId):
    print("start Mosiac Process")
    compareInputPath = ''
    identifyInputPath = ''
    spliceInputPath = ''
    users = OfflineTask.objects.all()
    preprocessSets = OfflinePreprocessSet.objects.all()
    for user in users:
        if user.id == userId:
            originPath = BASE_DIR.replace('\\','/') + "/static/upload/" + user.folderOriginPath
            compareInputPath = originPath
            identifyInputPath = originPath
            spliceInputPath = originPath
            if (user.isCompare and user.isComparePre) \
               or (user.isIdentify and user.isIdentifyPre) \
                or (user.isSplice and user.isSplicePre):
                for preprocessSet in preprocessSets:
                    if preprocessSet.id == user.preprocessSet_id:
                       preprocess_handle(originPath, originPath.replace('origin','preprocess'),
                                         user.overDate, user.title_id, ".JPG",
                                         preprocessSet.is_brightness, preprocessSet.is_dehaze, preprocessSet.is_gamma,
                                         preprocessSet.is_clahe)
                       compareInputPath = originPath.replace('origin','preprocess')
                       identifyInputPath = originPath.replace('origin','preprocess')
                       spliceInputPath = originPath.replace('origin','preprocess')

            if user.isIdentify:
                print('处理识别')
            if user.isSplice:
                splice_handle(spliceInputPath,spliceInputPath.replace('preprocess','splice'),
                              user.overDate, user.title_id)
            if user.isCompare:
                splices = SingleImageSpliceInfo.objects.all()
                for splice in splices:
                    if splice.id == user.comparePath_id:
                        compare_handle(compareInputPath, compareInputPath.replace('preprocess','compare'),
                                       splice.imageSplicePath, splice.gpsCsvPath,
                                       user.overDate, user.title_id)
                        break
            break