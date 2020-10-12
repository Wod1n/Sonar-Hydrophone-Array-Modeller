import GUI as mw
import numpy as np
import matplotlib.pyplot as pyplt
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

        self.updateFailedArray()

        super().__init__(*args, **kwds)

    def quitPressed(self, event):
        print("quitting")
        exit()

    def panelButtonPressed(self, event):
        app.panelDialog()

    def showGraph(self, event):
        array = antarray.RectArray(self.xnumber, self.ynumber, self.xspacing/2, self.yspacing/2)
        #theta = np.arange(-180, 180, 0.1)

        y = np.linspace(0, 10, 1025)
        AF = array.get_pattern(beam_az = self.azi, beam_el = self.ele)["array_factor"]

        tilex = int(np.ceil(self.xspacing-0.5))*2+1
        tiley = int(np.ceil(self.yspacing-0.5))*2+1

        x = np.linspace(-tilex, tilex, AF.shape[1])
        y = np.linspace(-tiley, tiley, AF.shape[0])

        xgrid, ygrid = np.meshgrid(x,y)

        fig = pyplt.figure()
        ax = pyplt.axes(projection='3d')

        #toggle back in when failed array is merged in
        #array.toggle_panels(self.failedPanels)

        ax.contour3D(xgrid, ygrid, np.abs(array.get_pattern()["array_factor"]), 50, rstride=1, cstride=1,
            cmap=cm.coolwarm, linewidth=0, antialiased=False)

        print(array.get_pattern()["weight"])

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z');

        ax.view_init(60, 35)
        pyplt.show()
        print("graph")

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
