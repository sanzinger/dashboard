import wx, widgets

class Example(wx.Frame):
    def __init__(self, parent, title, full=False):
        super(Example, self).__init__(parent, title=title)

        
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("#000000")
        
        
        self.rpm = widgets.RPMGauge(bars=30, mode=widgets.RPMGauge.MODE_LOG, orient=widgets.RPMGauge.ORIENT_HORIZONTAL)
        self.rpm2 = widgets.RPMGauge(bars=10, mode=widgets.RPMGauge.MODE_LINEAR, orient=widgets.RPMGauge.ORIENT_VERTICAL);
        self.text1 = widgets.TextGauge((0,0), (.1,.1))
        self.text2 = widgets.TextGauge((0,0), (.4,.1))
        self.text2.value = "HALLO"
        
        self.rpmPanel = widgets.PanelWrapper(panel, -1, (300,200))
        self.rpmPanel.addPainter(self.rpm, position=(0,-.050), size=(1,.8))
        #self.rpmPanel.addPainter(self.rpm, position=(0,0.7), size=(1,.2))
        #self.rpmPanel.addPainter(self.rpm2, position=(.05,.7), size=(.1,.3))
        #self.rpmPanel.addPainter(self.rpm2, position=(.25,.7), size=(.1,.3))
        self.rpmPanel.addPainter(self.text1, position=(.30, .7), size=(.1, .1))
        #self.rpmPanel.addPainter(self.text2, position=(.50, .7), size=(.1, .05))
        #CenterPanel = wx.Panel(panel, -1)
        self.sld = wx.Slider(panel, -1, 75, 0, 100, (-1, -1), (250, -1), wx.SL_LABELS)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.rpmPanel, 5, wx.EXPAND)
        vbox.Add(self.sld, 1, wx.EXPAND)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyUP)
        self.Bind(wx.EVT_SCROLL, self.onScroll)
        self.update()
        
        if full:
            self.ShowFullScreen(True, style=wx.FULLSCREEN_ALL)
            panel.SetFocus()
        else:
            self.Centre()
            self.Show()
            
    def update(self):
        self.rpm.value = float(self.sld.GetValue())/100
        self.rpm2.value = 1-float(self.sld.GetValue())/100
        self.text1.value = str(self.sld.GetValue()) + " rpm"
        
    def onScroll(self, event):
        self.update()
        self.rpmPanel.Refresh()
        
    def onKeyUP(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.Close()



if __name__ == '__main__':
    app = wx.App()
    Example(None, 'RPM', full=False)
    app.MainLoop()