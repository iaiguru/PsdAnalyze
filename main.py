import os
from psd_tools import PSDImage
from loguru import logger
from PIL import Image

# constants
IMAGESET_DIR = 'E:\\ImageSet'
INPUT_EXT = ('.psd')
LOGFILE = "log.txt"
MAX_RESIZE = 500
OUTPUT_EXT = '.jpeg'
RAWSET_DIR = '.\\dataset\\raw\\'
TARGETSET_DIR = '.\\dataset\\target\\'
MIN_FILE_SIZE = 2  # 2KB
RAW_LAYER_LABEL = '背景'


def main():
    # init logger
    logger.add(LOGFILE, format="{time} {level} {message}",
               level="INFO", encoding="utf-8", mode="w")

    logger.info('process started')

    # traverse psd dir
    for dirName, subdirList, fileList in os.walk(IMAGESET_DIR):
        for fname in fileList:
            if fname.lower().endswith(INPUT_EXT):
                procFile(dirName, fname)
                break

    logger.info('process completed')


def resizeImage(image):
    width, height = image.size
    size = width
    if height > size:
        size = height
    ratio = 1
    if size > MAX_RESIZE:
        ratio = MAX_RESIZE / size
    if size == width:
        width = MAX_RESIZE
        height = int(ratio * height)
    else:
        width = int(ratio * width)
        height = MAX_RESIZE

    return image.resize((width, height))


def procFile(dirName, fileName):
    inputFilePath = dirName + '\\' + fileName
    outputFileName = os.path.splitext(fileName)[0] + OUTPUT_EXT

    try:
        # check filesize
        if os.stat(inputFilePath).st_size < MIN_FILE_SIZE * 1024:
            logger.info(
                '{0} -> less than {1}KB'.format(inputFilePath, MIN_FILE_SIZE))
            return
        # open
        psd = PSDImage.open(inputFilePath)
        # export composed layer
        image = resizeImage(psd.compose())
        image.save(TARGETSET_DIR + outputFileName)
        logger.info('{0} -> target'.format(inputFilePath))
        # export background layer
        rawFound = False
        for layer in psd:
            if layer.name == RAW_LAYER_LABEL:
                layerImage = layer.topil()
                width, height = layerImage.size
                image = resizeImage(layerImage)
                resizedWidth, resizedHeight = image.size
                logger.info('{0} -> resized: ({1} , {2}) to ({3}, {4})'.format(
                    inputFilePath, width, height, resizedWidth, resizedHeight))
                image.save(RAWSET_DIR + outputFileName)
                logger.info('{0} -> raw'.format(inputFilePath))
                rawFound = True
                break
        if rawFound == False:
            logger.info('{0} -> raw not found'.format(inputFilePath))
    except:
        logger.error('{0} -> error'.format(inputFilePath))


if __name__ == "__main__":
    main()
