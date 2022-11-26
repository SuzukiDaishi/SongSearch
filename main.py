import glob
from mutagen.mp4 import MP4
import json, os, sys, subprocess
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

for i in range(1, 22):
    composer = f"composer{i}"
    print(composer)
    pm, _, _, _ = wrapper.generate(
        audio_path="data_wav/THE IDOLM@STER STARLIT SEASON 01/05 SESSION!.wav", 
        composer=composer, 
        model=model
    )
    pm.write(composer+".midi")