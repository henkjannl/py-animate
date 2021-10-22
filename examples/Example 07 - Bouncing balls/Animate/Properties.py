from Animate.Constants import *

class DiscreteProperty(object):

    def __init__(self):
        self.Sequence=[]

    def Append(self, time, value):
        self.Sequence.append( (time, value) )

    def Deploy(self, MaxTime, DefaultValue):

        # Sort the list
        self.Sequence.sort()

        # Insert a point if no points are present
        if len(self.Sequence)==0:
            self.Sequence.append( (0, DefaultValue) )

        # Insert a point at t=0 if needed
        if self.Sequence[0][0]>0:
            FirstValue = self.Sequence[0][1]
            self.Sequence.insert( 0, (0, FirstValue) )

        # Determine the last value in the list (for FRAMESPERSECOND etc.)
        self.LastValue = self.Sequence[-1][1]

        # Append a point at t=MaxTime if needed
        if self.Sequence[-1][0]<MaxTime:
            self.Sequence.append( (MaxTime, self.LastValue) )
            

    def Value(self, time):

        # requested time is before the start of the sequence
        t0, y0 = self.Sequence[0]
        if time<t0:
            return y0
        
        # requested time is after the end of the sequence
        t1, y1 = self.Sequence[-1]
        if t1<time:
            return y1
        
        # requested time is somewhere in between
        for t1,y1 in self.Sequence[1:]:
            
            if t0<=time<=t1:
                return y0
            
            t0, y0 = t1, y1
            
        return 0


class AnalogProperty(DiscreteProperty):

    def Value(self, time, interpolation):

        # requested time is before the start of the sequence
        t0, y0 = self.Sequence[0]
        if time<=t0:
            return y0
        
        # requested time is after the end of the sequence
        t1, y1 = self.Sequence[-1]
        if time>=t1:
            return y1
        
        # requested time is somewhere in between
        for t1,y1 in self.Sequence[1:]:

            if t0<=time<=t1:
                try:
                    relativevalue = Displacement(interpolation, (time-t0) / (t1-t0) )
                    result=y0+relativevalue*(y1-y0)
                except:
                    print("Error in properties line 76")
                    print("interpolation={inter} time={tim} t0={t0} t1={t1}".format(inter=interpolation, tim=time, t0=t0, t1=t1))
                    print("y1={y1} relative={rel} y0={y0}".format(y1=y1, rel=relativevalue, y0=y0))
                    exit(0)
                return result
            
            t0=t1
            y0=y1
        
        # No values in sequence
        return 0