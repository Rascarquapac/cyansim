import os
import pandas as pd
import json as json
from pprint   import pprint
from load import Descriptor
from pool import Pool
from case import Case
from view_camera   import ViewCamera
from view_network  import ViewNetwork
from view_lens     import ViewLens
from gear import Cyangear
from draw_mermaid import Mermaid
from message import Messages
from draw     import Draw

class Test():
	def __init__(self):
		self.filename   = "some_case.json"
		self.descriptor = Descriptor(update=True)
		self.camera     = ViewCamera(self.descriptor)
		self.pool       = Pool()
		self.case       = Case(camera=self.camera,pool= self.pool,active=True,filename=self.filename)
		self.cyangear   = Cyangear(self.pool)
		self.network    = ViewNetwork(self.pool)
		self.lens       = ViewLens(self.pool)
		self.cyangear   = Cyangear(self.pool)
		self.messages   = Messages()
		self.draw       = Draw()
if __name__ == "__main__":
	test=Test()
	if os.path.exists(test.filename):
		test.camera.edit_number()
		test.camera.display_selected()
		test.network.edit()
		test.lens.edit()
		test.cyangear.analyze()
		print(test.messages.gear_list(test.cyangear))
		mermaid=Mermaid()    
		mermaid.code(test.cyangear)