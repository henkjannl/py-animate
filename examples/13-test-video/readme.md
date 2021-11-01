This example is used as an example for an issue posed at [ffmpeg-python](https://github.com/kkroening/ffmpeg-python/issues/606#issue-1034399324)

Remarks for [TestVideo.py](https://github.com/henkjannl/py-animate/blob/6c81d72a2db9ca54eb61d3d051729521134543e5/examples/13-test-video/TestVideo.py):

| File | Created on | Playable on VLC? | Playable on Windows Media Player? |
|------|------|------|------|
| movie-asus-pc.mp4  | Asus PC, windows 10, i7 processor | yes*   | no  |
| movie-asus-pc.mpeg | Asus PC, windows 10, i7 processor | yes    | no  |
| movie-hp-pc.mp4    | HP PC, windows 10, i7 processor   | yes    | no  |
| movie-hp-pc.mpeg   | HP PC, windows 10, i7 processor   | yes    | no  |
| export-shotcut-from-hp.mp4 | ShotCut export from same HP laptop | yes    | no |
| movie-asus-pc-converted-with-vlc.mp4 | Converted using VLC media player | yes | yes |

1) movie-asus-pc.mp4 looks garbled result using VLC on Asus, good result on HP
2) All videos can be played using VLC on the HP laptop
3) Windows Media Player crashes when loading any of these videos on both laptops, except the last one

VLC can also be used to convert the video to another .mp4 file. The result can be played on both laptops, also with Windows Media Player. It can then also be used in PowerPoint presentations.
