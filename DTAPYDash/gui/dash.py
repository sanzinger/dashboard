import wx, widgets, DTALib, thread, serial

class Dash(wx.Frame):
    def __init__(self, parent, title, full=False):
        super(Dash, self).__init__(parent, title=title)
        self.frame = None
        
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("#000000")
        
        
        self.rpm = widgets.RPMGauge(bars=100, mode=widgets.RPMGauge.MODE_LOG, orient=widgets.RPMGauge.ORIENT_HORIZONTAL)
        self.rpmText = widgets.TextGauge((0,0), (.1,.1))
        self.voltText = widgets.TextGauge((0,0), (.1,.1))
        
        self.rpmPanel = widgets.PanelWrapper(panel, -1, (500,200))
        self.rpmPanel.addPainter(self.rpm, position=(0,-.050), size=(1,.8))
        self.rpmPanel.addPainter(self.rpmText, position=(.5, .4), size=(.1, .08))
        self.rpmPanel.addPainter(self.voltText, position=(.50, .7), size=(.1, .08))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.rpmPanel, 5, wx.EXPAND)
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
        frame = self.frame
        if frame and "rpm" in frame.keys:
            
            self.rpmText.value = str(frame.getValue("rpm")) + " rpm"
            
        if frame and "volts" in frame.keys:
            self.rpm.value = float(frame.getValue("volts"))/180
            self.voltText.value = str(frame.getValue("volts")/10.0 if frame else "N/A") + " V"
        
        
    def setFrame(self, frame):
        self.frame = frame
        self.update()
        self.Refresh()
        
    def onScroll(self, event):
        self.update()
        self.rpmPanel.Refresh()
        
    def onKeyUP(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.Close()
            
def updater(output):
    """
    @type output: Dash
    """
    ser = serial.Serial('/dev/ttyUSB0', 1228800)
    try:
        client = DTALib.DTALib.CanClient(ser)
        p = DTALib.DTALib.DTAFrameParser()
        i = 0;
        while True:
            frame = client.readMessage()
            dtaFrame = p.parse(frame)
            output.setFrame(dtaFrame)
    finally:
            ser.close()

if __name__ == '__main__':
    app = wx.App()
    dash  = Dash(None, 'Dash', full=False)
    thread.start_new_thread(updater,(dash,))
    app.MainLoop()