from ..GUI_Output import wilsonDialog

class wilsonDialogController(wilsonDialog):

    def __init__(self, app, *args, **kwds):

        self.app = app
        super().__init__(*args, **kwds)
        self.setValues()


    def wilsonEquation(self, update = False):

        temperature = self.tempctrl.GetValue()
        salinity = self.salinctrl.GetValue()
        depth = self.depthctrl.GetValue()

        sos = 1449 + 4.6*temperature - 0.055*(temperature**2) + 1.39*(salinity - 35) + 0.017*depth

        self.sos.SetLabel(str(sos))

        if update:
            self.app.window.sos = sos

    def setValues(self):

        self.sos.SetLabel(str(self.app.window.sos))
        self.freqctrl.SetValue(self.app.window.frequency)
        self.tempctrl.SetValue(self.app.window.temperature)
        self.salinctrl.SetValue(self.app.window.salinity)
        self.depthctrl.SetValue(self.app.window.depth)

    def tempchanged(self, event):
        self.wilsonEquation()

    def temptyped(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'temptyped' not implemented!")
        event.Skip()

    def salinchanged(self, event):  # wxGlade: wilsonDialog.<event_handler>
        self.wilsonEquation()

    def salintyped(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'salintyped' not implemented!")
        event.Skip()

    def depthchanged(self, event):  # wxGlade: wilsonDialog.<event_handler>
        self.wilsonEquation()
        event.Skip()

    def depthtyped(self, event):  # wxGlade: wilsonDialog.<event_handler>
        print("Event handler 'depthtyped' not implemented!")
        event.Skip()

    def okPressed(self, event):  # wxGlade: wilsonDialog.<event_handler>
        self.wilsonEquation(True)

        self.app.window.frequency = self.freqctrl.GetValue()
        self.app.window.temperature = self.tempctrl.GetValue()
        self.app.window.salinity = self.salinctrl.GetValue()
        self.app.window.depth = self.depthctrl.GetValue()

        self.Close()
