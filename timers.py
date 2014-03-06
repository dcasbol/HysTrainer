"""Timers module

Here are defined all timers involved in the simulation
process.
"""

from common import *
import time
import threading

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class NailMovingTimer(wx.Timer):
	"""Animate the nail when key 'A' pressed."""

	def __init__(self, frame, period = 2):
		"""Constructor.

		Usage in main frame constructor:
		nail_timer = NailMovingTimer(self)
		nail_timer.StartMoving()

		Better leave the default period.
		"""
		wx.Timer.__init__(self)
		self.frame = frame
		self.count = 0
		self.delta = -0.1
		self.nail_depth = 0

	def Notify(self):
		"""Callback function."""
		if self.count == 20:
			self.Stop()
			return
		elif self.count == 10:
			self.delta = -self.delta
		
		self.nail_depth += self.delta
		self.frame.UpdateNail(self.nail_depth)
		self.count += 1

	def StartMoving(self):
		"""Timer firing method."""
		self.Start(100, wx.TIMER_CONTINUOUS)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class DialogHidingTimer(wx.Timer):
	"""Hide a dialog after some seconds."""

	def __init__(self, frame, period = 2):
		"""Constructor.

		Usage in main frame constructor:
		dialog_timer = DialogHidingTimer(self)
		dialog_timer.StartHiding()

		Better leave the default period.
		"""
		wx.Timer.__init__(self)
		self.frame = frame
		self.period = period * 1000

	def Notify(self):
		"""Callback function."""
		self.frame.Show(False)

	def StartHiding(self):
		"""Timer firing method."""
		self.Start(self.period, wx.TIMER_ONE_SHOT)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CutDisapearTimer(wx.Timer):
	"""Animate two element parts while fading them out."""

	def __init__(self, renderer, actor_1, actor_2, period = 3):
		"""Constructor.

		Usage:
		cut_timer = CutDisapearTimer(renderer, actor_upper_part, actor_downer_part)
		cut_timer.StartDisapearing()

		Better use default timing.
		"""
		wx.Timer.__init__(self)
		self.ren = renderer
		self.actor_1 = actor_1
		self.actor_2 = actor_2
		self.count = int(period*10)
		self.period = period
		self.opacity_step = 1/float(self.count)
		self.opacity = 1
		self.rotation_step = 90/float(self.count)
		self.translation_step = 1/float(self.count)

	def Notify(self):
		"""Callback function.

		Make a split & hide effect between two parts.
		"""
		self.actor_1.RotateZ(self.rotation_step)
		self.actor_1.AddPosition(0,self.translation_step,0)
		self.actor_1.GetProperty().SetOpacity(self.opacity)
		self.actor_2.GetProperty().SetOpacity(self.opacity)
		self.opacity -= self.opacity_step
		self.count -= 1
		if self.count <= 0:
			self.Stop()
			self.ren.RemoveActor(self.actor_1)
			self.ren.RemoveActor(self.actor_2)

	def StartDisapearing(self):
		"""Timer firing method."""
		self.Start(100, wx.TIMER_CONTINUOUS)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class SimulationTimer(wx.Timer):
	"""Main simulation timer.

	Coordinate main simulation process and haptic interaction.
	"""

	def __init__(self):
		wx.Timer.__init__(self)
		
		# Flags
		self.Initialized = False
		self.Highlight = False
		self.use_haptic = False
		self.state = 0
		self.left_pedal_pressed = False
		self.right_pedal_pressed = False
		self.cutting = False
		
		# External Attributes
		self.Simulation = None
		self.Scenario = None
		
		# Internal Attributes
		self.EmptyPD = vtk.vtkPolyData()
		self.Elements = list()
		self.Extractors = list()
		self.GFilters = list()
		self.Mappers = list()
		self.Actors = list()
		self.ren = None
		self.__timer = None
	
	def HighlightOn(self):
		"""Turn collision highlighting ON."""
		self.Highlight = True
	
	def HighlightOff(self):
		"""Turn collision highlighting OFF."""
		self.Highlight = False

	def CuttingOn(self):
		"""Turn cutting effect on collision ON."""
		self.cutting = True

	def CuttingOff(self):
		"""Turn cutting effect on collision OFF."""
		self.cutting = False
	
	def AddHighlightObject(self, obj):
		"""Add an object to highlight on collision."""
		elements = obj.GetElements()
		elements.InitTraversal()
		e = elements.GetNextElement()
		while e:
			self.AddHighlightElement(e)
			e = elements.GetNextElement()
	
	def AddHighlightElement(self, element):
		"""Add an element to highlight on collision."""
		self.Elements.append(element)
	
	def SetSimulation(self, Sim):
		"""Set the simulation object to be used."""
		if self.Simulation:
			self.Reset()
			
		self.Simulation = Sim
		self.Scenario = Sim.GetScenario()
		self.ren = self.Scenario.GetRenderWindow().GetRenderers().GetFirstRenderer()
	
	def Reset(self):
		"""Reset the timer to an initial state."""

		# Remove actors
		for a in self.Actors:
			self.ren.RemoveActor(a)
		
		# Restore flags
		self.Initialized = False
		self.Highlight = False
		
		# Restore all external attributes
		self.Scenario = None
		del self.Simulation
		self.Simulation = None
		
		# Restore all internal attributes
		del self.Elements
		self.Elements = list()
		del self.Extractors
		self.Extractors = list()
		del self.GFilters
		self.GFilters = list()
		del self.Mappers
		self.Mappers = list()
		del self.Actors
		self.Actors = list()
	
	def Initialize(self):
		"""Initialize timer and check haptic interaction."""
		if self.Initialized:
			return self.use_haptic

		self.Initialized = True
		
		# Set tools
		for e in self.Elements:
			e.Update()
			vis = e.GetVisualizationModel()
			# Create and set
			extractor = vtk.vtkExtractCells()
			extractor.SetInput(vis.GetInput())
			gfilter = vtk.vtkGeometryFilter()
			mapper = vtk.vtkPolyDataMapper()
			actor = vtk.vtkActor()
			actor.SetMapper(mapper)
			actor.GetProperty().SetColor(1,0,0)
			actor.GetProperty().SetOpacity(0.5)
			# Add to lists
			self.Extractors.append(extractor)
			self.GFilters.append(gfilter)
			self.Mappers.append(mapper)
			self.Actors.append(actor)
			# Add to renderer
			self.ren.AddActor(actor)
			# Identify cavity objects
			if e.GetName().find('cavity') >= 0:
				e.is_cavity = True
			else:
				e.is_cavity = False

		# Haptic use. Camera and camera volume.
		self.use_haptic = False
		try:
			self.haptic = self.Simulation.GetHapticDevice()
			if self.haptic and self.haptic.IsA('vtkSBM'):
				self.use_haptic = True
				# Set haptic attributes
				self.haptic.SetCamera(self.Scenario.GetCamera())
				# Look for camera volume
				objects = self.Scenario.GetObjects()
				objects.InitTraversal()
				o = objects.GetNextObject()
				while o:
					if o.IsA('vtkToolSingleChannel') and o.GetToolModel() == vtkesqui.vtkToolSingleChannel.Camera:
						self.haptic.SetCameraObject(o)
						o = None
					else:
						o = objects.GetNextObject()
				self.haptic.SetSingleChannel(True)

				# Check if object found and SBM connected
				if not self.haptic.GetCameraObject() or self.haptic.Init() <= 0:
					self.use_haptic = False
					self.Simulation.SetHapticDevice(None)

			else:
				self.Simulation.SetHapticDevice(None)
		except AttributeError:
			pass
		
		# Initialize simulation
		self.Simulation.Initialize()
		self.Simulation.SetCollisionModeToSimple()
		
		# Initialize interactor
		self.style = self.Simulation.GetInteractorStyle()
		self.style.Initialize()
		self.Lens = self.style.Lens
		self.Lens.LastRoll = 0

		if self.use_haptic:
			self.state = 1 # Wait for haptic extraction
		else:
			self.state = 0 # Start simulation

		return self.use_haptic

	def Interact(self):
		"""Update scenario from haptic data."""
		if self.use_haptic:
			self.haptic.UpdateScenario()
			Roll = self.haptic.GetLeftToolRoll()
			self.Lens.Rotate(Roll - self.Lens.LastRoll)
			self.Lens.Update()
			self.Lens.LastRoll = Roll

	def SimulationLoop(self):
		"""Main simulation loop iteration."""
		self.Interact()
		self.Simulation.Step()
		self.CutOnCollisions()
		self.SetHighlights()
		self.Scenario.Render()

	def StartSimulation(self):
		"""Timer firing method."""
		self.__timer = threading.Timer(0.04, self.Notify_2, [time.time()])
		self.__timer.start()
	
	def Notify(self):
		"""Main simulation timer callback.

		State machine. Control simulation states
		and GUI interaction through haptic device.
		"""
		if not self.Initialized:
			self.Initialize()
		# State 0: simulate
		if self.state == 0:
			self.SimulationLoop()
			if self.use_haptic:
				self.haptic.UpdateDevice()
				if self.haptic.GetLeftToolDepth() == 0.0:
					self.state = 2
				else:
					self.UpdatePedals()
					left = self.left_pedal_pressed
					right = self.right_pedal_pressed
					grasp = self.haptic.GetLeftToolOpening()

					# Use grasp to activate Nail
					self.parent.UpdateNail(grasp-1)
					
					# Use pedals to insert/extract tool
					if left and not right:
						insertion = self.haptic.GetToolInsertion()
						if insertion >= 0.1:
							self.haptic.SetToolInsertion(insertion - 0.1)
						else:
							self.haptic.SetToolInsertion(0.0)
						self.parent.AddToolInsertion(-1)
					elif not left and right:
						insertion = self.haptic.GetToolInsertion()
						self.haptic.SetToolInsertion(insertion + 0.1)
						self.parent.AddToolInsertion(1)

		elif self.use_haptic:
			self.haptic.UpdateDevice()
			# State 1: wait for haptic extraction
			if self.state == 1:
				# Initialization: wait for haptic extraction
				self.parent.ShowExtractText()
				depth = self.haptic.GetLeftToolDepth()
				if depth == 0.0:
					self.state = 2
			# State 2: Lens inclination/tool selection
			elif self.state == 2:
				depth = self.haptic.GetLeftToolDepth()
				if depth > 0.0:
					self.state = 0
					self.parent.ApplyLensSelection()
					self.parent.ShowSimulation()
				else:
					self.haptic.UpdateDevice()
					self.UpdatePedals()
					self.parent.ShowLenses()
					prev = self.left_pedal_click
					next = self.right_pedal_click
					grasp = self.haptic.GetLeftToolOpening()

					if prev and not next:
						if grasp < 0.5:
							self.parent.SelectPreviousTool()
						else:
							self.parent.SelectPreviousLens()
					elif not prev and next:
						if grasp < 0.5:
							self.parent.SelectNextTool()
						else:
							self.parent.SelectNextLens()

	def SetHighlights(self):
		"""Highlight registered elements on collisions.

		Working order:
			1. Get ColPoints.
			2. Map to VisPoints.
			3. Get correspondant cells.
			4. Get some neighbour cells.
			5. Highlight them.
		"""
		# Is this option enabled?
		if not self.Highlight:
			return
			
		# Each element must be highlighted
		#for eid in xrange(len(self.Elements)):
		#	e = self.Elements[eid]
		eid = 0
		for e in self.Elements:
			if e.IsEnabled():
				vis = e.GetVisualizationModel()
				col = e.GetCollisionModel()
				
				# Get point IDs
				pids = vtk.vtkIdList()
				cols = self.Simulation.GetCollisions()
				# TODO: comprobar si hay colisiones
				cols.InitTraversal()
				c = cols.GetNextCollision()
				while c:
					if c.GetObjectId() == e.GetObjectId():
						pids.InsertUniqueId(c.GetPointId())
					c = cols.GetNextCollision()
					
				# Map to VisPoints
				locator = vtk.vtkPointLocator()
				locator.SetDataSet(vis.GetInput())
				colpd = col.GetInput()
				visIds = vtk.vtkIdList()
				for i in xrange(pids.GetNumberOfIds()):
					colid = pids.GetId(i)
					vid = locator.FindClosestPoint(colpd.GetPoint(colid))
					visIds.InsertUniqueId(vid)
				
				# Get cells
				vispd = vis.GetInput()
				cids = vtk.vtkIdList()
				for i in range(visIds.GetNumberOfIds()):
					tempIds = vtk.vtkIdList()
					vispd.GetPointCells(visIds.GetId(i), tempIds)
					for j in range(tempIds.GetNumberOfIds()):
						cids.InsertUniqueId(tempIds.GetId(j))
						
				# Get some neighbour cells
				Neighbours = True
				if Neighbours:
					nbs = vtk.vtkIdList()
					for i in range(cids.GetNumberOfIds()):
						tempPointIds = vtk.vtkIdList()
						vispd.GetCellPoints(cids.GetId(i), tempPointIds)
						for j in range(tempPointIds.GetNumberOfIds()):
							tempCellIds = vtk.vtkIdList()
							vispd.GetPointCells(tempPointIds.GetId(j), tempCellIds)
							for k in range(tempCellIds.GetNumberOfIds()):
								nbs.InsertUniqueId(tempCellIds.GetId(k))
					for i in range(nbs.GetNumberOfIds()):
						cids.InsertUniqueId(nbs.GetId(i))
						
				# Highlight them
				if cids.GetNumberOfIds() == 0:
					self.Mappers[eid].SetInput(self.EmptyPD)
				else:
					self.Extractors[eid].SetCellList(cids)
					self.Extractors[eid].Update()
					self.GFilters[eid].SetInput(self.Extractors[eid].GetOutput())
					self.GFilters[eid].Update()
					self.Mappers[eid].SetInput(self.GFilters[eid].GetOutput())
					
				self.Mappers[eid].Update()
				self.Actors[eid].SetUserMatrix(col.GetActor().GetUserMatrix())
				if e.is_cavity:
					self.Actors[eid].SetScale(0.99)
				else:
					self.Actors[eid].SetScale(1.01)
				self.Actors[eid].GetProperty().SetOpacity(0.5)

			eid += 1

	def CutOnCollisions(self):
		"""If function activated, cut organ on collision.

		Split the element in two parts and make a split & fade effect.
		"""
		if not self.cutting:
			return

		for eid in xrange(len(self.Elements)):
			e = self.Elements[eid]
			if not e.is_cavity:
				cm = e.GetCollisionModel()
				cols = cm.GetCollisions()
				num_cols = cols.GetNumberOfCollisions()

				if num_cols > 0:
					# Is the colliding pair a blade?

					# Then go!
					vis = e.GetVisualizationModel()
					va = vis.GetActor()
					p = cols.GetCollision(0).GetPoint()
					n = [0,1,0]

					plane = vtk.vtkPlane()
					plane.SetOrigin(p)
					plane.SetNormal(n)

					cf = vtk.vtkClipPolyData()
					cf.SetValue(0)
					cf.GenerateClippedOutputOn()
					cf.SetInputConnection(vis.GetOutputPort())
					cf.SetClipFunction(plane)

					cutter = vtk.vtkCutter()
					cutter.SetInputConnection(vis.GetOutputPort())
					cutter.SetCutFunction(plane)
					strips = vtk.vtkStripper()
					strips.SetInputConnection(cutter.GetOutputPort())
					strips.Update()
					cutpoly = vtk.vtkPolyData()
					cutpoly.SetPoints(strips.GetOutput().GetPoints())
					cutpoly.SetPolys(strips.GetOutput().GetLines())
					cutpoly.Update()

					revpoly = vtk.vtkReverseSense()
					revpoly.SetInput(cutpoly)
					revpoly.ReverseNormalsOn()
					revpoly.Update()

					actor_1, actor_2 = (None, None)

					for i in range(2):
						piece = vtk.vtkAppendPolyData()
						cleaner = vtk.vtkCleanPolyData()
						txt_map = vtk.vtkTextureMapToSphere()
						txt_map.PreventSeamOn()
						mapper = vtk.vtkPolyDataMapper()
						actor = vtk.vtkActor()

						if i == 0:
							piece.AddInput(revpoly.GetOutput())
							piece.AddInput(cf.GetOutput())
							actor_1 = actor
						else:
							piece.AddInput(cutpoly)
							piece.AddInput(cf.GetClippedOutput())
							actor_2 = actor

						piece.Update()
						cleaner.SetInput(piece.GetOutput())
						cleaner.Update()

						txt_map.SetInput(cleaner.GetOutput())
						mapper.SetInput(txt_map.GetOutput())
						actor.SetMapper(mapper)
						actor.SetUserMatrix(va.GetUserMatrix())
						actor.SetTexture(va.GetTexture())
						actor.GetProperty().BackfaceCullingOn()
						self.ren.AddActor(actor)

					# Disable element so it doesn't bother anymore
					e.Disable()

					actor.dis_timer = dis_timer = CutDisapearTimer(self.ren, actor_1, actor_2)
					dis_timer.StartDisapearing()


	def UpdatePedals(self):
		"""Update haptic pedals information.

		Updated vars:
			left/right_pedal_click
			left/right_pedal_pressed
		"""
		left_pedal = self.haptic.GetLeftPedalState()
		if left_pedal:
			if not self.left_pedal_pressed:
				self.left_pedal_click = True
				self.left_pedal_pressed = True
			else:
				self.left_pedal_click = False
		else:
			self.left_pedal_click = False
			self.left_pedal_pressed = False
						
		right_pedal = self.haptic.GetRightPedalState()
		if right_pedal:
			if not self.right_pedal_pressed:
				self.right_pedal_click = True
				self.right_pedal_pressed = True
			else:
				self.right_pedal_click = False
		else:
			self.right_pedal_click = False
			self.right_pedal_pressed = False
			