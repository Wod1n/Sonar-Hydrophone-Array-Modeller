import wx
import GUI.Controllers as gui

class windowApp(wx.App):
    """
    Overall app holding all the window and dialog objects
    """

    def OnInit(self):
        """
        Opens the Main Window on initialisation
        """
        self.window = gui.MainWindowController(self, None, wx.ID_ANY, "")
        self.window.Show()
        return True

    def panelDialog(self):
        """
        Opens the Panel Dialog as a dialog box when the button is pressed in the Main Window
        """
        self.dialog = gui.panelDialogController(self, None, wx.ID_ANY, "")
        self.dialog.configureSize()
        self.dialog.Show()

    def presetDialog(self):
        """
        Opens the Preset Dialog as a dialog box when the button is pressed in the Main Window
        """
        self.dialog = gui.presetDialogController(self, None, wx.ID_ANY, "")
        self.dialog.Show()

    def wilsonDialog(self):
        self.dialog = gui.wilsonDialogController(self, None, wx.ID_ANY, "")
        self.dialog.Show()

if __name__ == "__main__":
    app = windowApp(0)
    app.MainLoop()
