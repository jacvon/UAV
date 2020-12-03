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
from identify.yolo_video import identify_handle


def mosiac_handle(userId, queryset):
    print("start Mosiac Process")
    compareInputPath = ''
    identifyInputPath = ''
    spliceInputPath = ''
    isPreFlag = False
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
                        queryset.update(preprocess_status='p')
                        preprocess_handle(originPath, originPath.replace('origin','preprocess'),
                                         user.overDate, user.title_id, ".JPG",
                                         preprocessSet.is_brightness, preprocessSet.is_dehaze, preprocessSet.is_gamma,
                                         preprocessSet.is_clahe)
                        isPreFlag = True
                        compareInputPath = originPath.replace('origin','preprocess')
                        identifyInputPath = originPath.replace('origin','preprocess')
                        spliceInputPath = originPath.replace('origin','preprocess')

            if user.isIdentify:
                queryset.update(identify_status='p')
                if isPreFlag:
                    identify_handle(identifyInputPath, identifyInputPath.replace('preprocess', 'identify'),
                                    user.overDate, user.title_id)
                else:
                    identify_handle(identifyInputPath, identifyInputPath.replace('origin', 'identify'),
                                    user.overDate, user.title_id)
            if user.isSplice:
                queryset.update(splice_status='p')
                if isPreFlag:
                    splice_handle(spliceInputPath,spliceInputPath.replace('preprocess','splice'),
                                user.overDate, user.title_id)
                else:
                    splice_handle(spliceInputPath, spliceInputPath.replace('origin', 'splice'),
                                  user.overDate, user.title_id)
            if user.isCompare:
                queryset.update(comparison_status='p')
                splices = SingleImageSpliceInfo.objects.all()
                for splice in splices:
                    if splice.id == user.comparePath_id:
                        if isPreFlag:
                            compare_handle(compareInputPath, compareInputPath.replace('preprocess','compare'),
                                           splice.imageSplicePath, splice.gpsCsvPath,
                                           user.overDate, user.title_id)
                        else:
                            compare_handle(compareInputPath, compareInputPath.replace('origin', 'compare'),
                                           splice.imageSplicePath, splice.gpsCsvPath,
                                           user.overDate, user.title_id)
                        break
            break