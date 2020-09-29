import MainWindow as mw
import PanelDialogController as pdc
import wx
import numpy as np

class MainFrameController(mw.MainFrame):

    def __init__(self, *args, **kwds):

        self.xnumber = 1
        self.xspacing = 1
        self.ynumber = 1
        self.yspacing = 1

        self.updateFailedArray()

        super().__init__(*args, **kwds)

    def quitPressed(self, event):
        print("quitting")
        exit()

    def panelButtonPressed(self, event):
        app.panelDialog()

    def xnumberSliderChanged(self, event):
        self.xnumber = self.xnumberSlider.GetValue()
        self.xnumberSpinBox.SetValue(self.xnumber)
        self.updateFailedArray()

    def xnumberSpinBoxChanged(self, event):
        self.xnumber = self.xnumberSpinBox.GetValue()
        self.xnumberSlider.SetValue(self.xnumber)
        self.updateFailedArray()

    def xspacingSliderChanged(self, event):
        self.xspacing = self.xspacingSlider.GetValue()
        self.xspacingSpinBox.SetValue(self.xspacing)
        self.updateFailedArray()

    def xspacingSpinBoxChanged(self, event):
        self.xspacing = self.yspacingSpinBox.GetValue()
        self.yspacingSlider.SetValue(self.xspacing)
        self.updateFailedArray()

    def ynumberSliderChanged(self, event):
        self.ynumber = self.ynumberSlider.GetValue()
        self.ynumberSpinBox.SetValue(self.ynumber)
        self.updateFailedArray()

    def ynumberSpinBoxChanged(self, event):
        self.ynumber = self.ynumberSpinBox.GetValue()
        self.ynumberSlider.SetValue(self.ynumber)
        self.updateFailedArray()

    def yspacingSliderChanged(self, event):
        self.yspacing = self.yspacingSlider.GetValue()
        self.yspacingSpinBox.SetValue(self.yspacing)
        self.updateFailedArray()

    def yspacingSpinBoxChanged(self, event):
        self.yspacing = self.yspacingSpinBox.GetValue()
        self.yspacingSlider.SetValue(self.yspacing)
        self.updateFailedArray()

    def updateFailedArray(self):
        self.failedPanels = np.ones((self.xnumber, self.ynumber), dtype=int)

class panelDialogController(mw.panelDialog):

    def okPressed(self, event):
        counterx = 0
        countery = 0
        counter = 0

        while countery < app.window.ynumber:
            while counterx < app.window.xnumber:
                if self.buttons[counter].GetValue():
                    app.window.failedPanels[counterx][countery] = 1
                if not self.buttons[counter].GetValue():
                    app.window.failedPanels[counterx][countery] = 0

                counter += 1
                counterx +=1

            counterx = 0
            countery += 1

        print(app.window.failedPanels)
        print("OK")
        self.Close()

    def configureSize(self):

        print(app.window.failedPanels)
        self.grid_sizer_1.SetCols(app.window.xnumber)
        self.grid_sizer_1.SetRows(app.window.ynumber)
        self.grid_sizer_1.Clear()

        self.buttons = {}
        counterx = 0
        countery = 0
        counter = 0

        while countery < app.window.ynumber:
            while counterx < app.window.xnumber:
                self.buttons[counter] = wx.CheckBox(self, wx.ID_ANY, "")
                if app.window.failedPanels[counterx][countery] == 0:
                    self.buttons[counter].SetValue(False)
                if app.window.failedPanels[counterx][countery] == 1:
                    self.buttons[counter].SetValue(True)
                self.grid_sizer_1.Add(self.buttons[counter])

                counter += 1
                counterx +=1

            counterx = 0
            countery += 1


class windowApp(wx.App):

    def OnInit(self):
        self.window = MainFrameController(None, wx.ID_ANY, "")
        self.window.Show()
        return True

    def panelDialog(self):
        self.dialog = panelDialogController(None, wx.ID_ANY, "")
        self.dialog.configureSize()
        self.dialog.Show()

if __name__ == "__main__":
    app = windowApp(0)
    app.MainLoop()
