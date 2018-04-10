# !/bin/bash

date=$(date +%m\-%d\-%Y);
SCRIPTPATH="$( cd "$HOME/Pictures/Screenshots" ; pwd -P )"
FILE=$SCRIPTPATH/"Screen_"$date

if [[ -e $FILE.png ]]; then
    i=1
    while [[ -e $FILE"_"$i.png ]] ; do
        let i++
    done
    # echo $i
    # echo "$FILE"_"$i.png"
    exec screencapture "$FILE"_"$i.png"
else
	exec screencapture "$FILE.png"  
fi

