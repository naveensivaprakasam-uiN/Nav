import numpy as np, soundfile as sf, json, subprocess, sys
B=sys.argv[1]
s,sr=sf.read(sys.argv[2] if len(sys.argv)>2 else 'rn48.wav',dtype='float32')
V=json.load(open('rec16.wav.vad.json')); segs=json.load(open('segs.json'))
PRE,POST,FADE=0.05,0.12,0.02
def fade(x,n):
    n=min(n,len(x)//2); r=np.linspace(0,1,n,dtype=np.float32); x[:n]*=r; x[-n:]*=r[::-1]; return x
for i,(a,b,_) in enumerate(segs):
    regs=[(max(va,a-0.3),min(vb,b+0.3)) for va,vb in V if vb>a-0.3 and va<b+0.3]
    t0=regs[0][0]-PRE; t1=regs[-1][1]+POST
    out=np.zeros(int((t1-t0)*sr),np.float32)
    for va,vb in regs:
        p,q=int((va-PRE)*sr),int((vb+POST)*sr); o=p-int(t0*sr); seg=fade(s[p:q].copy(),int(FADE*sr)); seg=seg[:max(0,len(out)-o)]
        out[o:o+len(seg)]+=seg
    out=np.concatenate([np.zeros(int(.2*sr),np.float32),out,np.zeros(int(.3*sr),np.float32)])
    sf.write(f'/tmp/tts/c{i:02d}.wav',out,sr)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'/tmp/tts/c{i:02d}.wav','-af','highpass=f=80,lowpass=f=12000,loudnorm=I=-16:TP=-1.5:LRA=11','-ar','44100','-ac','1','-c:a','libmp3lame','-b:a','96k',f'{B}/audio/{i:02d}.mp3'],check=True)
    print(f'{i:02d} {len(regs)} speech parts, {len(out)/sr:.1f}s')
