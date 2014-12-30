import wx, math

class PanelWrapper(wx.Panel):
    def __init__(self, parent, id=-1, size=(80, 110)):
        wx.Panel.__init__(self, parent, id, size=size)
        self.parent = parent
        self.painters = []
        
        self.SetBackgroundColour('#000000')
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)
        
    def addPainter(self, painter, position=(0,0), size=(1.0,1.0)):
        self.painters.append((painter, position, size))
    
    def onPaint(self, event):
        dc = wx.PaintDC(self)
        w,h = self.GetSize()
        for i in self.painters:
            painter, position, size = i
            painter.setSize((size[0]*w, size[1]*h))
            painter.setPosition((position[0]*w, position[1]*h))
            painter.paint(dc)
    
    def onSize(self, event):
        self.Refresh()
    

class Painter:
    def __init__(self, position=(0,0), size=(80, 110)):
        self.size = size
        self.position = position
    
    def setSize(self, size):
        self.size = size
    
    def setPosition(self, position):
        self.position = position
    
    
class TextGauge(Painter):
    def __init__(self, position=(0,0), size=(80, 110)):
        Painter.__init__(self, position, size)
        self.value = "asdf"
        
    
    def paint(self, dc):
        """
        @type dc: wx.PaintDC
        """
        w,h = self.size
        dc.SetTextForeground("#36ff27")
        dc.SetFont(wx.Font(self.size[1], wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))
        dc.SetDeviceOrigin(self.position[0], self.position[1]+h)
        dc.SetAxisOrientation(True, True)
        dc.DrawText(str(self.value), self.size[0], self.size[1])
        pass
    
    def setValue(self, value):
        self.value = value
    
    
        
class RPMGauge(Painter):
    MODE_LOG = 1
    MODE_LINEAR = 2
    ORIENT_VERTICAL = 1
    ORIENT_HORIZONTAL = 2
    
    def __init__(self, position=(0,0), size=(80, 110), bars=8, mode=MODE_LOG, orient=ORIENT_VERTICAL):
        #self.size = size
        #self.position = position
        Painter.__init__(self, position, size)
        self.bars = bars
        self.value = 0
        self.mode = mode
        self.orientation = orient
    
    def paint(self, dc):
        isVertical = self.orientation == RPMGauge.ORIENT_VERTICAL
        w,h = self.size
        
        if self.mode == RPMGauge.MODE_LOG:
            x1 = lambda x: 1.0-math.log(1.2)/math.log(1.2+1*x)
            x2 = lambda x: 1.0-math.log(1.05)/math.log(1.05+1*x)
        else:
            x1 = lambda x: 0.0
            x2 = lambda x: 1.0
        
        def colorBars(x):
            if x > redArea:
                return "#FF0000" if value > x else "#730000"
            if x > yellowArea:
                return "#FFFF00" if value > x else "#808000"
            else:
                return "#36ff27" if value > x else "#075100"
            
        dc.SetDeviceOrigin(self.position[0], self.position[1]+h)
        dc.SetAxisOrientation(True, True)
        value = self.value
        redArea = .8
        yellowArea = .7
        barSpaceRatio = .2
        if isVertical: (w, h) = (h,w)
        barDistance = ((w*(1+barSpaceRatio/self.bars) / self.bars))
        barWidth = ((barDistance * (1.0-barSpaceRatio)))
        
        color = colorBars
        for i in range(0, self.bars):
            prc = .0001 + float(i+.5)/self.bars
            dc.SetBrush(wx.Brush(color(prc)))
            bottom = h * x1(prc)
            top = h * x2(prc) - bottom
            if isVertical:
                dc.DrawRectangle(bottom, i*barDistance, top, barWidth)
            else:
                dc.DrawRectangle(i*barDistance, bottom, barWidth, top)
  