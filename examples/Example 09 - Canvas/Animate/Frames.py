# Item types
IT_ASSEMBLY = "ASS"
IT_IMAGE    = "IMG"
IT_MASK     = "MSK"
IT_TEXT     = "TXT"

class Frame():
    def __init__(self):
        self.ItemName = ''
        self.Time = 0.000
        self.ItemType = IT_IMAGE
        self.Image = '' # Used as filename or as text to be displayed
        self.Font = 'Verdana.ttf'
        self.Xpos = 0
        self.Ypos = 0
        self.Xscale = 1.0
        self.Yscale = 1.0
        self.Rotation = 0
        self.Xpole = 0
        self.Ypole = 0
        self.TextSize = 0
        self.TextColor = 'BLACK'        
        self.Opacity = 1
        self.ZOrder = 0

def Zsorter(Frame1, Frame2):
    # Sort frames, based on Z order
    if Frame1.ZOrder<Frame2.ZOrder:
        return 1
    else:
        if Frame1.ZOrder>Frame2.ZOrder:
            return -1
        else:
            return 0
