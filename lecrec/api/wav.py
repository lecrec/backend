import wave
import tempfile
import os

def wav_split(filepath, filename, outpath='temp/'):
    wr=wave.open(filepath,"r")
    b=wr.readframes(wr.getframerate()*10800)
    j=0
    start_time=0
    slice_list=[0]
    latest_time=0
    cur_time=0
    is_started=False
    is_speaking=False
    for x in b:
        j=j+1
        if(j%2==1):
            continue
        cur_time=j/32000
        if (x>20 and x<246) :
            if(is_started==False):
                is_started=True
                start_time=j/(wr.getframerate()*2)
            elif(is_speaking==False):
                if(cur_time-latest_time>=0.20):
                    is_started=False
                elif(cur_time-start_time>0.30):
                    is_speaking=True
            latest_time=cur_time
        elif(is_speaking==True and cur_time-latest_time>=0.5):
            slice_list.append(start_time)
            is_speaking=False
            is_started=False

    if(is_started==True):
        slice_list.append(start_time)
    end=0
    j=0
    i=0
    while(True):
        if(i >= len(slice_list)):
            break
        if(slice_list[i]-j>20):
            mean=(slice_list[i]+j)/2
            slice_list.insert(i,mean)
            continue
        j=slice_list[i]
        i=i+1
    start_list=[0]
    j=0
    i=0
    dur=0
    time_list=[0]
    while(True):
        if(i >= len(slice_list)):
            break
        dur=slice_list[i]-j
        if(dur>=5):
            dur=0
            start_list.append(round(wr.getframerate()*(slice_list[i]-0.25)))
            time_list.append(slice_list[i]-0.25)
            j=slice_list[i]
        i=i+1
    if(wr.getnframes()-start_list[len(start_list)-1]<5*wr.getframerate()):
        start_list[len(start_list)-1]=wr.getnframes()
        time_list.pop(len(time_list)-1)
    else:
        start_list.append(wr.getnframes())
    bytes_arr=bytearray(b)
    spliter(filename, start_list, wr, bytes_arr, outpath=outpath)
    return time_list

def spliter(filename, start_list, wr, bytes_arr, outpath):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for i in range(len(start_list)-1):
        wav_file=wave.open(outpath + name_split(filename, i), "w")
        frame_num=start_list[i+1]-start_list[i]
        wav_file.setnchannels(wr.getnchannels())
        wav_file.setsampwidth(wr.getsampwidth())
        wav_file.setframerate(wr.getframerate())
        wav_file.setnframes(frame_num)
        wav_file.setcomptype(wr.getcomptype(),wr.getcompname())
        wav_file.writeframesraw(bytes_arr[2*start_list[i]:2*(start_list[i+1]-1)])
        wav_file.close()

def name_split(ori_filename, idx):
    return ori_filename.split('.')[0]+"+"+str(idx)+".wav"

if __name__ == '__main__':
    wav_split('little_prince.wav')
