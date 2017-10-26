# -*- coding: utf-8 -*-
import argparse
import os
import re
from hparams import hparams, hparams_debug_string
from synthesizer import Synthesizer


sentences = [
#'Vân Anh đã hẹn báo thức cho bạn vào lúc bảy giờ ba mươi phút sáng ngày mai.',
#'Theo dự báo thì Đà Lạt vào cuối tuần này sẽ có mưa nhẹ vào buổi sáng.',
#'Xin chào, Vân Anh có thể hỗ trợ được gì cho anh chị ạ?',
#'Bạn đang nghe các bài hát của Trịnh Công Sơn.',
#'Bảo Hiểm Xã Hội, Bảo Hiểm Y Tế đầy đủ cho người lao động.',
#'bao hiem xa hoi, bao hiem y te day du cho nguoi lao dong.',
#'Chiến thắng cho đội nhà là thứ cao nhất cổ động viên hướng tới.',
#'Đôi nam nữ mang vàng giả đi bán bị cam me ra ghi lại.',
#'năm giờ mười phút ngày tám tháng chín năm hai nghìn không trăm mười bảy.',
#'Xin chào bạn, hôm nay là thứ hai',
#'Bé trông xanh xao và bị ho.',
'Công ty Olli.',
'Công ty ô li.',
#'Bạn đang nghe bài hát Chạm khẽ tim anh một chút thôi.'
#'Thêm vào đó là tình trạng hoạt động vượt công suất thiết kế.',
#'Bài tập này có từ thời Bắc Tống Trung Quốc.'
]


def get_output_base_path(checkpoint_path):
  base_dir = os.path.dirname(checkpoint_path)
  m = re.compile(r'.*?\.ckpt\-([0-9]+)').match(checkpoint_path)
  name = 'eval-%d' % int(m.group(1)) if m else 'eval'
  return os.path.join(base_dir, name)


def run_eval(args):
  print(hparams_debug_string())
  synth = Synthesizer()
  synth.load(args.checkpoint)
  base_path = get_output_base_path(args.checkpoint)
  for i, text in enumerate(sentences):
    path = '%s-%d.wav' % (base_path, i)
    print('Synthesizing: %s' % path)
    with open(path, 'wb') as f:
      f.write(synth.synthesize(text))


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--checkpoint', required=True, help='Path to model checkpoint')
  parser.add_argument('--hparams', default='',
    help='Hyperparameter overrides as a comma-separated list of name=value pairs')
  args = parser.parse_args()
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
  hparams.max_iters = 500
  hparams.parse(args.hparams)
  run_eval(args)


if __name__ == '__main__':
  main()
