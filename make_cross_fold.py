from util import *

def make_cross_fold(basePath, filePath):
    destPath = os.path.join(filePath, 'cross_fold')
    make_path(destPath)
    check_path(basePath)

    spkDict = pickle.load(open(os.path.join(filePath, 'spkDict.dict'), 'rb'))
    uttDict = pickle.load(open(os.path.join(filePath, 'uttDict.dict'), 'rb'))

    for files in glob.glob(os.path.join(basePath, '*.txt')):
        print files
        fileName = os.path.split(files)[1]
        f = open(os.path.join(destPath, fileName), 'wb')
        lines = open(files, 'rb').readlines()
        for items in lines:
            items = items.split('\n')[0].split('\t')
            spkName, uttName = os.path.split(items[0])
            uttName = os.path.splitext(uttName)[0]
            spkID = items[1]
            f.write(spkDict[spkID][0]+' '+uttDict[uttName][0]+' '+spkID+'\n')
        f.close()


if __name__ == '__main__':
    print ''
    dataType = 'ESC10'
    filePath = 'files_{:s}'.format(dataType)
    basePath = '../Coding/src_esc10/files/evaluate-setup'

    make_cross_fold(basePath, filePath)


