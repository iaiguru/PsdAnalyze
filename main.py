import os
from psd_tools import PSDImage


def main():
    imagesetDir = '.'
    inputExts = ('.psd')

    for dirName, subdirList, fileList in os.walk(imagesetDir):
        for fname in fileList:
            if fname.lower().endswith(inputExts):
                procFile(dirName, fname)


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
        print('Target - ' + inputFilePath)
        # export background layer
        for layer in psd:
            if layer.name == '背景':
                layer_image = layer.topil()
                layer_image.save(rawsetDir + outputFileName)
                print('Raw - ' + inputFilePath)
                break
    except:
        print('Parsing Error - ' + inputFilePath)


if __name__ == "__main__":
    main()
