# -*- coding: utf-8 -*-
import io
import numpy as np
import tensorflow as tf
from hparams import hparams
from models import create_model
from text import text_to_sequence
from util import audio


class Synthesizer:
  def load(self, checkpoint_path, model_name='tacotron'):
    print('Constructing model: %s' % model_name)
    inputs = tf.placeholder(tf.int32, [1, None], 'inputs')
    input_lengths = tf.placeholder(tf.int32, [1], 'input_lengths')
    with tf.variable_scope('model') as scope:
      self.model = create_model(model_name, hparams)
#      for i in range(2):
#        with tf.variable_scope('net', reuse=bool(i)):
#          with tf.device('/gpu:{}'.format(i)):
#            with tf.name_scope('gpu_{}'.format(i)):
#               self.model.initialize(inputs, input_lengths)
      self.model.initialize(inputs, input_lengths)

#    print('Loading checkpoint: %s' % checkpoint_path)
#    config = tf.ConfigProto(allow_soft_placement=True)
#    config.gpu_options.allow_growth = True
#    self.session = tf.Session(config=config)
    self.session = tf.Session()
    self.session.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    saver.restore(self.session, checkpoint_path)


  def synthesize(self, text):
    cleaner_names = [x.strip() for x in hparams.cleaners.split(',')]
    seq = text_to_sequence(text, cleaner_names)
    feed_dict = {
      self.model.inputs: [np.asarray(seq, dtype=np.int32)],
      self.model.input_lengths: np.asarray([len(seq)], dtype=np.int32)
    }
    spec = self.session.run(self.model.linear_outputs[0], feed_dict=feed_dict)
    out = io.BytesIO()
    audio.save_wav(audio.inv_spectrogram(spec.T), out)
    return out.getvalue()
