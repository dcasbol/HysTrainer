"""HysTrainer main frame module.

Here is the main code of HysTrainer.
"""

from common import *
from ButtonContainer import *
from SimulationInteractorStyle import *
from SimulationRenderWindowInteractor import *
from timers import *

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class SimulationFrame(wx.Frame):
	"""HysTrainer main frame."""

	def __init__(self):
		wx.Frame.__init__(self, None, -1, "Rigid endoscopy simulator", size=(850,650))

		# Path
		self.path = '.'
		# On Mac platforms (if built as app)
		if os.name == 'mac' and sys.argv[0] != 'main.p':
				self.path = sys.argv[0]
				i = self.path.rfind('/')
				self.path = self.path[:i]
		# Application icon on other platforms
		if os.name == 'nt':
			ico_file = wx.Icon(self.path+'/resources/HysTrainer.ico',wx.BITMAP_TYPE_ICO)
			self.SetIcon(ico_file)

		# GUI Elements
		sttBox = wx.StaticBox(self, -1, "Tool Selector")
		loadButton = wx.Button(self, -1, 'Load Simulation')
		self.fnDisplay = wx.StaticText(self, -1, 'No simulation loaded', style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
		exitButton = wx.Button(self, -1, 'Exit')
		self.widget = SimulationRWI(self, -1)
		self.extractText = wx.StaticText(self, -1, 'Extract haptic device before start', style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
		self.toolSelectionText = wx.StaticText(self, -1, 'Use left/right pedals to select previous/next tool', style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
		self.toolInsertionText = wx.StaticText(self, -1, 'Tool insertion', style = wx.ALIGN_LEFT | wx.ST_NO_AUTORESIZE)
		self.inGauge = wx.Gauge(self, -1, 50, style = wx.GA_HORIZONTAL)
		self.tool_depth = 0

		# Lens selection buttons
		lens_selection_text = wx.StaticText(self, -1, 'Select the lens you want to mount or use left/right pedals', style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)

		lens_0_img = wx.Image(self.path+'/resources/lens_0.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		lens_0_selected_img = wx.Image(self.path+'/resources/lens_0-selected.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		lens_30_img = wx.Image(self.path+'/resources/lens_30.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		lens_30_selected_img = wx.Image(self.path+'/resources/lens_30-selected.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		lens_70_img = wx.Image(self.path+'/resources/lens_70.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		lens_70_selected_img = wx.Image(self.path+'/resources/lens_70-selected.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()

		self.lens_buttons = list()
		lens_0_button = wx.BitmapButton(self, -1, lens_0_img)
		lens_0_button.angle = 0
		lens_0_button.default_img = lens_0_img
		lens_0_button.selected_img = lens_0_selected_img
		self.lens_buttons.append(lens_0_button)
		lens_30_button = wx.BitmapButton(self, -1, lens_30_img)
		lens_30_button.angle = 30
		lens_30_button.default_img = lens_30_img
		lens_30_button.selected_img = lens_30_selected_img
		self.lens_buttons.append(lens_30_button)
		lens_70_button = wx.BitmapButton(self, -1, lens_70_img)
		lens_70_button.angle = 70
		lens_70_button.default_img = lens_70_img
		lens_70_button.selected_img = lens_70_selected_img
		self.lens_buttons.append(lens_70_button)

		self.lens_buttons_sizer = wx.BoxSizer(wx.VERTICAL)
		self.lens_buttons_sizer.Add(lens_selection_text, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, border = 10)
		lens_sizer = wx.BoxSizer(wx.HORIZONTAL)
		for b in self.lens_buttons:
			lens_sizer.Add(b, 0, wx.FIXED_MINSIZE | wx.ALL, border = 10)
		self.lens_buttons_sizer.Add(lens_sizer, 2, wx.EXPAND | wx.TOP | wx.BOTTOM, border = 10)

		# Tool buttons
		lens_img = wx.Image(self.path+'/resources/lens.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		lens_selected_img = wx.Image(self.path+'/resources/lens-selected.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		cauterizer_img = wx.Image(self.path+'/resources/cauterizer.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		cauterizer_selected_img = wx.Image(self.path+'/resources/cauterizer-selected.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		smallBrush_img = wx.Image(self.path+'/resources/brush_small.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		smallBrush_selected_img = wx.Image(self.path+'/resources/brush_small-selected.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		cutter_img = wx.Image(self.path+'/resources/cutter.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		cutter_selected_img = wx.Image(self.path+'/resources/cutter-selected.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		
		self.tool_buttons = ButtonContainer()

		camera_button = wx.BitmapButton(self, -1, lens_img)
		camera_button.default_img = lens_img
		camera_button.selected_img = lens_selected_img
		self.tool_buttons.AddButton(camera_button, 'camera')
		camera_button.Hide()

		cauterizer_button = wx.BitmapButton(self, -1, cauterizer_img)
		cauterizer_button.default_img  = cauterizer_img
		cauterizer_button.selected_img = cauterizer_selected_img
		self.tool_buttons.AddButton(cauterizer_button, 'cauterizer', vtkesqui.vtkToolSingleChannel.Cauterizer)
		cauterizer_button.Hide()

		brush_button = wx.BitmapButton(self, -1, smallBrush_img)
		brush_button.default_img  = smallBrush_img
		brush_button.selected_img = smallBrush_selected_img
		self.tool_buttons.AddButton(brush_button, 'brush', vtkesqui.vtkToolSingleChannel.Brush)
		brush_button.Hide()

		cutter_button = wx.BitmapButton(self, -1, cutter_img)
		cutter_button.default_img  = cutter_img
		cutter_button.selected_img = cutter_selected_img
		self.tool_buttons.AddButton(cutter_button, 'cutter', vtkesqui.vtkToolSingleChannel.Cutter)
		cutter_button.Hide()

		self.tool_models = (vtkesqui.vtkToolSingleChannel.Cauterizer,
		                    vtkesqui.vtkToolSingleChannel.Brush,
		                    vtkesqui.vtkToolSingleChannel.Cutter)

		# Fitting
		# Upper sizer
		upSizer = wx.BoxSizer(wx.HORIZONTAL)
		upSizer.Add(loadButton, 0, wx.EXPAND)
		upSizer.Add(self.fnDisplay, 1, wx.EXPAND)
		upSizer.Add(exitButton, 0, wx.EXPAND)
		# Left side sizer
		lsSizer = self.lsSizer = wx.BoxSizer(wx.VERTICAL)
		lsSizer.Add(upSizer, 0, wx.EXPAND | wx.ALL, border = 10)
		lsSizer.Add(self.widget, 1, wx.EXPAND | wx.ALL, border = 10)
		lsSizer.Add(self.extractText, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, border = 300)
		lsSizer.Add(self.toolSelectionText, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, border = 300)
		lsSizer.Add(self.lens_buttons_sizer, 1, wx.FIXED_MINSIZE | wx.ALIGN_CENTER | wx.TOP, border = 10)
		self.extractText.Hide()
		self.toolSelectionText.Hide()
		lsSizer.Hide(4)
		# Tool selector sizer
		self.toolSelector = wx.StaticBoxSizer(sttBox, wx.VERTICAL)
		self.toolSelector.SetMinSize((129,474))
		self.tool_buttons.SetSizer(self.toolSelector)
		# Right side sizer (instrumental + insertion bar)
		rsSizer = self.rsSizer = wx.BoxSizer(wx.VERTICAL)
		rsSizer.Add(self.toolSelector, 1, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.ALL, border = 10)
		rsSizer.Add(self.toolInsertionText, 0, wx.FIXED_MINSIZE | wx.LEFT | wx.RIGHT, border = 10)
		rsSizer.Add(self.inGauge, 0, wx.EXPAND | wx.ALL, border = 10)
		# Main sizer
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(lsSizer, 1, wx.EXPAND)
		sizer.Add(rsSizer, 0, wx.EXPAND, border = 10)

		self.SetSizer(sizer)
		self.Layout()
		self.widget.Enable(1)
		self.widget.AddObserver("ExitEvent", lambda o,e,f=self: f.Close())

		# Set Renderer
		self.ren = vtk.vtkRenderer()
		self.renWin = self.widget.GetRenderWindow()
		self.renWin.AddRenderer(self.ren)

		# Set simulation timer (includes collision highlighter)
		self.timer = SimulationTimer()
		self.timer.parent = self
		
		# Set simulation references
		self.scenario = None
		self.style = None
		self.simulation = None

		# Bindings
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseEvent)
		self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

		loadButton.Bind(wx.EVT_BUTTON, self.OnLoadButton)
		exitButton.Bind(wx.EVT_BUTTON, self.OnClose)

		lens_0_button.Bind(wx.EVT_BUTTON, self.OnLens0)
		lens_30_button.Bind(wx.EVT_BUTTON, self.OnLens30)
		lens_70_button.Bind(wx.EVT_BUTTON, self.OnLens70)
		
		camera_button.Bind(wx.EVT_BUTTON, self.OnCameraButton)
		cauterizer_button.Bind(wx.EVT_BUTTON, self.OnCauterizerButton)
		brush_button.Bind(wx.EVT_BUTTON, self.OnBrushButton)
		cutter_button.Bind(wx.EVT_BUTTON, self.OnCutterButton)
		
		# This is necessary in order to communicate some key events to VTK
		camera_button.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		cauterizer_button.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		brush_button.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		cutter_button.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

		# Center and show
		self.Center()
		self.Show()
		self.Update()
	
	def OnLoadButton(self, event):
		"""Manage the SRML load."""

		# First stop the timer
		self.timer.Stop()

		# Show FileOpen dialog
		dialog = wx.FileDialog(self, "Choose a SRML file", self.path+"/examples", \
			wildcard="*.srml", style=wx.FD_OPEN | wx.FILE_MUST_EXIST)
		if dialog.ShowModal() == wx.ID_CANCEL:
			if self.simulation:
				self.ShowSimulation()
				self.StartTimer()
			return
		else:
			self.HideAll()
		

		# Reset the wxTimer
		self.timer.Reset()
		
		# Reset current renderer
		self.renWin.InvokeEvent("DeleteAllObjects")
		self.ren.RemoveAllLights()
		actors = self.ren.GetActors()
		actors.InitTraversal()
		a = actors.GetNextActor()
		while a:
			self.ren.RemoveActor(a)
			a = actors.GetNextActor()
		

		# Reset simulation objects
		self.scenario = None
		self.style = None
		self.simulation = None
		
		# Read the SRML file
		reader = vtkesqui.vtkSRMLReader()
		reader.SetFileName(dialog.GetPath())
		sim = reader.ConstructSimulation()
		

		# Check if valid simulation was returned
		if not sim:
			dialog = wx.MessageDialog(self, "The SMRL file seems to be bad constructed.", \
				"Bad SRML file", wx.OK)
			dialog.ShowModal()
			self.UpdateToolSelector()
			return
		

		# Check if the scene matches the requirements
		check_val = self.CheckScene(sim.GetScenario())
		if check_val:
			msg = "Bad scene configuration."
			if check_val == -1:
				msg += "\nUnknow object found."
			elif check_val == -2:
				msg += "\nInvalid number of camera tools."
			elif check_val == -3:
				msg += "\nMissing texture in at least one element."
			dialog = wx.MessageDialog(self, msg, \
				"Bad scene", wx.OK)
			dialog.ShowModal()
			self.UpdateToolSelector()
			return
		

		# Set up simulation
		self.simulation = sim

		self.simulation.InteractionOn()

		self.scenario = self.simulation.GetScenario()

		self.scenario.SetRenderWindow(self.renWin)
		

		# Set the wxTimer correctly
		self.timer.SetSimulation(self.simulation)

		self.AddHighlightObjects()

		self.timer.HighlightOn()
		

		# Add tool buttons to the tool selector
		self.UpdateToolSelector()


		# Locate nail to provide further animations
		self.LocateNail()
		
		# Set SRML title
		self.fnDisplay.SetLabel(dialog.GetFilename())
		

		# Set Interactor Style
		self.style = MyStyle(self)
		self.style.SetScenario(self.scenario)
		self.simulation.SetInteractorStyle(self.style)


		# Initialize the timer
		self.use_haptic = self.timer.Initialize()
		self.timer.CuttingOff()
		if self.use_haptic:
			self.selected_lens = 0
			button = self.lens_buttons[0]
			button.SetBitmapLabel(button.selected_img)
			self.StartTimer()
		else:
			self.ShowLenses()
	
	def CheckScene(self, scenario):
		"""Check that the SRML meets the requirements.

		Check that there are only organs and single-channel tools.
		Also checks that there is only a camera tool.
		Return values:
			 0 if OK
			-1 if unknow object
			-2 if invalid number of camera tools
			-3 if element without texture.
		"""
		# Check that there are only organs and single-channel tools
		objects = scenario.GetObjects()
		objects.InitTraversal()
		o = objects.GetNextObject()
		nCamTools = 0
		while o:
			current_is_cam_tool = False
			if o.IsA('vtkToolSingleChannel'):
				if o.GetToolModel() == vtkesqui.vtkToolSingleChannel.Camera:
					current_is_cam_tool = True
					nCamTools += 1
			elif not o.IsA('vtkOrgan'):
				return -1
			# Does it have valid textures? Win32: Should it require it also for invisible objects?
			if not current_is_cam_tool:
				elements = o.GetElements()
				elements.InitTraversal()
				e = elements.GetNextElement()
				while e:
					tfn = e.GetVisualizationModel().GetTextureFileName()
					if not tfn or tfn == '' or not os.path.exists(tfn):
						return -3
					e = elements.GetNextElement()
			o = objects.GetNextObject()
		if nCamTools != 1:
			return -2
		return 0

	def UpdateToolSelector(self):
		"""Refresh the toolbar.

		Hide or show buttons depending on SRML data.
		"""
		self.tool_buttons.HideAllButtons()

		if not self.scenario:
			return

		# Reset list. Camera is default.
		self.tool_buttons.ShowButtonByName('camera')
		self.tool_buttons.SelectButtonByName('camera')

		# Show tool buttons required
		objects = self.scenario.GetObjects()
		objects.InitTraversal()
		o = objects.GetNextObject()
		while o:
			# Check model
			if o.IsA('vtkToolSingleChannel'):
				model = o.GetToolModel()
				if model in self.tool_models:
					self.tool_buttons.ShowButtonByModel(model)
					self.tool_buttons.GetButtonByModel(model).Tool = o
			o = objects.GetNextObject()

		# Layout toolbar
		self.Layout()
		self.FitInside()

	def SelectTool(self, tool_id):
		"""Select the tool with the ID given.

		The tool must be full retracted.
		Other side effects, as button highlighting and cutting mode,
		are taken into account.
		"""
		if tool_id < 0 or tool_id >= self.tool_buttons.GetNumberOfVisibleButtons():
			return

		if not self.style.ChangeTool(tool_id):
			self.ShowToolWarning()
			return

		if self.tool_buttons.GetSelectedButtonId() == tool_id:
			self.tool_buttons.SelectButtonByName('camera')
		else:
			self.tool_buttons.SelectButtonById(tool_id)

		if self.use_haptic:
			haptic = self.simulation.GetHapticDevice()
			haptic.GetTools().RemoveAllItems()
			if self.tool_buttons.GetSelectedButtonName() != 'camera':
				haptic.AddTool(self.tool_buttons.GetSelectedButton().Tool)

		if self.tool_buttons.GetSelectedButtonName() == 'cutter':
			self.timer.CuttingOn()
		else:
			self.timer.CuttingOff()

		# In order to mantain control of insertion gauge
		self.tool_depth = 0
		self.inGauge.SetValue(0)

		return

	def HideAll(self):
		"""Hide all GUI main views."""
		self.widget.Hide()
		self.toolSelectionText.Hide()
		self.lsSizer.Hide(4)
		self.extractText.Hide()
		self.Layout()

	def ShowExtractText(self):
		"""Show a warning to extract the haptic device."""
		self.widget.Hide()
		self.toolSelectionText.Hide()
		self.lsSizer.Hide(4)
		self.extractText.Show()
		self.Layout()

	def ShowToolSelectionText(self):
		"""Show a usage advice to select the tool."""
		self.widget.Hide()
		self.extractText.Hide()
		self.lsSizer.Hide(4)
		self.toolSelectionText.Show()
		self.Layout()

	def ShowSimulation(self):
		"""Show the simulation window."""
		self.extractText.Hide()
		self.toolSelectionText.Hide()
		self.lsSizer.Hide(4)
		self.widget.Show()
		self.Layout()

	def ShowLenses(self):
		"""Show the lens selection view."""
		self.widget.Hide()
		self.extractText.Hide()
		self.toolSelectionText.Hide()
		self.lsSizer.Show(4)
		self.Layout()

	def ShowToolWarning(self):
		"""Show a warning when wrong tool change."""
		msg = wx.Frame(self, -1, "Can't change tool")
		msg.m_sizer = wx.BoxSizer(wx.VERTICAL)
		msg.m_display = wx.StaticText(msg, -1, 'You must extract the tool first', style=wx.ALIGN_CENTRE | wx.ST_NO_AUTORESIZE)
		msg.m_sizer.Add(msg.m_display, 0, wx.EXPAND | wx.ALL, border = 30)
		msg.SetSizer(msg.m_sizer)
		msg.m_timer = DialogHidingTimer(msg)
		msg.Fit()
		msg.CenterOnParent()
		msg.Show()
		msg.m_timer.StartHiding()
	
	def AddHighlightObjects(self):
		"""Set the organs to be highlighted when colided."""
		objects = self.scenario.GetObjects()
		objects.InitTraversal()
		o = objects.GetNextObject()
		while o:
			if o.IsA('vtkOrgan'):
				self.timer.AddHighlightObject(o)
			o = objects.GetNextObject()

	def ChangeLens(self, angle):
		"""Change lens inclination angle."""
		if angle < 0 or angle > 90:
			return

		if self.timer.use_haptic:
			haptic = self.simulation.GetHapticDevice()
			haptic.SetLensAngle(angle)
		else:
			self.style.SetLensAngle(angle)

	def LocateNail(self):
		"""Find the nail object and point it."""
		objects = self.scenario.GetObjects()
		objects.InitTraversal()
		o = objects.GetNextObject()
		while o:
			if o.GetName().find('nail') >= 0:
				elements = o.GetElements()
				elements.InitTraversal()
				e = elements.GetNextElement()
				while e:
					if e.GetName() == 'nail':
						self.nail = e
						self.nail.depth = 0
						e = None
					else:
						e = elements.GetNextElement()
				o = None
			else:
				o = objects.GetNextObject()


	def OnLens0(self, event):
		"""0-degree-lens button callback."""
		self.ChangeLens(0)
		self.ShowSimulation()
		if self.timer.use_haptic and self.selected_lens != 0:
			prev_button = self.lens_buttons[self.selected_lens]
			prev_button.SetBitmapLabel(prev_button.default_img)
			self.selected_lens = 0
			button = self.lens_buttons[self.selected_lens]
			button.SetBitmapLabel(button.selected_img)
		else:
			self.StartTimer()

	def OnLens30(self, event):
		"""30-degree-lens button callback."""
		self.ChangeLens(30)
		self.ShowSimulation()
		if self.timer.use_haptic and self.selected_lens != 1:
			prev_button = self.lens_buttons[self.selected_lens]
			prev_button.SetBitmapLabel(prev_button.default_img)
			self.selected_lens = 1
			button = self.lens_buttons[self.selected_lens]
			button.SetBitmapLabel(button.selected_img)
		else:
			self.StartTimer()

	def OnLens70(self, event):
		"""70-degree-lens button callback."""
		self.ChangeLens(70)
		self.ShowSimulation()
		if self.timer.use_haptic and self.selected_lens != 2:
			prev_button = self.lens_buttons[self.selected_lens]
			prev_button.SetBitmapLabel(prev_button.default_img)
			self.selected_lens = 2
			button = self.lens_buttons[self.selected_lens]
			button.SetBitmapLabel(button.selected_img)
		else:
			self.StartTimer()

	def SelectPreviousLens(self):
		"""Move the lens selection to the left.

		If the selection is on the very left button, next button selected
		will be the very right one.
		""" 
		prev_button = self.lens_buttons[self.selected_lens]
		prev_button.SetBitmapLabel(prev_button.default_img)
		self.selected_lens = (self.selected_lens - 1) % len(self.lens_buttons)
		button = self.lens_buttons[self.selected_lens]
		button.SetBitmapLabel(button.selected_img)

	def SelectNextLens(self):
		"""Move the lense selection to the right.

		If the selection is on the very right button, next button selected
		will be the very left one.
		"""
		prev_button = self.lens_buttons[self.selected_lens]
		prev_button.SetBitmapLabel(prev_button.default_img)
		self.selected_lens = (self.selected_lens + 1) % len(self.lens_buttons)
		button = self.lens_buttons[self.selected_lens]
		button.SetBitmapLabel(button.selected_img)

	def ApplyLensSelection(self):
		"""Apply the lens inclination selected."""
		self.ChangeLens(self.lens_buttons[self.selected_lens].angle)

	def SelectPreviousTool(self):
		"""Move the tool selection upwards.

		If the selection is on the top, next button selected will be
		the bottom one.
		Side effects are taken into account.
		"""
		button_id = self.tool_buttons.GetSelectedButtonId()
		if button_id == -1:
			n = self.tool_buttons.GetNumberOfVisibleButtons()
			button_id = tool_id = n - 1
		else:
			button_id = tool_id = button_id - 1
			if tool_id < 0:
				tool_id = 0
				
		if self.use_haptic:
			self.simulation.GetHapticDevice().UpdateScenario()

		if not self.style.ChangeTool(tool_id):
			self.ShowToolWarning()
			return
		else:
			self.tool_buttons.SelectButtonById(button_id)
			
		if self.use_haptic:
			haptic = self.simulation.GetHapticDevice()
			haptic.GetTools().RemoveAllItems()
			if self.tool_buttons.GetSelectedButtonName() != 'camera':
				haptic.AddTool(self.tool_buttons.GetSelectedButton().Tool)

		# In order to mantain control of insertion gauge
		self.tool_depth = 0
		self.inGauge.SetValue(0)

	def SelectNextTool(self):
		"""Move the tool selection upwards.

		If the selection is on the button, next button selected will be
		the top one.
		Side effects are taken into account.
		"""
		button_id = self.tool_buttons.GetSelectedButtonId()
		n = self.tool_buttons.GetNumberOfVisibleButtons()
		if button_id == n - 1:
			tool_id = n - 1
			button_id = -1
		else:
			button_id = tool_id = button_id + 1

		if self.use_haptic:
			self.simulation.GetHapticDevice().UpdateScenario()
			
		if not self.style.ChangeTool(tool_id):
			self.ShowToolWarning()
			return
		else:
			self.tool_buttons.SelectButtonById(button_id)
			
		if self.use_haptic:
			haptic = self.simulation.GetHapticDevice()
			haptic.GetTools().RemoveAllItems()
			if self.tool_buttons.GetSelectedButtonName() != 'camera':
				haptic.AddTool(self.tool_buttons.GetSelectedButton().Tool)

		# In order to mantain control of insertion gauge
		self.tool_depth = 0
		self.inGauge.SetValue(0)

	def OnCameraButton(self, event):
		"""Camera button callback function."""
		if self.tool_buttons.GetSelectedButtonName() == 'camera':
			return

		if not self.style.ChangeTool(self.tool_buttons.GetSelectedButtonId()):
			self.ShowToolWarning()
			return

		self.tool_buttons.SelectButtonByName('camera')
		self.timer.CuttingOff()

		if self.use_haptic:
			haptic = self.simulation.GetHapticDevice()
			haptic.GetTools().RemoveAllItems()

		# In order to mantain control of insertion gauge
		self.tool_depth = 0
		self.inGauge.SetValue(0)

	def OnToolButton(self, button_name):
		"""Generic tool button callback function."""
		if button_name == self.tool_buttons.GetSelectedButtonName():
			return

		if not self.style.ChangeTool(self.tool_buttons.GetButtonIdByName(button_name)):
			self.ShowToolWarning()
			return

		self.tool_buttons.SelectButtonByName(button_name)

		if self.tool_buttons.GetSelectedButtonName() == 'cutter':
			self.timer.CuttingOn()
		else:
			self.timer.CuttingOff()

		if self.use_haptic:
			haptic = self.simulation.GetHapticDevice()
			haptic.GetTools().RemoveAllItems()
			haptic.AddTool(self.tool_buttons.GetSelectedButton().Tool)

		# In order to mantain control of insertion gauge
		self.tool_depth = 0
		self.inGauge.SetValue(0)
	
	def OnCauterizerButton(self, event):
		"""Cauterizer button callback function."""
		self.OnToolButton('cauterizer')
	
	def OnBrushButton(self, event):
		"""Brush button callback function."""
		self.OnToolButton('brush')
	
	def OnCutterButton(self, event):
		"""Cutter button callback function."""
		self.OnToolButton('cutter')
	
	def OnClose(self, event):
		"""Close event callback function."""
		# Stop timer
		self.timer.Stop()
		# Delete all objects
		self.renWin.InvokeEvent("DeleteAllObjects")
		# Finally exit. Previous actions were only preventively made.
		sys.exit()

	def OnKeyDown(self, event):
		"""Forward key events to other GUI elements."""
		# Just enough to allow other items to catch key events
		self.widget.OnKeyDown(event)
		event.Skip()
		
	def OnMouseEvent(self, event):
		"""Forward mouse events to other GUI elements."""
		# Just enough to allow other items to catch mouse events
		event.Skip()

	def OnMouseWheel(self, event):
		"""Forward mouse-wheel events to other GUI elements."""
		# Just enough to allow other items to catch mouse events
		self.widget.OnMouseWheel(event)
		event.Skip()

	def StartTimer(self):
		"""Start the simulation timer."""
		self.timer.Start(40, wx.TIMER_CONTINUOUS)
		#self.timer.StartSimulation()

	def UpdateNail(self, opening):
		"""Update the nail extraction."""
		# Check tool selected
		if self.nail and self.tool_buttons.GetSelectedButtonName() == 'cauterizer':
			nail = self.nail
			new_depth = opening
			nail.Translate(0,0,new_depth - nail.depth)
			nail.depth = new_depth
			nail.Modified()

	def AddToolInsertion(self, insertion):
		"""Change the tool insertion."""
		if self.tool_buttons.GetSelectedButtonName() == 'camera':
			return

		self.tool_depth += insertion
		if self.tool_depth < 0:
			self.tool_depth = 0
		elif self.tool_depth <= self.inGauge.GetRange():
			self.inGauge.SetValue(self.tool_depth)
