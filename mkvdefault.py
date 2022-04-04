
import subprocess
import sys
import enzyme
import os

alltracks = []
paths = sys.argv[1:]
paths.sort()
first = True
for path in paths:
        #mkv = pymkv.MKVFile(path)
        with open(path, 'rb') as f:
            test = enzyme.MKV(f)
        tracksforfile = []
        tracksforfile.append(path)
        for track in test.video_tracks:
            if (first == True):
                print(os.path.basename(path))
                print(track.number,"Video",track.name,track.language,track.codec_id,int(track.default))
        for track in test.audio_tracks:
            temp = ((track.number,"Audio",track.language))
            tracksforfile.append(temp)
            
            if (first == True):
                print(track.number,"Audio",track.name,track.language,track.codec_id,int(track.default))
                    
        for track in test.subtitle_tracks:
            temp = ((track.number,"Subs",track.name,track.language,track.codec_id))
            tracksforfile.append(temp)
            
            if (first == True):
                
                print(track.number,"Subs",track.name,track.language,track.codec_id,int(track.default))
        alltracks.append(tracksforfile)
        first = False
default_audio = int(input("\npick default audio track id: "))
default_subs = int(input("pick default subs track id: "))
errorfiles = []
allsame = True
for file in alltracks:
    localsame = True
    localerror = []
    print(os.path.basename(file[0]))
    if(len(file) != len(alltracks[0])):
            sizetemp = []
            if(len(alltracks[0][1:]) > len(file[1:])):
                for i in range(len(alltracks[0][1:])):
                    if i >= len(file[1:]):
                        sizetemp.append("(EMPTY)")
                    else:
                        sizetemp.append(file[1:][i])
            else:
                for i in range(len(file[1:])):
                    if i >= len(alltracks[0][1:]):
                        alltracks[0][1:] += ["(EMPTY)"]
                        sizetemp.append(file[1:][i])
                    else:
                        sizetemp.append(file[1:][i])
            errorfiles.append((file[0],"size",sizetemp))
            allsame = False
            print("Error size\n")
            continue
    for i in range(len(file[1:])):
        if(file[1:][i] != alltracks[0][1:][i]):
            localerror.append(("X",file[1:][i]))
            allsame = False
            localsame = False
        else:
            localerror.append(("OK",file[1:][i]))
    if(localsame):
        print("metadata matches, editing defaults...")
        for i in range(2,len(alltracks[0][1:]) + 2):
            if (i == default_audio or i == default_subs):
                command = f'mkvpropedit.exe "{file[0]}" --edit track:{i} --set flag-default=1'
                subprocess.run(command,capture_output=True)
            else:
                command = f'mkvpropedit.exe "{file[0]}" --edit track:{i} --set flag-default=0'
                subprocess.run(command,capture_output=True)
        print("done!\n")
    else:
        print("Error name\n")
        errorfiles.append((file[0],"name",localerror))
if(not allsame):
    print("\n\nthere was an error changing one or more files\n")
    print("the following files are different from file",os.path.basename(alltracks[0][0]) + ":\n")
    for file in errorfiles:
        print("\n" + os.path.basename(file[0]))
        if(file[1] == "size"):
            for i in range(len(file[2])):
                x=0
                print(file[2][i],alltracks[0][1:][i])
        elif(file[1] == "name"):
            for i in range(len(file[2])):
                print(file[2][i][0],file[2][i][1],alltracks[0][1:][i])
else: 
    print("\ndone without errors!")
input()