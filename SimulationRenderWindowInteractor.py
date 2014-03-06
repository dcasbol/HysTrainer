"""Embedded VTK window module"""

from common import *
import vtk.wx.wxVTKRenderWindowInteractor as wxRWI

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
baseRWI = wxRWI.wxVTKRenderWindowInteractor
class SimulationRWI(baseRWI):
	"""Embedded VTK window on wxPython GUI."""

	def __init__(self, parent, id):
		"""Constructor

		Usage: widget = SimulationRWI(self, -1)
		Must be instantiated in main frame constructor.
		"""
		baseRWI.__init__(self, parent, id)
		self.scenario = None

	def OnKeyDown(self, event):
		"""Handle the wx.EVT_KEY_DOWN event for wxVTKRenderWindowInteractor.

		Specific vtkESQui implementation. Add extra control.
		Allow only the keys in this regexp:
			[0-9acqzx]|Left|Right|Up|Down|Prior|Next
			Including combinations with Shift key.
		"""

		shift = event.ShiftDown()
		keycode = event.GetKeyCode()
		if keycode >= 65 and keycode <= 90: # Convert caps
			keycode = keycode + 32
		
		allowed = range(ord('0'),ord('9')) + [ord('a'), ord('c'), ord('q'), ord('z'), ord('x'), \
			wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_UP, wx.WXK_DOWN, wx.WXK_PAGEUP, wx.WXK_PAGEDOWN]
		
		# Only process allowed keys
		if not shift and keycode not in allowed:
			return
		
		# event processing should continue
		event.Skip()

		ctrl = event.ControlDown()
		keysym = 'None'

		# Special keys
		keysym_dict = {wx.WXK_LEFT:'Left', wx.WXK_RIGHT:'Right', \
									 wx.WXK_UP:'Up', wx.WXK_DOWN:'Down', \
									wx.WXK_PAGEUP:'Prior', wx.WXK_PAGEDOWN:'Next'}
		key = chr(0)
		if keycode < 256:
			key = chr(keycode)
			keysym = key
		elif keycode in keysym_dict:
			keysym = keysym_dict[keycode]

		# wxPython 2.6.0.1 does not return a valid event.Get{X,Y}()
		# for this event, so we use the cached position.
		(x,y)= self._Iren.GetEventPosition()
		self._Iren.SetEventInformation(x, y,
										 ctrl, shift, key, 0,
										 keysym)

		self._Iren.KeyPressEvent()
		self._Iren.CharEvent()
	
	def OnSize(self, event):
		"""Handle the wx.EVT_SIZE event.

		Communicate the size change to the scenario.
		"""
		if (self.scenario):
			try:
				width, height = event.GetSize()
			except:
				width = event.GetSize().width
				height = event.GetSize().height
			self.scenario.SetWindowSize(width, height)
			
		baseRWI.OnSize(self, event)
