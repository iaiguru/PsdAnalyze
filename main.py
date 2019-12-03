import os
from psd_tools import PSDImage
from loguru import logger


def main():
    imagesetDir = 'E:\\ImageSet'
    inputExts = ('.psd')
    logFileName = "log.txt"

    # init logger
    logger.add(logFileName, format="{time} {level} {message}", level="INFO")

    logger.info('process started')
    # traverse psd dir
    for dirName, subdirList, fileList in os.walk(imagesetDir):
        for fname in fileList:
            if fname.lower().endswith(inputExts):
                procFile(dirName, fname)

    logger.info('process completed')


def procFile(dirName, fileName):
    outputExt = '.jpeg'
    rawsetDir = '.\\dataset\\raw\\'
    targetsetDir = '.\\dataset\\target\\'
    inputFilePath = dirName + '\\' + fileName
    outputFileName = os.path.splitext(fileName)[0] + outputExt

    try:
        # open
        psd = PSDImage.open(inputFilePath)
        # export composed layer
        psd.compose().save(targetsetDir + outputFileName)
        logger.info(fileName + ' -> target')
        # export background layer
        for layer in psd:
            if layer.name == '背景':
                layer_image = layer.topil()
                layer_image.save(rawsetDir + outputFileName)
                logger.info(fileName + ' -> raw')
                break
    except:
        logger.error(fileName + ' -> error')


if __name__ == "__main__":
    main()
