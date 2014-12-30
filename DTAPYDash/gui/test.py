import wx, widgets

class Example(wx.Frame):
    def __init__(self, parent, title, full=False):
        super(Example, self).__init__(parent, title=title)

        
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("#000000")
        
        
        self.rpm = widgets.RPMGauge(panel, -1, (200,350), bars=100, mode=widgets.RPMGauge.MODE_LOG, orient=widgets.RPMGauge.ORIENT_VERTICAL)
        #CenterPanel = wx.Panel(panel, -1)
        self.sld = wx.Slider(panel, -1, 75, 0, 100, (-1, -1), (250, -1), wx.SL_LABELS)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.rpm, 5, wx.EXPAND)
        vbox.Add(self.sld, 1, wx.EXPAND)
        panel.SetSizer(vbox)
        """
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        
        
        hbox.Add(self.rpm, 1, wx.EXPAND)

        hbox2.Add(CenterPanel, 1, wx.EXPAND)
        hbox3.Add(self.sld, 0, wx.TOP)

        CenterPanel.SetSizer(hbox3)

        vbox.Add(hbox, 7, wx.EXPAND)
        vbox.Add(hbox2, 1, wx.EXPAND)

        
        
        panel.SetSizer(vbox)
        """
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
        
    def onScroll(self, event):
        self.update()
        self.rpm.Refresh()
        
    def onKeyUP(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.Close()



if __name__ == '__main__':
    app = wx.App()
    Example(None, 'RPM', full=True)
    app.MainLoop()