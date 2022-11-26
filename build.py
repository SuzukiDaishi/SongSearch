import glob
from mutagen.mp4 import MP4
import json, os, sys, subprocess
import librosa
import numpy as np
import torch
from omegaconf import OmegaConf

sys.path.append("pop2piano")
from transformer_wrapper import TransformerWrapper

device = "cuda" if torch.cuda.is_available() else "cpu"
config = OmegaConf.load("pop2piano/config.yaml")
wrapper = TransformerWrapper(config)
wrapper = wrapper.load_from_checkpoint("model-1999-val_0.67311615.ckpt", config=config).to(device)
model = "dpipqxiy"
wrapper.eval()

if not os.path.isdir("data_wav"):
    os.mkdir("data_wav")
if not os.path.isdir("data_midi"):
    os.mkdir("data_midi")

data = []

for filepath in sorted(glob.glob(f"data/*/*.m4a")):
    print(filepath)
    mp4 = MP4(filepath)
    track_title     = mp4.tags["\xa9nam"][0]
    album           = mp4.tags["\xa9alb"][0]
    artist          = mp4.tags["\xa9ART"][0]
    year            = mp4.tags["\xa9day"][0]
    bitrate         = mp4.info.bitrate
    length          = mp4.info.length
    channels        = mp4.info.channels
    sample_rate     = mp4.info.sample_rate
    bits_per_sample = mp4.info.bits_per_sample
    codec           = mp4.info.codec
    print(f"track_title: {track_title}")
    print(f"album: {album}")
    print(f"artist: {artist}")
    print(f"year: {year}")
    print(f"bitrate: {bitrate}")
    print(f"length: {length}")
    print(f"channels: {channels}")
    print(f"sample_rate: {sample_rate}")
    print(f"bits_per_sample: {bits_per_sample}")
    print(f"codec: {codec}")
    WAVS_DIR = '/'.join(filepath.replace('data', 'data_wav').split('.')[0].split('/')[:-1])
    MIDIS_DIR = '/'.join(filepath.replace('data', 'data_midi').split('.')[0].split('/')[:-1])
    WAV_NAME = f"{WAVS_DIR}/{filepath.split('.')[0].split('/')[-1]}.wav"
    MIDI_NAME = f"{MIDIS_DIR}/{filepath.split('.')[0].split('/')[-1]}.midi"
    print(" ".join(["ffmpeg", "-i", f"{filepath}", "-loglevel", "quiet", f"{WAV_NAME}"]))
    
    ModeHist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    bpm = 0
    if not os.path.isdir(WAVS_DIR):
        os.mkdir(WAVS_DIR)
    if not os.path.isdir(MIDIS_DIR):
        os.mkdir(MIDIS_DIR)
    if not os.path.isfile(WAV_NAME):
        subprocess.run(["ffmpeg", "-i", f"{filepath}", "-loglevel", "quiet", f"{WAV_NAME}"])
        y, sr = librosa.load(WAV_NAME)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    if not os.path.isfile(MIDI_NAME) and os.path.isfile(WAV_NAME):
        composer = "composer3"
        pm, _, _, _ = wrapper.generate(
            audio_path=WAV_NAME, 
            composer=composer, 
            model=model
        )
        pm.write(MIDI_NAME)
        
        for i, roll in enumerate(pm.get_piano_roll() > 0):
            ModeHist[i % 12] += np.sum(roll).item()
    
    data.append({
        "track_title": track_title,
        "album": album,
        "artist": artist,
        "year": year,
        "bitrate": bitrate,
        "length": length,
        "channels": channels,
        "sample_rate": sample_rate,
        "bits_per_sample": bits_per_sample,
        "codec": codec,
        "bpm": tempo,
        "mode_hist": ModeHist,
        "file_path": filepath,
        "wav_path": WAV_NAME,
        "midi_path": MIDI_NAME,
    })
    print()
        

with open('data_wav.json', 'w') as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))