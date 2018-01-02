
basePath='/home/lj/work/project/dataset/data_UBK/audio'
for x in $basePath/*/*.wav
do
    #echo $x
    b=${x};#${x##*/}
    c=${x/.wav/-tmp.wav}
    d=${x/.wav/-S.wav}
    echo $b
    echo $c
    echo $d
    sox $b -r 44100 $c
    mv $b $d
    mv $c $b
    #break
done

