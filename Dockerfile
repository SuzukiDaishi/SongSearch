FROM pytorch/pytorch

RUN pip install --upgrade torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1 ffmpeg

RUN pip install pretty-midi==0.2.9 omegaconf==2.1.1 youtube-dl==2021.12.17 transformers==4.16.1 pytorch-lightning essentia==2.1b6.dev609 note-seq==0.0.3 pyFluidSynth==1.3.0

RUN pip install mutagen

# docker build ./ -t pytorch_demo
# sudo docker run -it -v $(pwd):/workspace pytorch_demo:latest python build.py