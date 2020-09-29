import PanelDialog as pd
import wx

class panelDialogController(pd.panelDialog):

    def cancelPressed(self, event):
        print("Cancel")
        self.Close()

    def okPressed(self, event):
        print("OK")
        self.Close()
