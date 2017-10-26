# Text-to-Speech
# Requirement
    pip install -r requirements.txt
# Process data
    python preprocess.py --dataset ljspeech
# Training
    python train.py
# Evaluation
    python eval.py --checkpoint=~/tacotron/logs-tacotron/model.ckpt-163000
# Tensorboard
    tensorboard --logdir ~/tacotron/logs-tacotron
