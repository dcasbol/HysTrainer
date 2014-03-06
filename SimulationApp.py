"""App module.

Contain the class SimulationApp.
"""

from SimulationFrame import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class SimulationApp(wx.App):
	"""HysTrainer app class."""

	def __init__(self):
		wx.App.__init__(self, False)

	def OnInit(self):
		"""Build main frame before starting the app loop."""
		self.frame = SimulationFrame()
		return True
