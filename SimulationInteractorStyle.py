"""Interactor style module

Here is defined the class MyStyle, which keeps tracking
of the lens disk, among other tasks.
"""

from common import *
from LensDisk import *
from timers import NailMovingTimer

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
baseSCIS = vtkesqui.vtkSingleChannelInteractorStyle
class MyStyle(baseSCIS):
	"""Extended vtkSingleChannelInteractorStyle class.

	Extend some functionality related to the lens simulation.
	"""
	def __init__(self, parent):
		"""Constructor

		Usage: style = MyStyle(self)
		Must be instantiated in the main frame constructor.
		"""
		self.parent = parent

	def Initialize(self):
		"""Add some observers to mouse and keyboard events."""
		baseSCIS.Initialize(self)
		self.Lens = LensDisk(self.GetScenario())
		self.Lens.Initialize()

		# Bind events
		self.AddObserver('LeftButtonPressEvent', self.LensLeftButtonPress)
		self.AddObserver('LeftButtonReleaseEvent', self.LensLeftButtonRelease)
		self.AddObserver('KeyPressEvent', self.LensKeyPress)
		self.AddObserver('MouseMoveEvent', self.LensMouseMove)
		self.AddObserver('MouseWheelForwardEvent', self.LensMouseWheelForward)
		self.AddObserver('MouseWheelBackwardEvent', self.LensMouseWheelBackward)

		# Interactor
		self.iren = self.GetInteractor()

		# Variables
		self.prevpos = 0
		self.pressed = False

	def SetLensAngle(self, angle):
		"""Set lens inclination angle."""
		baseSCIS.SetLensAngle(self, angle)
		self.Lens.Update()

	def LensLeftButtonPress(self, obj, evt):
		"""Additional LeftButtonPressEvent callback function."""
		if self.parent.timer.Initialized and self.parent.timer.use_haptic:
			return

		self.OnLeftButtonDown()
		self.pressed = True

	def LensLeftButtonRelease(self, obj, evt):
		"""Additional LeftButtonReleaseEvent callback function."""
		if self.parent.timer.Initialized and self.parent.timer.use_haptic:
			return

		self.OnLeftButtonUp()
		self.pressed = False

	def LensKeyPress(self, obj, evt):
		"""Additional KeyPressEvent callback function.

		Add some control on key events.
		"""
		key = self.iren.GetKeySym()

		# Tool change through GUI control
		try:
			i = int(key)
			if i >= 0 and i <= 9:
				self.parent.SelectTool(i)
				# Stereo-rendering is not desirable
				if i == 3:
					rw = self.iren.GetRenderWindow()
					rw.SetStereoRender(not rw.GetStereoRender())
				return
		except ValueError:
			pass

		use_haptic = False
		if self.parent.timer.Initialized and self.parent.timer.use_haptic:
			use_haptic = True

		if not use_haptic:
			self.OnKeyPress()

			if key == 'z':
				self.Lens.Rotate(1)
			elif key == 'x':
				self.Lens.Rotate(-1)
			elif key == 'a':
				self.timer = timer = NailMovingTimer(self.parent)
				timer.StartMoving()
			elif key == 'Prior':
				self.parent.AddToolInsertion(1)
			elif key == 'Next':
				self.parent.AddToolInsertion(-1)

			self.Lens.Update()

	def LensMouseMove(self, obj, evt):
		"""Additional MouseMoveEvent callback function."""
		if self.parent.timer.Initialized and self.parent.timer.use_haptic:
			return

		self.OnMouseMove()
		pick = self.iren.GetEventPosition()
		shift = self.iren.GetShiftKey()
		if shift and self.pressed:
			x = -0.1*(pick[0] - self.prevpos)
			self.Lens.Rotate(x)

		self.prevpos = pick[0]
		self.Lens.Update()

	def LensMouseWheelForward(self, obj, evt):
		"""Additional MouseWheelForwardEvent callback function."""
		if self.parent.timer.Initialized and self.parent.timer.use_haptic:
			return

		self.OnMouseWheelForward()
		self.Lens.Update()
		if self.iren.GetShiftKey():
			self.parent.AddToolInsertion(1)

	def LensMouseWheelBackward(self, obj, evt):
		"""Additional MouseWheelBackwardEvent callback function."""
		if self.parent.timer.Initialized and self.parent.timer.use_haptic:
			return

		self.OnMouseWheelBackward()
		self.Lens.Update()
		if self.iren.GetShiftKey():
			self.parent.AddToolInsertion(-1)
