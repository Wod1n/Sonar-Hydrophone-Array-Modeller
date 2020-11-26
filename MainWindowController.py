"""
    This file contains the class for the Main Window Controller
    Overloading the empty methods for the GUI elements
"""


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
    """
    A class which controls the main window GUI element
    and the array shape

    Overloads the mainFrame class generated by wxGlade

    ...

    Attributes
    ----------

    arraytype : string
        Type of array to use
        (Currently Linear or Rect)
    xnumber : int
        Number of elements in the x axis
    xspacing : float
        Spacing of the elements along the x axis
        (Normalized to wavelength)
    xshading : string
        Type of shading employed in the x direction
        (Square [default], Chebyshev, Taylor, Hamming, Hanning)
    ynumber : int
        Number of elements in the y axis
    yspacing : float
        Spacing of the elements along the y axis
        (Normalized to wavelength)
    yshading : string
        Type of shading employed in the y direction
        (Square [default], Chebyshev, Taylor, Hamming, Hanning)
    azi : int
        Steering of the beam in the azimuthal direction
        (Range +/- 180 degrees)
    ele : int
        Steering of the beam in elevation
        (Range +/- 90 degrees)
    graphMode : string
        Type of graph to be displayed
        (currently 3D intensity or 2D polar)
    """


    def __init__(self, *args, **kwds):
        """
        Parameters
        ----------
        arraytype : string
            Type of array to use
            (Currently Linear or Rect)
            Default Rect
        xnumber : int
            Number of elements in the x axis
            Default 1
        xspacing : float
            Spacing of the elements along the x axis
            (Normalized to wavelength)
            Default 1
        xshading : string
            Type of shading employed in the x direction
            (Square [default], Chebyshev, Taylor, Hamming, Hanning)
        ynumber : int
            Number of elements in the y axis
            Default 1
        yspacing : float
            Spacing of the elements along the y axis
            (Normalized to wavelength)
            Default 1
        yshading : string
            Type of shading employed in the y direction
            (Square [default], Chebyshev, Taylor, Hamming, Hanning)
        azi : int
            Steering of the beam in the azimuthal direction
            (Range +/- 180 degrees)
            Default 0
        ele : int
            Steering of the beam in elevation
            (Range +/- 90 degrees)
            Default 0
        graphMode : string
            Type of graph to be displayed
            (currently 3D intensity or 2D polar)
            Default 3D Surface
        """


        self.arraytype = "rect"
        self.xnumber = 1
        self.xspacing = 1
        self.ynumber = 1
        self.yspacing = 1
        self.azi = 0
        self.ele = 0
        self.graphMode = "3D Surface"
        self.xshading = "Square"
        self.yshading = "Square"
        self.sos = 1500
        self.frequency = 500
        self.temperature = 18
        self.salinity = 100
        self.depth = 20

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
        """
        Exits the program
        """
        print("quitting")
        exit()

    def panelButtonPressed(self, event):
        """
        Opens failed panels Dialog
        """
        app.panelDialog()

    def surface3d(self, pattern, xgrid, ygrid):
        """
        Shows the 3D surface plot

        Parameters
        ----------
        pattern : dictionary
            Contains the information regarding array factor
        xgrid : array
            Array for the points on the x axis
        ygrid : array
            Array for the points on the y axis
        """
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
        """
        Shows the 2D Polar plot

        Parameters
        ----------
        pattern : dictionary
            Contains the information regarding array factor
        xgrid : array
            Array for the points on the x axis
        ygrid : array
            Array for the points on the y axis
        """

        azimuth = pattern['azimuth']
        AF = pattern['array_factor']

        middle = math.ceil(AF.shape[1]/2)

        fig = pyplt.figure()
        ax = pyplt.axes(polar=True)

        ax.plot(azimuth/180 * np.pi, 20*np.log10(np.abs(AF[:, middle]) + 0.000001),color='green', linewidth=2)
        ax.set_rmin(-70)

        pyplt.show()


    def showGraph(self, event):
        """
        Commands the program to display the graph selected
        """

        wavelength = self.sos / self.frequency
        print(wavelength)

        xfraction = self.xspacing / (wavelength*100)
        yfraction = self.yspacing / (wavelength*100)

        print(xfraction, yfraction)

        array = antarray.RectArray(self.xnumber, self.ynumber, xfraction, yfraction)
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
        """
        Generates a dictionary of values for the current state
        """
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
        """
        Changes the x number combo box value to match the x number slider value
        """
        self.xnumber = self.xnumberSlider.GetValue()
        self.xnumberSpinBox.SetValue(self.xnumber)
        self.updateFailedArray()

    def xnumberSpinBoxChanged(self, event):
        """
        Changes the x number slider value to match the x number combo box value
        """
        self.xnumber = self.xnumberSpinBox.GetValue()
        self.xnumberSlider.SetValue(self.xnumber)
        self.updateFailedArray()

    def xspacingSliderChanged(self, event):
        """
        Changes the x spacing combo box value to match the x spacing slider value
        """
        self.xspacing = self.xspacingSlider.GetValue()
        self.xspacingSpinBox.SetValue(self.xspacing)
        self.updateFailedArray()

    def xspacingSpinBoxChanged(self, event):
        """
        Changes the x spacing slider value to match the x spacing combo box value
        """
        self.xspacing = self.xspacingSpinBox.GetValue()
        self.xspacingSlider.SetValue(self.xspacing)
        self.updateFailedArray()

    def ynumberSliderChanged(self, event):
        """
        Changes the y number combo box value to match the y number slider value
        """
        self.ynumber = self.ynumberSlider.GetValue()
        self.ynumberSpinBox.SetValue(self.ynumber)
        self.updateFailedArray()

    def ynumberSpinBoxChanged(self, event):
        """
        Changes the y number slider value to match the y number combo box value
        """
        self.ynumber = self.ynumberSpinBox.GetValue()
        self.ynumberSlider.SetValue(self.ynumber)
        self.updateFailedArray()

    def yspacingSliderChanged(self, event):
        """
        Changes the y spacing combo box value to match the y spacing slider value
        """
        self.yspacing = self.yspacingSlider.GetValue()
        self.yspacingSpinBox.SetValue(self.yspacing)
        self.updateFailedArray()

    def yspacingSpinBoxChanged(self, event):
        """
        Changes the y spacing slider value to match the y spacing combo box value
        """
        self.yspacing = self.yspacingSpinBox.GetValue()
        self.yspacingSlider.SetValue(self.yspacing)
        self.updateFailedArray()

    def aziSliderChanged(self, event):
        """
        Changes the azi combo box value to match the azi slider value
        """
        self.azi = self.aziSlider.GetValue()
        self.aziSpinBox.SetValue(self.azi)

    def aziSpinBoxChanged(self, event):
        """
        Changes the azi slider value to match the azi combo box value
        """
        self.azi = self.aziSpinBox.GetValue()
        self.aziSlider.SetValue(self.azi)

    def eleSliderChanged(self, event):
        """
        Changes the ele combo box value to match the ele slider value
        """
        self.ele = self.eleSlider.GetValue()
        self.eleSpinBox.SetValue(self.ele)

    def eleSpinBoxChanged(self, event):
        """
        Changes the ele slider value to match the ele combo box value
        """
        self.ele = self.eleSpinBox.GetValue()
        self.eleSlider.SetValue(self.ele)

    def xwindowChanged(self, event):
        """
        Changes the shading on the x

        Options:
            * Square (Default)
            * Chebyshev
            * Taylor
            * Hamming
            * Hanning
        """
        self.xshading =  self.xwindowSelector.GetValue()

    def ywindowChanged(self, event):
        """
        Changes the shading on the y dimension

        Options:
            * Square (Default)
            * Chebyshev
            * Taylor
            * Hamming
            * Hanning
        """
        self.yshading =  self.ywindowSelector.GetValue()

    def graphComboSelect(self, event):
        """
        Changes the type of graph

        Options:
            * 3D Intensity (Default)
            * 2D Polar
        """
        self.graphMode = self.graphCombo.GetValue()

    def wilsonPressed(self, event):
        app.wilsonDialog()

    def presetSave(self, event):
        """
        Save the current state of the program to be recalled later
        """
        print("Saving Config")
        app.presetDialog()

    def presetLoad(self, event):
        """
        Load a prior used state of the program to be used

        FIle Type required '.sham'
        """
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
        """
        Updates the array for panel failures on closure of the panel failed dialog
        """
        self.failedPanels = np.ones((self.xnumber, self.ynumber), dtype=int)

    def getDimensions(self):
        """
        Gets the current array dimensions
        """
        return (self.xnumber, self.ynumber)

class panelDialogController(mw.panelDialog):
    """
    A class which controls the panel dialog window GUI element

    Overloads the panelDialog class generated by wxGlade

    ...

    Attributes
    ----------

    grid_sizer_1 : wxgridsizer
        Grid which dynamically scales to the size of the array
        Contains checkboxes which toggle pannels on and off
    """

    def okPressed(self, event):
        """
        Closes the dialog and saves the selected working panels to the array
        """
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
        """
        Dynamically scales the dialog box to match the size of the array
        """

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
    """
    A class which controls the preset dialog window GUI element

    Overloads the presetDialog class generated by wxGlade
    """

    def presetOKPressed(self, event):
        """
        Save the current state with the filename specified in the box
        """
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

class wilsonDialogController(mw.wilsonDialog):

    def wilsonEquation(self, update = False):

        temperature = self.tempctrl.GetValue()
        salinity = self.salinctrl.GetValue()
        depth = self.depthctrl.GetValue()

        sos = 1449 + 4.6*temperature - 0.055*(temperature**2) + 1.39*(salinity - 35) + 0.017*depth

        self.sos.SetLabel(str(sos))

        if update:
            app.window.sos = sos

    def setValues(self):

        self.sos.SetLabel(str(app.window.sos))
        self.freqctrl.SetValue(app.window.frequency)
        self.tempctrl.SetValue(app.window.temperature)
        self.salinctrl.SetValue(app.window.salinity)
        self.depthctrl.SetValue(app.window.depth)

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

        app.window.frequency = self.freqctrl.GetValue()
        app.window.temperature = self.tempctrl.GetValue()
        app.window.salinity = self.salinctrl.GetValue()
        app.window.depth = self.depthctrl.GetValue()

        self.Close()

class windowApp(wx.App):
    """
    Overall app holding all the window and dialog objects
    """

    def OnInit(self):
        """
        Opens the Main Window on initialisation
        """
        self.window = MainFrameController(None, wx.ID_ANY, "")
        self.window.Show()
        return True

    def panelDialog(self):
        """
        Opens the Panel Dialog as a dialog box when the button is pressed in the Main Window
        """
        self.dialog = panelDialogController(None, wx.ID_ANY, "")
        self.dialog.configureSize()
        self.dialog.Show()

    def presetDialog(self):
        """
        Opens the Preset Dialog as a dialog box when the button is pressed in the Main Window
        """
        self.dialog = presetDialogController(None, wx.ID_ANY, "")
        self.dialog.Show()

    def wilsonDialog(self):
        self.dialog = wilsonDialogController(None, wx.ID_ANY, "")
        self.dialog.setValues()
        self.dialog.Show()

if __name__ == "__main__":
    app = windowApp(0)
    app.MainLoop()
