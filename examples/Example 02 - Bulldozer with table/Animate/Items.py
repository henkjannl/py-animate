
from PIL import Image                         # www.pythonware.com/library/pil/handbook
import math

import logging

from Animate.Properties import *
from Animate.Constants import *

'''
The different types of item are deliberately no subclasses of Item,
because at the time of creation, the type of item may not be known.
For instance, if first XPOS of an item is given, and then IMAGE.

Therefore, all items are the same and ItemType determines the type of
item. ItemType can be changed after creation without ruining the
properties already parsed.
'''



class Item(object):
    ''' Each distinct object of the animation is stored as an item.

        The item class defines all changes on every property for one item.
        Every property has its own timeline, independent of the timelines
        of the other properties.
        The timeline is a list of (time, property) tuples, which are lateron
        transferred to discrete, equidistant frames '''

    def __init__(self):
        self.ItemName = ''
        self.ItemType = IT_BASE
        self.SheetName = ''
        
        self.TimeOffsetUsed = False

        self.Properties = {}

        # Create all properties
        for name, kind, default in DEFAULTVALUES:

            if kind == DISCRETE:
                self.Properties[name] = DiscreteProperty()
            else:
                self.Properties[name] = AnalogProperty()

        self.PrevImageName = ''
        self.LoadedImage = None


    def StandardChecks(self):
        self.TimeOffsetUsed = (len(self.Properties['TIMEOFFSET'].Sequence)>0)
        
        # To do: more checks can be done, such as checking of images exist
        
    def AddImage(self, time, filename):

        self.ItemType = IT_IMAGE
        self.Properties['IMAGE'].Append(time, filename)

    def AddMask(self, time, filename):

        self.ItemType = IT_MASK
        self.Properties['MASK'].Append(time, filename)

    def AddText(self, time, text):

        self.ItemType = IT_TEXT
        self.Properties['TEXT'].Append(time, text)

    def AddScript(self, time, script):

        self.ItemType = IT_ASSY
        self.Properties['SCRIPT'].Append(time, script)

    def AddCanvas(self, time, script):

        self.ItemType = IT_CANVAS
        self.Properties['SCRIPT'].Append(time, script)

    def Deploy(self, MaxTime):

        # Prepare each property for first use
        for name, kind, default in DEFAULTVALUES:
            self.Properties[name].Deploy(MaxTime, default)


class ItemDict(dict):
    def __init__(self, *args):
        dict.__init__(self, args)

    def __getitem__(self, key):

        if key not in self.keys():
            newitem = Item()
            newitem.ItemName = key

            dict.__setitem__(self, key, newitem)
            
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):

        dict.__setitem__(self, key, val)
