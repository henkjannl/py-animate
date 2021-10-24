# -*- coding: utf-8 -*-

import ffmpeg
mov='movie.mpeg'
try:
    stream = ffmpeg.input('Frames\Frame%05d.png')
    stream = ffmpeg.output(stream, mov)
    stream.overwrite_output()
    ffmpeg.run(stream)
except Exception as e:
    print(e)
