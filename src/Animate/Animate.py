import os
import time
#import numpy as np

import logging

LOG_FILENAME = '__logfile.txt'

try:
    os.remove(LOG_FILENAME)
except:
    pass
    
logging.basicConfig(filename=LOG_FILENAME, filemode='w',level=logging.DEBUG)

# www.pythonware.com/library/pil/handbook
from PIL import Image,ImageFont, ImageDraw
from PIL import ImageEnhance, ImageFilter

import Animate.Scripts
import Animate.Constants

#Todo: make this platform and -system independent
DEFAULTFONT = "C:\\WINDOWS\\Fonts\\verdana.TTF"

def timefmt(t):

    MIN  = 60
    HOUR = 60*MIN
    DAY  = 24*HOUR
    WEEK = 7*DAY
    YEAR = 365.25*DAY
    MONTH=YEAR/12

    if t>=YEAR:
        return "{:.1f} years".format(t/YEAR) 
    elif t>=MONTH:
        return "{:.1f} months".format(t/MONTH) 
    elif t>=WEEK:
        return "{:.1f} weeks".format(t/WEEK) 
    elif t>=DAY:
        return "{:.1f} days".format(t/DAY) 
    elif t>=HOUR:
        return "{:.1f} hours".format(t/HOUR) 
    elif t>=MIN:
        return "{:.1f} min".format(t/MIN) 
    else:
        return "{:.1f} sec".format(t) 


def Model(FileName, SheetName):

    print('### PARSING SCRIPTS  ###')
    logging.debug('### PARSING SCRIPTS  ###')

    # Create general list of scripts
    ScriptList = {}

    # Read main script
    Main = Animate.Scripts.Script(FileName, SheetName, ScriptList)

    # Parse the main script
    Main.ParseScript(FileName, SheetName)

    # Add the main script to the global list of scripts
    ScriptList[SheetName]=Main

    # Do some standard checks after parsing
    print('')
    print('### CHECKING SCRIPTS  ###')
    logging.debug('### CHECKING SCRIPTS  ###')
    OK = True
    for Script in ScriptList.values():

        if not Script.StandardChecks():
            OK=False

    assert OK

    # Get the global variables from the main script
    FramesPerSecond = Main.FramesPerSecond

    FirstFrame = int(Main.FirstFrame)

    if Main.LastFrame==-1:
        LastFrame = int(Main.MaxTime*FramesPerSecond)
    else:
        LastFrame = int(Main.LastFrame)

    MaxTime = 1.0*LastFrame/FramesPerSecond

    # Deploy all scripts, items and properties
    for Script in ScriptList.values():
        Script.Deploy(MaxTime)

    # Try to store the frames in a directory called 'Frames'
    Path = os.getcwd()
    p = os.path.join(Path,'Frames')
    if os.path.exists(p):
        if os.path.isdir(p):
            Path=p
    else:
        os.mkdir(p)
        Path=p

    # Start creating frames
    print('')
    print('### GENERATING IMAGES ###')
    logging.debug('### GENERATING IMAGES  ###')
    StartTime = time.time()

    ## ToDo: Creating GIFs is needs to be made configurable
    animatedImages = []
    #animatedSize = ( 800, int(800*Main.Height/Main.Width) )
    animatedSize = ( Main.Width, Main.Height )
    

    for Frame in range(FirstFrame, LastFrame):

        FileName='Frame%05d.png' % Frame
        
        if LastFrame != FirstFrame:
            PercentageReady = 100.0 * (Frame - FirstFrame + 1) / (LastFrame - FirstFrame)
        else:
            PercentageReady = 100.0

        # Check out the right time corresponding to this frame
        Time = 1.0*Frame/FramesPerSecond
        
        SecondsPassed = time.time() - StartTime
        SecondsToGo = SecondsPassed*(100-PercentageReady)/(PercentageReady)

        print('Generating frame %05d  t=%.2f s  %.1f%% ready, %s to go' % (Frame, Time, PercentageReady, timefmt(SecondsToGo)))

        # Start with a white image
        Picture = Image.new("RGBA", (Main.Width,Main.Height), color = '#FFFFFF' )

        # Get the picture from the Main script
        ItemPicture = Main.GetPicture(Time, Frame)

        # Draw the picture over the background
        Picture.paste( ItemPicture, (0,0) )

        # Show the time if desired
        if Main.ShowTime:
            Verdana = ImageFont.truetype(DEFAULTFONT, 20)
            Draw = ImageDraw.Draw(Picture)
            Draw.text( (2,Main.Height-24), '%.3f s' % Time, fill="Black", font=Verdana)

        # enhance the quality of the image
        Picture = Picture.filter(ImageFilter.SMOOTH_MORE)
        Picture = Picture.filter(ImageFilter.SHARPEN)
        logging.debug('  Frame %s saved' % FileName)
        Picture.save( os.path.join(Path, FileName), "PNG")

        animatedImages.append( Picture.resize(animatedSize, Image.ANTIALIAS) )

    if Main.AnimatedGIF:
        print("Creating animated GIF {gif}".format(gif=Main.AnimatedGIF))
        animatedImages[0].save(Main.AnimatedGIF,
                  save_all=True, append_images=animatedImages[1:], optimize=True, duration=40, loop=0)

    if Main.Movie:
        try:
            print("Creating movie {movie}".format(movie=Main.Movie))
            import ffmpeg
            stream = ffmpeg.input('Frames\Frame%05d.png')
            stream = ffmpeg.output(stream, Main.Movie)
            stream = ffmpeg.overwrite_output(stream)
            ffmpeg.run(stream)
        except Exception as e:
            print('Problem when creating the movie, perhaps ffmpeg is not installed')
            print('see https://ffmpeg.org/download.html')
            print(e)

