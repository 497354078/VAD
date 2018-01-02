from util import *
from general import get_vad_dict



if __name__ == '__main__':
    print ''
    dataType = 'ESC10'
    vadFile = 'files_{:s}/vad.scp'.format(dataType)

    vadDict = get_vad_dict(vadFile)


