import GUI as mw
import numpy as np
import matplotlib.pyplot as pyplt
import matplotlib.transforms as mtransforms
from mpl_toolkits import mplot3d
from matplotlib import cm
import json
import glob, os
from zipfile import ZipFile
import antarray
import math
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
        self.xshading = "Square"
        self.yshading = "Square"

        self.updateFailedArray()

        os.chdir("Presets/")

        super().__init__(*args, **kwds)
        wxglade_tmp_menu = wx.Menu()
        number = 0
        self.preset = {}
        for file in glob.glob("*.sham"):
            wxglade_tmp_menu.Append(number, file[:-5])
            self.preset[number] = file
            self.Bind(wx.EVT_MENU, self.presetLoad, id=number)
            number += 1

        self.frame_menubar.Insert(3, wxglade_tmp_menu, "Presets")


    def quitPressed(self, event):
        print("quitting")
        exit()

    def panelButtonPressed(self, event):
        app.panelDialog()

    def surface3d(self, pattern, xgrid, ygrid):
        fig = pyplt.figure()
        ax = pyplt.axes(projection='3d')

        AF = pattern['array_factor']

        ax.plot_surface(xgrid, ygrid, 20*np.log10(np.abs(AF) + 0.0001),cmap=cm.coolwarm, linewidth=0)
        ax.set_title('Surface plot')

        ax.set_xlabel('y')
        ax.set_ylabel('x')
        ax.set_zlabel('Intensity')

        ax.view_init(60, 35)
        pyplt.show()

    def polar2d(self, pattern, xgrid, ygrid):

        azimuth = pattern['azimuth']
        AF = pattern['array_factor']

        middle = math.ceil(AF.shape[1]/2)

        fig = pyplt.figure()
        ax = pyplt.axes(polar=True)

        ax.plot(azimuth/180 * np.pi, 20*np.log10(np.abs(AF[:, middle]) + 0.000001),color='green', linewidth=2)
        ax.set_rmin(-70)

        pyplt.show()


    def showGraph(self, event):
        array = antarray.RectArray(self.xnumber, self.ynumber, self.xspacing/2, self.yspacing/2)
        #theta = np.arange(-180, 180, 0.1)

        array.toggle_panels(self.failedPanels)

        pattern = array.get_pattern(beam_az = self.azi, beam_el = self.ele, windowx=self.xshading, windowy=self.yshading)

        x = np.linspace(-90, 90, pattern['array_factor'].shape[1])
        y = np.linspace(-90, 90, pattern['array_factor'].shape[0])

        xgrid, ygrid = np.meshgrid(x,y)

        graph_type = {
        "3D Surface" : self.surface3d,
        "2D Polar" : self.polar2d,
        }

        graph_type[self.graphMode](pattern, xgrid, ygrid)

    def getState(self):
        current_state = {   "xnumber" : self.xnumber,
                            "xspacing" : self.xspacing,
                            "ynumber" : self.ynumber,
                            "yspacing" : self.yspacing,
                            "azimuth" : self.azi,
                            "elevation" : self.ele,
                            "graphmode" : self.graphMode,
                            "xshading" : self.xshading,
                            "yshading" : self.yshading}

        return current_state

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

    def xwindowChanged(self, event):
        self.xshading =  self.xwindowSelector.GetValue()

    def ywindowChanged(self, event):
        self.yshading =  self.ywindowSelector.GetValue()

    def graphComboSelect(self, event):
        self.graphMode = self.graphCombo.GetValue()

    def presetSave(self, event):
        print("Saving Config")
        app.presetDialog()

    def presetLoad(self, event):
        with ZipFile(self.preset[event.GetId()]) as myzip:
            myzip.extract("current_state.json")
            myzip.extract("fails.npy")

        with open("current_state.json") as f:
            data = json.load(f)

        self.xnumber = data["xnumber"]
        self.xspacing = data["xspacing"]
        self.ynumber = data["ynumber"]
        self.yspacing = data["yspacing"]
        self.azi = data["azimuth"]
        self.ele = data["elevation"]
        self.graphMode = data["graphmode"]
        self.xshading = data["xshading"]
        self.yshading = data["yshading"]

        self.failedPanels = np.load("fails.npy")

        os.remove("current_state.json")
        os.remove("fails.npy")

        self.xnumberSpinBox.SetValue(self.xnumber)
        self.xnumberSlider.SetValue(self.xnumber)
        self.xspacingSpinBox.SetValue(self.xspacing)
        self.xspacingSlider.SetValue(self.xspacing)
        self.ynumberSpinBox.SetValue(self.ynumber)
        self.ynumberSlider.SetValue(self.ynumber)
        self.yspacingSpinBox.SetValue(self.yspacing)
        self.yspacingSlider.SetValue(self.yspacing)
        self.aziSpinBox.SetValue(self.azi)
        self.aziSlider.SetValue(self.azi)
        self.eleSpinBox.SetValue(self.ele)
        self.eleSlider.SetValue(self.ele)
        self.graphCombo.SetValue(self.graphMode)
        self.xwindowSelector.SetValue(self.xshading)
        self.ywindowSelector.SetValue(self.yshading)

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

class presetDialogController(mw.presetDialog):
    def presetOKPressed(self, event):
        current_state = app.window.getState()
        print(current_state)
        f = open("current_state.json", "w")
        f.write(json.dumps(current_state))
        f.close()
        np.save("fails", app.window.failedPanels)

        name = self.presetName.GetValue()

        zipObj = ZipFile(name + ".sham", "w")
        zipObj.write("current_state.json")
        zipObj.write("fails.npy")
        zipObj.close()

        os.remove("current_state.json")
        os.remove("fails.npy")

        self.Close()

class windowApp(wx.App):

    def OnInit(self):
        self.window = MainFrameController(None, wx.ID_ANY, "")
        self.window.Show()
        return True

    def panelDialog(self):
        self.dialog = panelDialogController(None, wx.ID_ANY, "")
        self.dialog.configureSize()
        self.dialog.Show()

    def presetDialog(self):
        self.dialog = presetDialogController(None, wx.ID_ANY, "")
        self.dialog.Show()

if __name__ == "__main__":
    app = windowApp(0)
    app.MainLoop()
