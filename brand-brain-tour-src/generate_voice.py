import json, re, subprocess, numpy as np, soundfile as sf, sys
from kokoro_onnx import Kokoro
import sherpa_onnx
B=sys.argv[1]
st=json.load(open(B+'/steps.json'))
lines=[st['intro']]+[s['v'] for s in st['steps']]
k=Kokoro('kokoro-v1.0.onnx','voices-v1.0.bin')
VV=np.load('voices-v1.0.bin'); VOICE=VV['bf_lily']  # voice D (Lily), chosen by the team
d='sherpa-onnx-whisper-base.en/'
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+'base.en-encoder.int8.onnx',decoder=d+'base.en-decoder.int8.onnx',tokens=d+'base.en-tokens.txt',language='en',task='transcribe')
def norm(s): return re.sub(r'[^a-z0-9 ]','',s.lower()).split()
def wer(a,b):
    a,b=norm(a),norm(b);D=[[i+j if i*j==0 else 0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1): D[i][j]=min(D[i-1][j]+1,D[i][j-1]+1,D[i-1][j-1]+(a[i-1]!=b[j-1]))
    return D[-1][-1]/len(a)
tot=0
for n,t in enumerate(lines):
    ph=k.tokenizer.phonemize(t,'en-gb').replace('mˈɛtəɹ','mˈɛtə')
    s,sr=k.create(ph,voice=VOICE,speed=0.98,lang='en-gb',is_phonemes=True)
    s=np.concatenate([np.zeros(int(.12*sr),np.float32),s.astype(np.float32),np.zeros(int(.25*sr),np.float32)])
    sf.write(f'/tmp/tts/{n:02d}.wav',s,sr)
    stv=rec.create_stream();stv.accept_waveform(sr,s);rec.decode_stream(stv)
    w=wer(t,stv.result.text);tot+=len(s)/sr
    print(f'{n:02d} {len(s)/sr:5.1f}s WER={w:.2f} peak={np.abs(s).max():.2f}' + ('' if w<0.06 else '  >> '+stv.result.text))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'/tmp/tts/{n:02d}.wav','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ac','1','-ar','24000','-b:a','96k',f'{B}/audio/{n:02d}.mp3'],check=True)
print('total',round(tot),'s')
