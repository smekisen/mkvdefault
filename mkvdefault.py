
import subprocess
import sys
import os
import json


paths = sys.argv[1:]
paths.sort()
loop = True
while(loop):
    alltracks = []
    first = True
    print(os.path.basename(paths[0]))
    def load_json(file):
        mkvmerge_json_out = subprocess.check_output([
            'mkvmerge',
            '--identify',
            '--identification-format',
            'json',
            os.path.abspath(file),
            ], stderr=subprocess.DEVNULL)
        json_data = json.loads(mkvmerge_json_out)
        return json_data
        
        
    for path in paths:
            trackjson = load_json(path)
            tracksforfile = []
            tracksforfile.append(path)
            for track in trackjson.get('tracks'):
                language = track.get('properties').get('language')
                title = track.get('properties').get('track_name')
                codec_id = track.get('properties').get('codec_id')
                codec = track.get('codec')
                track_type = track.get('type')
                number = track.get('properties').get('number')
                default_track = int(track.get('properties').get('default_track'))
                if (first == True):
                    print(number,track_type,title,language,codec,default_track)
                if(track_type == "audio"):
                    temp = ((number,track_type,language))
                    tracksforfile.append(temp)
                elif(track_type == "subtitles"):
                    temp = ((number,track_type,title,language,codec))
                    tracksforfile.append(temp)
            alltracks.append(tracksforfile)
            first = False
    default_audio = int(input("\npick default audio track id: "))
    default_subs = int(input("pick default subs track id: "))
    print("\n")
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
        paths = []
        for file in errorfiles:
            paths.append(file[0])
            print("\n" + os.path.basename(file[0]))
            if(file[1] == "size"):
                for i in range(len(file[2])):
                    x=0
                    print(file[2][i],alltracks[0][1:][i])
            elif(file[1] == "name"):
                for i in range(len(file[2])):
                    print(file[2][i][0],file[2][i][1],alltracks[0][1:][i])
        print("\n\nContinuing on first error-file\n\n")
    else: 
        print("\ndone without errors!")
        loop = False
input()