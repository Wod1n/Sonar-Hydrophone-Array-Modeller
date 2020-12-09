from ..GUI_Output import presetDialog
from zipfile import ZipFile

import json
import os
import numpy as np

class presetDialogController(presetDialog):
    """
    A class which controls the preset dialog window GUI element

    Overloads the presetDialog class generated by wxGlade
    """

    def __init__(self, app, *args, **kwds):
        self.app = app

        super().__init__(*args, **kwds)

    def presetOKPressed(self, event):
        """
        Save the current state with the filename specified in the box
        """
        name = self.presetName.GetValue()
        self.app.window.saveState(name)
        self.Close()