import os
import time

# www.lexicon.net/sjmachin/xlrd.html
import xlrd

import logging

from PIL import Image # www.pythonware.com/library/pil/handbook
from PIL import ImageFont, ImageDraw, ImageEnhance
from PIL import ImageFilter

from Animate.Items import *
from Animate.Properties import *
from Animate.Constants import *

LOG_FILENAME = '__logfile.txt'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

def SelectFont(Directories, Fonts):
    
    for Font in Fonts:
        for Path in Directories:
            try:
                FontName=os.path.join(Path,Font)
                SelectedFont = ImageFont.truetype(FontName, 20)
                return FontName
            except:
                logging.debug('%s not successful' % FontName )
            
    print('All attempts to load fonts failed')



class Script():

    def __init__(self, FileName, SheetName, ScriptList):

        logging.debug('  Script.__init__(%s, %s)' % (FileName, SheetName) )

        self.FileName        = FileName
        self.SheetName       = SheetName
        self.ScriptList      = ScriptList
        self.IsCanvas        = False
        self.FirstImage      = True
        self.ImageDir        = 'Pictures'
        
        self.FirstFrame      = 0            # Allows the processing of a subset of frames
        self.LastFrame       = -1
        self.FramesPerSecond = 10

        self.ShowTime        = False        # Display the time in each frame

        self.Movie           = False        # Can be overridden by filename of movie
        self.AnimatedGIF     = False        # Can be overridden by filename of animated gif

        self.MaxTime         = 0            # Largest time, retrieved from the parser
        
        self.TimeOffset      = 0.0          # Script, assembly or canvas can be run with an offset to the global time
        
        self.Width           = 800          # Width of the output image
        self.Height          = 600          # Height of the output image

        self.Items           = ItemDict()   # Dictionary of items

        # List of (time, item, back/front) tuples
        self.Zbuffer         = []
        self.ZbufferIndex    = 0

        # List of Items
        self.Zorder          = []

        # Picture that was processed last
        self.Picture         = False
        self.PictureFrame    = -1


    def ParseScript(self, FileName, SheetName):

        logging.debug('  Script.ParseScript(%s, %s)' % (FileName, SheetName))

        # Open excel file with frame data
        wb = xlrd.open_workbook(FileName)
        sh = wb.sheet_by_name(SheetName)

        print(' - parsing script %s' % SheetName)
        for Row in range(sh.nrows):

            # A row contains frame data if the first cell contains a float
            if sh.cell(rowx=Row,colx=0).ctype==xlrd.XL_CELL_NUMBER:

                time    = sh.cell(rowx=Row,colx=0).value
                command = sh.cell(rowx=Row,colx=1).value.upper().strip()

                if self.MaxTime<time: self.MaxTime=time

                if command == 'WIDTH':
                    # Determine the width of the output frames
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_NUMBER, \
                        "%s at row %d of sheet %s expects a number" % (command, Row+1, SheetName)

                    self.Width = int(sh.cell(rowx=Row,colx=2).value)

                elif command == 'HEIGHT':
                    # Determine the height of the output frames
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_NUMBER, \
                        "%s at row %d of sheet %s expects a number" % (command, Row+1, SheetName)

                    self.Height = int(sh.cell(rowx=Row,colx=2).value)

                elif command == 'FRAMESPERSECOND':
                    # Sets the number of frames per second for the whole movie
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_NUMBER, \
                        "%s at row %d of sheet %s expects a number in column C" % (command, Row+1, SheetName)

                    self.FramesPerSecond = sh.cell(rowx=Row,colx=2).value

                elif command == 'FIRSTFRAME':
                    # Determine the first frame to be processed,
                    # if not all frames must be processed. For debugging
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_NUMBER, \
                        "%s at row %d of sheet %s expects a number in column C" % (command, Row+1, SheetName)

                    self.FirstFrame = sh.cell(rowx=Row,colx=2).value

                elif command == 'LASTFRAME':
                    # Determine the last frame to be processed,
                    # if not all frames must be processed. For debugging
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_NUMBER, \
                        "%s at row %d of sheet %s expects a number in column C" % (command, Row+1, SheetName)

                    self.LastFrame = sh.cell(rowx=Row,colx=2).value

                elif command == 'SHOWTIME':
                    # Write the time in the lower left corner of the frames, for debug purposes
                    self.ShowTime = True

                elif command == 'HIDETIME':
                    # Do not write the time
                    self.ShowTime = False

                elif command == 'MOVIE':
                    # Sets the number of frames per second for the whole movie
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a filename for the movie" % (command, Row+1, SheetName)

                    self.Movie= sh.cell(rowx=Row,colx=2).value
                    print("Movie {movie} will be created after generating the frames".format(movie=self.Movie))

                elif command == 'ANIMATEDGIF':
                    # Sets the number of frames per second for the whole movie
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a filename for the animated gif" % (command, Row+1, SheetName)

                    self.AnimatedGIF= sh.cell(rowx=Row,colx=2).value
                    print("Animated GIF {gif} will be created after generating the frames".format(gif=self.AnimatedGIF))

                elif command == 'TABLE':
                    # Do not create a new script object, but import the commands in the current script
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string for the table name" % (command, Row+1, SheetName)

                    sheetname = sh.cell(rowx=Row,colx=2).value.strip()
                    self.ParseTable(self.FileName, sheetname)

                elif command == 'SCRIPT':
                    # Do not create a new script object, but import the commands in the current script

                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string for the script name" % (command, Row+1, SheetName)

                    sheetname = sh.cell(rowx=Row,colx=2).value.strip()

                    self.ParseScript(self.FileName, sheetname)

                elif command == 'ASSEMBLY':
                    # Create a new script object and use the image created by this
                    # script as feed for this item
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string for the assembly name" % (command, Row+1, SheetName)

                    assert sh.cell(rowx=Row,colx=3).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string for the sheet name" % (command, Row+1, SheetName)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()
                    sheetname = sh.cell(rowx=Row,colx=3).value

                    # If the script is not yet in the list, create it
                    if not sheetname in self.ScriptList:
                        NewScript = Script(FileName, sheetname, self.ScriptList)
                        self.ScriptList[sheetname] = NewScript
                        NewScript.ParseScript(FileName, sheetname)

                    # Assign the script to the
                    # ToDo: Implement item type directly
                    # ToDo: Implement change of script as function of time
                    self.Items[itemname].AddScript( time, sheetname )


                elif command == 'CANVAS':
                    # A canvas is an assembly of which the background is not reset for a new frame

                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string for the item tag" % (command, Row+1, SheetName)

                    assert sh.cell(rowx=Row,colx=3).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string for the sheet name" % (command, Row+1, SheetName)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()
                    sheetname = sh.cell(rowx=Row,colx=3).value

                    # If the script is not yet in the list, create it
                    if not sheetname in self.ScriptList:
                        NewScript = Script(FileName, sheetname, self.ScriptList)
                        NewScript.IsCanvas = True
                        self.ScriptList[sheetname] = NewScript
                        NewScript.ParseScript(FileName, sheetname)

                    # Assign the script to the
                    # ToDo: Implement item type directly
                    # ToDo: Implement change of script as function of time
                    self.Items[itemname].AddCanvas( time, sheetname )

                elif command == 'IMAGE':
                    # Assign a new filename for an image item
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string for the item tag" % (command, Row+1, SheetName)

#                    assert sh.cell(rowx=Row,colx=3).ctype==xlrd.XL_CELL_TEXT, \
#                        "%s at row %d expects a string for the filename" % (command, Row+1)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()
                    filename = os.path.join(self.ImageDir, sh.cell(rowx=Row,colx=3).value)

                    assert os.path.isfile(filename), \
                        "%s at row %d could not find file %s" % (command, Row+1, filename)

                    self.Items[itemname].AddImage( time, filename )


                elif command == 'MASK':

                    # Assign a new filename for a mask item
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string for the item tag" % (command, Row+1, SheetName)

                    assert sh.cell(rowx=Row,colx=3).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string for the filename" % (command, Row+1, SheetName)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()
                    filename = os.path.join(self.ImageDir, sh.cell(rowx=Row,colx=3).value)

                    assert os.path.isfile(filename), \
                        "%s at row %d could not find file %s" % (command, Row+1, filename)

                    self.Items[itemname].AddMask( time, filename )


                elif command == 'TEXT':
                    # Assign a new title for a text item
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string in column C" % (command, Row+1, SheetName)

                    assert sh.cell(rowx=Row,colx=3).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string in column D" % (command, Row+1, SheetName)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()
                    title = sh.cell(rowx=Row,colx=3).value

                    self.Items[itemname].AddText( time, title )


                elif command in ['XPOS', 'YPOS', 'XPOLE', 'YPOLE', 'XSCALE', 'YSCALE', 'ROTATION', 
                                 'TIMEOFFSET', 'TEXTSIZE', 'OPACITY']:

                    # Set a new x position
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects an item name in column C" % (command, Row+1, SheetName)

                    assert sh.cell(rowx=Row,colx=3).ctype==xlrd.XL_CELL_NUMBER, \
                        "%s at row %d of sheet %s expects a number in column D" % (command, Row+1, SheetName)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()
                    value = sh.cell(rowx=Row,colx=3).value

                    self.Items[itemname].Properties[command].Append(time, value)


                elif command in ['XMOVE', 'YMOVE', 'SXMOVE', 'SYMOVE', 'RMOVE', 'OMOVE']:

                    # Determine linear or cycloid movement
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string in column C" % (command, Row+1, SheetName)

                    assert sh.cell(rowx=Row,colx=3).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string in column D" % (command, Row+1, SheetName)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()
                    move = sh.cell(rowx=Row,colx=3).value.strip().upper()

                    if move in CheckMove:
                        self.Items[itemname].Properties[command].Append(time, CheckMove[move])
                    else:
                        print("Did not recognize type of movement on row %d." % (Row+1))

                elif command in ['TEXTCOLOR', 'FONT']:
                    # Set a new text color
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string in column C" % (command, Row+1, SheetName)

                    assert sh.cell(rowx=Row,colx=3).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string in column D" % (command, Row+1, SheetName)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()
                    textcolor = sh.cell(rowx=Row,colx=3).value.strip()
                    self.Items[itemname].Properties[command].Append(time, textcolor)

                elif command == 'BRINGTOFRONT':
                    # Bring the item to front at this time position
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string in column C" % (command, Row+1, SheetName)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()

                    self.Zbuffer.append( ( time, itemname, FRONT) )

                elif command == 'SENDTOBACK':
                    # Send the item to back at this time position
                    assert sh.cell(rowx=Row,colx=2).ctype==xlrd.XL_CELL_TEXT, \
                        "%s at row %d of sheet %s expects a string in column C" % (command, Row+1, SheetName)

                    itemname = sh.cell(rowx=Row,colx=2).value.upper().strip()
                    self.Zbuffer.append( ( time, itemname, BACK) )

                else:
                    print("Command %s not recognized on row %d." % (command, Row+1))

    def ParseTable(self, FileName, SheetName):

        logging.debug('  Script.ParseTable(%s, %s)' % (FileName, SheetName))

        # Open excel file with frame data
        wb = xlrd.open_workbook(FileName)
        sh = wb.sheet_by_name(SheetName)

        # Investigate which data each column contains
        print(' - parsing table %s' % SheetName)

        for Row in range(2, sh.nrows):

            # Only process rows with a time in the first column
            if sh.cell(rowx=Row,colx=0).ctype==xlrd.XL_CELL_NUMBER:

                time = sh.cell(rowx=Row,colx=0).value

                if self.MaxTime<time: self.MaxTime=time

                for Col in range(1, sh.ncols):

                    # Only process columns with an existing object in the first row and a command in the second row
                    if     sh.cell(rowx=0,colx=Col).ctype==xlrd.XL_CELL_TEXT and \
                        sh.cell(rowx=1,colx=Col).ctype==xlrd.XL_CELL_TEXT and \
                        len(sh.cell(rowx=0,colx=Col).value)>0 and \
                        len(sh.cell(rowx=1,colx=Col).value)>0:

                        itemname = sh.cell(rowx=0,colx=Col).value.upper().strip()
                        command = sh.cell(rowx=1,colx=Col).value.upper().strip()

                        # Only process items that have already been created
                        if itemname in self.Items:

                            item = self.Items[itemname]

                            if command == 'IMAGE':

                                if item.ItemType == IT_IMAGE:

                                    # Assign a new filename for an image item
                                    if sh.cell(rowx=Row,colx=Col).ctype==xlrd.XL_CELL_TEXT:

                                        filename = os.path.join(self.ImageDir, sh.cell(rowx=Row,colx=Col).value)

                                        assert os.path.isfile(filename), \
                                            "%s at row %d could not find file %s" % (command, Row+1, filename)

                                        self.Items[itemname].AddImage( time, filename )

                            elif command == 'MASK':

                                if self.Items[item].ItemType == IT_MASK:
                                    # Assign a new filename for an image item
                                    if sh.cell(rowx=Row,colx=Col).ctype==xlrd.XL_CELL_TEXT:

                                        filename = os.path.join(self.ImageDir, sh.cell(rowx=Row,colx=3).value)

                                        assert os.path.isfile(filename), \
                                            "%s at row %d could not find file %s" % (command, Row+1, filename)

                                        self.Items[itemname].AddMask( time, filename )

                            elif command == 'TEXT':

                                if item.ItemType == IT_TEXT:

                                    # Assign a new title for a text item
                                    if sh.cell(rowx=Row,colx=Col).ctype==xlrd.XL_CELL_TEXT:

                                        text = sh.cell(rowx=Row,colx=Col).value
                                        self.Items[itemname].AddText( time, text )

                            elif command in ['XPOS', 'YPOS', 'XPOLE', 'YPOLE', 'XSCALE', 'YSCALE', 'ROTATION', 
                                             'TIMEOFFSET', 'TEXTSIZE', 'OPACITY']:

                                # Set a new float property
                                if sh.cell(rowx=Row,colx=Col).ctype==xlrd.XL_CELL_NUMBER:
                                    xpos = sh.cell(rowx=Row,colx=Col).value
                                    self.Items[itemname].Properties[command].Append(time, xpos)

                            elif command in ['XMOVE', 'YMOVE', 'SXMOVE', 'SYMOVE', 'RMOVE', 'OMOVE']:
                                # Determine type of movement
                                if sh.cell(rowx=Row,colx=Col).ctype==xlrd.XL_CELL_TEXT:
                                    move = sh.cell(rowx=Row,colx=Col).value.strip().upper()
                                    if move in CheckMove:
                                        self.Items[itemname].Properties[command].Append(time, CheckMove[move])
                                    else:
                                        print("Did not recognize type of movement on row %d." % (Row+1))


                            elif command in ['TEXTCOLOR', 'FONT']:
                                if sh.cell(rowx=Row,colx=Col).ctype==xlrd.XL_CELL_TEXT:
                                    textcolor = sh.cell(rowx=Row,colx=Col).value.strip()
                                    self.Items[itemname].Properties[command].Append(time, textcolor)


                            else:
                                print('Command: ', command)
                                print('Column: ', Col+1)
                                print("Command %s not recognized on col %d." % (command, Col+1))

    def StandardChecks(self):

        print(' - checking script %s which has %d items' % (self.SheetName, len(self.Items) ))

        # Do some standard checks after parsing
        OK = True
        self.TimeOffsetUsed=False
        
        for i in self.Items.values():
            
            i.StandardChecks()

            if i.TimeOffsetUsed:
                self.TimeOffsetUsed=True

            if (i.ItemType == IT_IMAGE):

                if len(i.Properties['IMAGE'].Sequence)==0:

                    print('ERROR: %s has NO images' % i.ItemName)
                    OK=False

                else:

                    for time, filename in i.Properties['IMAGE'].Sequence:

                        if not os.path.isfile(filename):
                            print('Image not found: %s at tim %.3f' % (filename, time))
                            OK = False

            if (i.ItemType == IT_MASK):

                if len(i.Properties['MASK'].Sequence)==0:

                    print('ERROR: %s has NO mask' % i.ItemName)
                    OK=False

                else:

                    for time, filename in i.Properties['MASK'].Sequence:

                        if not os.path.isfile(filename):
                            print('Mask not found: %s at tim %.3f' % (filename, time))
                            OK = False

            if (i.ItemType == IT_TEXT):

                if len(i.Properties['TEXT'].Sequence)==0:
                    print('ERROR: %s has NO lines of text' % i.ItemName)
                    OK=False

        return OK


    def Deploy(self, MaxTime):

        logging.debug('')
        logging.debug('* DEPLOYING SCRIPT %s' % self.SheetName)

        for item in self.Items.values():
            item.Deploy(MaxTime)
            
        if not self.Zbuffer:
            # The Zbuffer has no items because the user did not specify 
            # any BRINGTOFRONT or SENDTOBACK commands
            
            # Get the name of a random item
            itemname = list(self.Items.keys())[0]
            
            self.Zbuffer.append( ( 0, itemname, FRONT) )

        self.Zbuffer.sort()

        time, item, direction = self.Zbuffer[-1]
        self.Zbuffer.append( (MaxTime, item, direction) )
        self.Zbuffer.sort()

        # Determine the order of the items at time = 0
        self.ZbufferIndex = 0

        # list() means we create a copy
        self.Zorder = list(self.Items.keys())


    def GetPicture(self, Time, Frame):

        # If exactly the same image was calculated before,
        # use that image
        #if Frame != self.PictureFrame and not self.TimeOffsetUsed:
        if True:

            logging.debug('')
            logging.debug('* SCRIPT %s IS GENERATING FRAME %.5d at time %.2f' % (self.SheetName, Frame, Time ))            

            # Start with a transparent image
            if (not self.IsCanvas) or self.FirstImage:
                self.Picture = Image.new("RGBA", (self.Width, self.Height), (255,0,0,0) )

            self.FirstImage=False

            # Determine the Z-order at the desired time
            while True:

                time, item, direction = self.Zbuffer[self.ZbufferIndex]

                if item not in self.Zorder:
                    print('Z-order failure: item %s not in script %s' % (item, self.SheetName) )

                self.Zorder.remove(item)

                if direction == FRONT:
                    self.Zorder.append(item)
                else:
                    self.Zorder.insert(0, item)

                if (self.Zbuffer[self.ZbufferIndex+1][0])>Time:
                    break
                else:
                    self.ZbufferIndex+=1

                
            ItemPicture = Image.new("RGBA", (self.Width, self.Height), (255,0,0,0) )

            # Draw each item
            for itemname in self.Zorder:

                Item = self.Items[itemname]

                move    = Item.Properties['OMOVE'   ].Value(Time)
                opacity = Item.Properties['OPACITY' ].Value(Time, move)

                move    = Item.Properties['XMOVE'   ].Value(Time)
                xpos    = Item.Properties['XPOS'    ].Value(Time, move)

                move    = Item.Properties['YMOVE'   ].Value(Time)
                ypos    = Item.Properties['YPOS'    ].Value(Time, move)

                move    = Item.Properties['SXMOVE'  ].Value(Time)
                sx      = Item.Properties['XSCALE'  ].Value(Time, move)

                move    = Item.Properties['SYMOVE'  ].Value(Time)
                sy      = Item.Properties['YSCALE'  ].Value(Time, move)

                move    = Item.Properties['RMOVE'   ].Value(Time)
                rot     = Item.Properties['ROTATION'].Value(Time, move)

                try:
                    logging.debug('  - Item %s:%s xpos= %.2f ypos= %.2f xscale= %.3f yscale= %.3f rot= %.3f opacity= %.3f' % (self.SheetName, itemname, xpos, ypos, sx, sy, rot, opacity))
                except:
                    print('opacity', opacity)
                    print('xpos', xpos)
                    print('ypos', ypos)
                    print('sx', sx)
                    print('sy', sy)
                    print('rot', rot)

                if opacity>0:

                    if Item.ItemType == IT_ASSY:

                        script = Item.Properties['SCRIPT'].Value(Time)
                        logging.debug('  - Assembly %s:%s requests an image from script %s' % (self.SheetName, itemname, script))

                        if script in self.ScriptList:
                            dt=Item.Properties['TIMEOFFSET'].Value(Time, LINEAR)
                            ItemPicture = self.ScriptList[script].GetPicture(Time-dt, Frame)
                        else:
                            logging.debug('  Script %s not in scriptlist!!:'% (script))
                            ItemPicture = Image.new("RGBA", (self.Width, self.Height), (255,0,0,0) )
                            
                        logging.debug('  Assembly %s continues:'% (self.SheetName))

                    if Item.ItemType == IT_CANVAS:

                        script = Item.Properties['SCRIPT'].Value(Time)
                        logging.debug('  - Canvas %s:%s requests an image from script %s' % (self.SheetName, itemname, script))

                        if script in self.ScriptList:
                            dt=Item.Properties['TIMEOFFSET'].Value(Time, LINEAR)
                            ItemPicture = self.ScriptList[script].GetPicture(Time-dt, Frame)
                        else:
                            ItemPicture = Image.new("RGBA", (self.Width, self.Height), (255,0,0,0) )

                    elif Item.ItemType == IT_IMAGE:

                        image = Item.Properties['IMAGE'].Value(Time)

                        if Item.PrevImageName != image:
                            Item.LoadedImage = Image.open(image).convert("RGBA")
                            Item.PrevImageName = image

                        ItemPicture = Item.LoadedImage


                    elif Item.ItemType == IT_MASK:

                        image = Item.Properties['MASK'].Value(Time)
                        logging.debug('Line 585 mask is %s' % image)

                        if Item.PrevImageName != image:
                            Item.LoadedImage = Image.open(image).convert("RGBA")
                            Item.PrevImageName = image

                        ItemPicture = Item.LoadedImage

                    elif Item.ItemType == IT_TEXT:

                        ItemPicture = Image.new("RGBA", (self.Width, self.Height), (255,0,0,0) )

                        text      = Item.Properties['TEXT'     ].Value(Time)
                        textsize  = int(Item.Properties['TEXTSIZE' ].Value(Time, LINEAR))
                        textcolor = Item.Properties['TEXTCOLOR'].Value(Time)
                        fontname  = Item.Properties['FONT'     ].Value(Time)

                        Directories = [ 'C:\\WINDOWS\\Fonts\\' ]
                        Fonts = [fontname, 'calibri.ttf', 'YanoneKaffeesatz-Regular.ttf', 'ARIALN.TTF', 'verdana.ttf', 'YanoneKaffeesatz-Light.ttf']

                        Face = ImageFont.truetype(SelectFont(Directories, Fonts), textsize)
                        Draw = ImageDraw.Draw(ItemPicture)
                        Draw.text( (0,0), text, fill=textcolor, font=Face)

                    # Retrieve the general properties
                    move  = Item.Properties['XMOVE'   ].Value(Time)
                    xpos  = Item.Properties['XPOS'    ].Value(Time, move)

                    move  = Item.Properties['YMOVE'   ].Value(Time)
                    ypos  = Item.Properties['YPOS'    ].Value(Time, move)

                    move  = Item.Properties['SXMOVE'  ].Value(Time)
                    sx    = Item.Properties['XSCALE'  ].Value(Time, move)
                    xpole = Item.Properties['XPOLE'   ].Value(Time, move)

                    move  = Item.Properties['SYMOVE'  ].Value(Time)
                    sy    = Item.Properties['YSCALE'  ].Value(Time, move)
                    ypole = Item.Properties['YPOLE'   ].Value(Time, move)

                    move  = Item.Properties['RMOVE'   ].Value(Time)
                    rot   = Item.Properties['ROTATION'].Value(Time, move)

                    fi    = math.pi/180*rot
                    sinfi = math.sin(fi)
                    cosfi = math.cos(fi)

                    w,h = ItemPicture.size

                    # Resize and rotate the ItemPicture
                    try:
                        ItemPicture=ItemPicture.resize( (int(sx*w+0.5), int(sy*h+0.5) ), Image.ANTIALIAS)
                        ItemPicture=ItemPicture.rotate(rot, expand=1)
                    except:
                        print('ERROR Script 663: Item %s:%s sx= %.2f sy= %.2f' % (self.SheetName, itemname, sx, sy))
                        break

                    wr,hr = ItemPicture.size

                    xt = xpos + xpole - ypole*sy*sinfi - xpole*sx*cosfi +0.5*w*sx*cosfi +0.5*h*sy*sinfi -0.5*wr
                    yt = ypos + ypole - ypole*sy*cosfi + xpole*sx*sinfi -0.5*w*sx*sinfi +0.5*h*sy*cosfi -0.5*hr

                    Mask = ItemPicture.convert("RGBA")
                    Mask = Image.blend(Image.new(ItemPicture.mode, ItemPicture.size, 0), ItemPicture, opacity)

                    if Item.ItemType != IT_MASK:

                        # Item is picture, assembly or canvas
                        self.Picture.paste( ItemPicture, (int(xt),int(yt)), Mask )

                    else:

                        # Item is mask
                        logging.debug('  - Applying mask for %s' % itemname)

                        # Start with a clean image with transparent background
                        CleanImage = Image.new("RGBA", (self.Width, self.Height), (0,0,0,0) )

                        # Use the mask rotated and translated
                        Mask = Image.new("L", (self.Width, self.Height), 0 )
                        Mask.paste( ItemPicture, (int(xt),int(yt)))

                        # Copy the image as-is with rotation and translation set to zero
                        CleanImage.paste( self.Picture, (0,0), Mask )

                        self.Picture = CleanImage.copy()

            self.PictureFrame = Frame

        return self.Picture.copy()
