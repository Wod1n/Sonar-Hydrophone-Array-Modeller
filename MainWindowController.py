import GUI as mw
import numpy as np
import matplotlib.pyplot as pyplt
import matplotlib.transforms as mtransforms
from mpl_toolkits import mplot3d
from matplotlib import cm
import antarray
import wx

class MainFrameController(mw.mainFrame):

    def __init__(self, *args, **kwds):

        self.xnumber = 1
        self.xspacing = 1
        self.ynumber = 1
        self.yspacing = 1
        self.azi = 0
        self.ele = 0
        self.graphMode = "3D Surface"

        self.updateFailedArray()

        super().__init__(*args, **kwds)

    def quitPressed(self, event):
        print("quitting")
        exit()

    def panelButtonPressed(self, event):
        app.panelDialog()

    def surface3d(self, AF, xgrid, ygrid):
        fig = pyplt.figure()
        ax = pyplt.axes(projection='3d')

        ax.plot_surface(xgrid, ygrid, 20*np.log10(np.abs(AF)),cmap='viridis', edgecolor='none')
        ax.set_title('Surface plot')

        ax.set_xlabel('y')
        ax.set_ylabel('x')
        ax.set_zlabel('Intensity')

        ax.view_init(60, 35)
        pyplt.show()

    def polar2d(self, AF, xgrid, ygrid):
        print(xgrid)
        print(ygrid)

    def showGraph(self, event):
        array = antarray.RectArray(self.xnumber, self.ynumber, self.xspacing/2, self.yspacing/2,)
        #theta = np.arange(-180, 180, 0.1)

        array.toggle_panels(app.window.failedPanels)

        AF = array.get_pattern(beam_az = self.azi, beam_el = self.ele)["array_factor"]

        tilex = int(np.ceil(self.xspacing-0.5))*2+1
        tiley = int(np.ceil(self.yspacing-0.5))*2+1

        x = np.linspace(-tilex, tilex, AF.shape[1])
        y = np.linspace(-tiley, tiley, AF.shape[0])

        xgrid, ygrid = np.meshgrid(x,y)

        graph_type = {
        "3D Surface" : self.surface3d,
        "2D Polar" : self.polar2d,
        }

        graph_type[self.graphMode](AF, xgrid, ygrid)

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
        self.xspacing = self.xspacingSpinBox.GetValue()
        self.xspacingSlider.SetValue(self.xspacing)
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

    def aziSliderChanged(self, event):
        self.azi = self.aziSlider.GetValue()
        self.aziSpinBox.SetValue(self.azi)

    def aziSpinBoxChanged(self, event):
        self.azi = self.aziSpinBox.GetValue()
        self.aziSlider.SetValue(self.azi)

    def eleSliderChanged(self, event):
        self.ele = self.eleSlider.GetValue()
        self.eleSpinBox.SetValue(self.ele)

    def eleSpinBoxChanged(self, event):
        self.ele = self.eleSpinBox.GetValue()
        self.eleSlider.SetValue(self.ele)

    def graphComboSelect(self, event):
        self.graphMode = self.graphCombo.GetValue()

    def presetSave(self, event):
        print("Saving Config")
        app.presetDialog()

    def updateFailedArray(self):
        self.failedPanels = np.ones((self.xnumber, self.ynumber), dtype=int)

    def getDimensions(self):
        return (self.xnumber, self.ynumber)

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

        self.Fit()


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
