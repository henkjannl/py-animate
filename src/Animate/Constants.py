import math

# Item types
IT_BASE   = "BAS"
IT_IMAGE  = "IMG"
IT_CANVAS = "CNV"
IT_MASK   = "MSK"
IT_TEXT   = "TXT"
IT_ASSY   = "ASS"

# Commands
ScriptCommands         = ['WIDTH', 'HEIGHT', 'FRAMESPERSECOND', 'FIRSTFRAME', 'LASTFRAME', 'SHOWTIME', 'HIDETIME', 
                          'TIMEOFFSET', 'TABLE', 'SCRIPT']
AnalogProperties       = ['XPOS', 'YPOS', 'XPOLE', 'YPOLE', 'XSCALE', 'YSCALE', 'ROTATION', 'OPACITY']
MoveCommands           = ['XMOVE', 'YMOVE', 'SXMOVE', 'SYMOVE', 'RMOVE', 'OMOVE']
ZorderCommands         = ['BRINGTOFRONT', 'SENDTOBACK']
AnalogTextProperties   = ['TEXTSIZE']
DiscreteTextProperties = ['TEXTCOLOR', 'FONT']
DiscreteProperties     = ['ASSEMBLY', 'IMAGE', 'CANVAS', 'MASK', 'TEXT']

# Default font
DEFAULTFONT = "C:\\WINDOWS\\Fonts\\verdana.TTF"
#DEFAULTFONT = "Verdana.ttf"

    
# BringToFront or SendToBack
FRONT = 0
BACK  = 1

# Interpolation of position and rotation
LINEAR  = 0
CYCLOID = 1
SPRING  = 2
CLICK   = 3
ACCEL   = 4
DAMPED  = 5
SUDDEN  = 6

CheckMove = {   'LINEAR' : LINEAR,
                'CYCLOID': CYCLOID,
                'SPRING' : SPRING,
                'CLICK'  : CLICK,
                'ACCEL'  : ACCEL,
                'DAMPED' : DAMPED,
                'SUDDEN' : SUDDEN   }

# Types and default values for all properties
DISCRETE = 0
ANALOG   = 1

DEFAULTVALUES = [   ('XPOS'      , ANALOG  , 0             ),
                    ('XMOVE'     , DISCRETE, LINEAR        ),
                    ('XSCALE'    , ANALOG  , 1             ),
                    ('SXMOVE'    , DISCRETE, LINEAR        ),
                    ('YPOS'      , ANALOG  , 0             ),
                    ('YMOVE'     , DISCRETE, LINEAR        ),
                    ('YSCALE'    , ANALOG  , 1             ),
                    ('SYMOVE'    , DISCRETE, LINEAR        ),
                    ('ROTATION'  , ANALOG  , 0             ),
                    ('RMOVE'     , DISCRETE, LINEAR        ),
                    ('XPOLE'     , ANALOG  , 0             ),
                    ('YPOLE'     , ANALOG  , 0             ),
                    ('OPACITY'   , ANALOG  , 1             ),
                    ('OMOVE'     , DISCRETE, LINEAR        ),
                    ('TIMEOFFSET', ANALOG  , 0             ),
                    ('IMAGE'     , DISCRETE, ''            ),
                    ('CANVAS'    , DISCRETE, ''            ),
                    ('MASK'      , DISCRETE, ''            ),
                    ('TEXT'      , DISCRETE, ''            ),
                    ('TEXTCOLOR' , DISCRETE, 'BLACK'       ),
                    ('TEXTSIZE'  , ANALOG  , 12            ),
                    ('FONT'      , DISCRETE, 'verdana.ttf' ),
                    ('SCRIPT'    , DISCRETE, ''            ) ]

def Displacement(interpolation, x):

    if interpolation == LINEAR:
        return x

    elif interpolation == CYCLOID:
        return x - 1/(2*math.pi)*math.sin(2*math.pi*x)
        
    elif interpolation == SPRING:
        return (441.8214882*x**8 - 1703.935071*x**7 + 2530.182847*x**6 - 
            1771.030096*x**5 + 561.4457127*x**4 - 62.98225215*x**3 + 
            5.597813989*x**2 - 0.09284320409*x - 0.000440360649)
            
    elif interpolation == CLICK:
        return x-0.4052443*math.sin(2*math.pi*x)+0.1453085*math.sin(4*math.pi*x)

    elif interpolation == ACCEL:
        return x**2

    elif interpolation == DAMPED:
        return 1-(1-x)**2

    elif interpolation == SUDDEN:
        if x<1:
            return 0
        else:
            return 1





