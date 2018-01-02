from util import *
from tools.ogg2wav import ogg2wav
from make_cross_fold import make_cross_fold

def write_dict(dict_, files):
    f = open(files, 'wb')
    for id_, key in enumerate(sorted(dict_.keys())):
    #for id_, key in enumerate(dict_):
        if id_ == 0: print key, dict_[key]
        s = key
        for items in dict_[key]:
            s += ' '+items
        s += '\n'
        f.write(s)
    f.close()

def change_spk2utt(spkDict, uttDict, spk2utt):
    newspk2utt = {}
    for spkName in spk2utt:
        newSpkName = spkDict[spkName][0]
        newspk2utt[newSpkName] = []
        for uttName in spk2utt[spkName]:
            newUttName = uttDict[uttName][0]
            newspk2utt[newSpkName].append(newUttName)
    return newspk2utt

def change_utt2spk(spkDict, uttDict, utt2spk):
    newutt2spk = {}
    for uttName in utt2spk:
        newutt2spk[uttDict[uttName][0]] = spkDict[utt2spk[uttName][0]]
    return newutt2spk

def change_wavscp(uttDict, wavscp, destPath, duration, sr):
    newwavscp = {}
    for uttName in wavscp:
        newUttName = uttDict[uttName][0]
        newUttFile = os.path.join(destPath, newUttName+'.wav')
        newwavscp[newUttName] = [newUttFile]
        #print wavscp[uttName][0]
        ogg2wav(wavscp[uttName][0], newUttFile, duration=duration, sr=sr)
    return newwavscp

def make_files(dataType, files, dataPath, destPath, filePath, duration, sr):
    lines = open(files, 'rb').readlines()
    spk2utt = {}
    utt2spk = {}
    wavscp = {}
    for id_, items in enumerate(lines):
        items = items.split('\n')[0].split('\t')
        spkName, uttName = os.path.split(items[0])
        uttName = os.path.splitext(uttName)[0]
        spkID = items[1]
        if id_ == 0: print items, spkName, uttName
        assert uttName not in wavscp
        wavscp[uttName] = [os.path.join(dataPath, items[0])]

        #if spkName not in spk2utt:
        #    spk2utt[spkName] = []
        if spkID not in spk2utt:
            spk2utt[spkID] = []
        spk2utt[spkID].append(uttName)

        assert uttName not in utt2spk
        utt2spk[uttName] = [spkID] # esc diff with ubk

    spkDict = {}
    uttDict = {}
    for id_s, spkName in enumerate(spk2utt):
        newSpkName = dataType+'_{:03d}'.format(id_s)
        assert spkName not in spkDict
        spkDict[spkName] = [newSpkName]
        for id_u, uttName in enumerate(spk2utt[spkName]):
            newUttName = newSpkName+'U{:04d}'.format(id_u)
            assert uttName not in uttDict
            uttDict[uttName] = [newUttName]

    spk2utt = change_spk2utt(spkDict, uttDict, spk2utt)
    utt2spk = change_utt2spk(spkDict, uttDict, utt2spk)
    wavscp = change_wavscp(uttDict, wavscp, destPath, duration, sr)

    if not os.path.exists(filePath):
        os.makedirs(filePath)
    write_dict(spk2utt, os.path.join(filePath, 'spk2utt'))
    write_dict(utt2spk, os.path.join(filePath, 'utt2spk'))
    write_dict(wavscp, os.path.join(filePath, 'wav.scp'))
    write_dict(spkDict, os.path.join(filePath, 'spkDict.txt'))
    write_dict(uttDict, os.path.join(filePath, 'uttDict.txt'))
    pickle.dump(spkDict, open(os.path.join(filePath, 'spkDict.dict'), 'wb'),
                protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(uttDict, open(os.path.join(filePath, 'uttDict.dict'), 'wb'),
                protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

    sr = 44100
    duration = 4000
    dataType = 'UBK' #UBK + audio
    metaFile = '../Coding/src_ubk/files/meta.audiolist'
    filePath = 'files_{:s}'.format(dataType)
    dataPath = '/home/lj/work/project/dataset/data_{:s}/audio'.format(dataType)
    destPath = '/home/lj/work/project/dataset/data_audio'

    make_files(dataType, metaFile, dataPath, destPath, filePath, duration, sr)

    print ''
    #dataType = 'ESC10'
    #filePath = 'files_{:s}'.format(dataType)
    basePath = '../Coding/src_ubk/files/evaluate-setup'

    make_cross_fold(basePath, filePath)
