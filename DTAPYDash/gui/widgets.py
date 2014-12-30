import wx, math


class RPMGauge(wx.Panel):
    MODE_LOG = 1
    MODE_LINEAR = 2
    ORIENT_VERTICAL = 1
    ORIENT_HORIZONTAL = 2
    
    def __init__(self, parent, id, size=(80, 110), bars=8, mode=MODE_LOG, orient=ORIENT_VERTICAL):
        wx.Panel.__init__(self, parent, id, size=size)
        self.parent = parent
        self.SetBackgroundColour('#000000')
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.bars = bars
        self.value = 0
        self.mode = mode
        self.orientation = orient
    
    def onPaint(self, event):
        dc = wx.PaintDC(self)
        isVertical = self.orientation == RPMGauge.ORIENT_VERTICAL
        w,h = self.GetSize()
        
        if self.mode == RPMGauge.MODE_LOG:
            x1 = lambda x: 1.0-math.log(1.2)/math.log(1.2+1*x)
            x2 = lambda x: 1.0-math.log(1.05)/math.log(1.05+1*x)
        else:
            x1 = lambda x: 0.0
            x2 = lambda x: 1.0
        
        dc.SetDeviceOrigin(0, h)
        dc.SetAxisOrientation(True, True)
        value = self.value
        redArea = .8
        yellowArea = .7
        barSpaceRatio = .2
        if isVertical: (w, h) = (h,w)
        barDistance = ((w*(1+barSpaceRatio/self.bars) / self.bars))
        barWidth = ((barDistance * (1.0-barSpaceRatio)))
        
        def colorBars(x):
            if x > redArea:
                return "#FF0000" if value > x else "#730000"
            if x > yellowArea:
                return "#FFFF00" if value > x else "#808000"
            else:
                return "#36ff27" if value > x else "#075100"
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
        
    def onSize(self, event):
        self.Refresh()
  