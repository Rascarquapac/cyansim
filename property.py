import pandas as pd
import csv
import pickle
from cyancameralens import Lens

class Properties():
    def __init__(self) -> None:
        self.pkl_properties()
        self.lens_properties()
        #END: No more used ...

    def pkl_properties(self):
        with open('./picklized/properties.pkl', 'rb') as file:
            properties = pickle.load(file)        
        self.options     = properties["options"]
        self.constraints = properties["constraints"]   
        return
    
    def lens_properties(self):
        lens = Lens()
        cameraLensCategories = lens.cameraLensCategories()
        self.options["cameraLensCategories"] = cameraLensCategories
        for category in cameraLensCategories:
            (lensControlConstraint, lensTypeConstraint, lensMotorConstraint) = lens.cameraLensConstraints(category)
            self.constraints[(category,"LensControls")] = lensControlConstraint
            self.constraints[(category,"LensTypes")]    = lensTypeConstraint
            self.constraints[(category,"LensMotors")]   = lensMotorConstraint
            

if __name__  == "__main__":
    test = Properties()
    test.pkl_properties()