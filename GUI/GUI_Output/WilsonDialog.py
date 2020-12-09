#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.4 on Sat Nov 28 18:18:52 2020
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class wilsonDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wilsonDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.sos = wx.StaticText(self, wx.ID_ANY, "label_17")
        self.freqctrl = wx.SpinCtrl(self, wx.ID_ANY, "500", min=0, max=1000)
        self.tempctrl = wx.SpinCtrl(self, wx.ID_ANY, "18", min=0, max=20)
        self.salinctrl = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=100)
        self.depthctrl = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=100)
        self.okButton = wx.Button(self, wx.ID_OK, "")
        self.cancelButton = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_SPINCTRL, self.tempchanged, self.tempctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.temptyped, self.tempctrl)
        self.Bind(wx.EVT_SPINCTRL, self.salinchanged, self.salinctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.salintyped, self.salinctrl)
        self.Bind(wx.EVT_SPINCTRL, self.depthchanged, self.depthctrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.depthtyped, self.depthctrl)
        self.Bind(wx.EVT_BUTTON, self.okPressed, self.okButton)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wilsonDialog.__set_properties
        self.SetTitle("Configure Sound Wave")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wilsonDialog.__do_layout
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.GridSizer(5, 2, 0, 0)
        label_13 = wx.StaticText(self, wx.ID_ANY, "Speed of Sound")
        grid_sizer_2.Add(label_13, 0, 0, 0)
        grid_sizer_2.Add(self.sos, 0, 0, 0)
        label_14 = wx.StaticText(self, wx.ID_ANY, "Frequency")
        grid_sizer_2.Add(label_14, 0, 0, 0)
        grid_sizer_2.Add(self.freqctrl, 0, 0, 0)
        label_16 = wx.StaticText(self, wx.ID_ANY, "Temperature")
        grid_sizer_2.Add(label_16, 0, 0, 0)
        grid_sizer_2.Add(self.tempctrl, 0, 0, 0)
        label_18 = wx.StaticText(self, wx.ID_ANY, "Salinity")
        grid_sizer_2.Add(label_18, 0, 0, 0)
        grid_sizer_2.Add(self.salinctrl, 0, 0, 0)
        label_17 = wx.StaticText(self, wx.ID_ANY, "Depth")
        grid_sizer_2.Add(label_17, 0, 0, 0)
        grid_sizer_2.Add(self.depthctrl, 0, 0, 0)
        sizer_13.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        sizer_12.Add(sizer_13, 1, wx.EXPAND, 0)
        sizer_15.Add(self.okButton, 0, wx.ALIGN_BOTTOM | wx.ALL, 2)
        sizer_15.Add(self.cancelButton, 0, wx.ALIGN_BOTTOM | wx.BOTTOM | wx.RIGHT | wx.TOP, 2)
        sizer_12.Add(sizer_15, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_12)
        sizer_12.Fit(self)
        self.Layout()
        # end wxGlade

    def tempchanged(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'tempchanged' not implemented!")
        event.Skip()

    def temptyped(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'temptyped' not implemented!")
        event.Skip()

    def salinchanged(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'salinchanged' not implemented!")
        event.Skip()

    def salintyped(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'salintyped' not implemented!")
        event.Skip()

    def depthchanged(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'depthchanged' not implemented!")
        event.Skip()

    def depthtyped(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'depthtyped' not implemented!")
        event.Skip()

    def okPressed(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'okPressed' not implemented!")
        event.Skip()

# end of class wilsonDialog

class MyApp(wx.App):
    def OnInit(self):
        self.mainFrame = wilsonDialog(None, wx.ID_ANY, "")
        self.SetTopWindow(self.mainFrame)
        self.mainFrame.ShowModal()
        self.mainFrame.Destroy()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()