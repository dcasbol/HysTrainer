"""Lens disk emulation module.

Here is defined the class LensDisk
"""

import vtk

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class LensDisk:
	"""Emulate the vision through a endoscopic lens.

	The scenario must be assigned at creation.
	ld = LensDisk(scenario)

	Needs to be initialized after the simulation object.
	"""

	def __init__(self, scenario):
		self.Initialized = False
		self.sc = scenario
	
	def Initialize(self):
		"""Prepare the class to work."""

		self.Initialized = True
		
		# Radius
		self.r = r = 0.1
		
		# Disk
		self.diskSrc = diskSrc = vtk.vtkDiskSource()
		diskSrc.SetCircumferentialResolution(50)
		diskSrc.SetInnerRadius(r)
		diskSrc.SetOuterRadius(3*r)
		diskSrc.Update()
		
		# Lens Triangle
		self.trianglePoints = trianglePoints = vtk.vtkPoints()
		trianglePoints.InsertNextPoint(0,-r*0.9,0)
		trianglePoints.InsertNextPoint(-r*0.05,-r,0)
		trianglePoints.InsertNextPoint(r*0.05,-r,0)
		
		self.triangleSrc = triangleSrc = vtk.vtkTriangle()
		for i in range(3):
			triangleSrc.GetPointIds().SetId(i,i)
			
		self.triangleCells = triangleCells = vtk.vtkCellArray()
		triangleCells.InsertNextCell(triangleSrc)
		
		self.trianglePD = trianglePD = vtk.vtkPolyData()
		trianglePD.SetPoints(trianglePoints)
		trianglePD.SetPolys(triangleCells)
		
		# Mappers
		self.diskMapper = diskMapper = vtk.vtkPolyDataMapper()
		diskMapper.SetInputConnection(diskSrc.GetOutputPort())
		
		self.triangleMapper = triangleMapper = vtk.vtkPolyDataMapper()
		triangleMapper.SetInput(trianglePD)
		
		# Actors
		self.diskActor = diskActor = vtk.vtkFollower()
		diskActor.SetMapper(diskMapper)
		diskActor.GetProperty().SetColor(0,0,0)
		
		self.triangleActor = triangleActor = vtk.vtkFollower()
		triangleActor.SetMapper(triangleMapper)
		triangleActor.GetProperty().SetColor(0,0,0)
		
		# Positioning
		self.cam = self.sc.GetCamera()
		self.p = self.cam.GetPosition()
		self.d = d = self.cam.GetDirectionOfProjection()
		factor = 0.2
		diskActor.AddPosition(self.p[0] + factor*d[0], \
			self.p[1] + factor*d[1], self.p[2] + factor*d[2])
		triangleActor.AddPosition(self.p[0] + factor*d[0], \
			self.p[1] + factor*d[1], self.p[2] + factor*d[2])
		
		self.ren = ren = self.sc.GetRenderWindow().GetRenderers().GetFirstRenderer()
		ren.AddActor(diskActor)
		ren.AddActor(triangleActor)
		diskActor.SetCamera(self.cam)
		triangleActor.SetCamera(self.cam)
	
	def GetActors(self):
		"""Return all vtkActors involved in a list."""
		return [self.diskActor, self.triangleActor]
	
	def Update(self):
		"""Update the lens position."""

		# Set new position
		p0 = self.p
		d0 = self.d
		p1 = self.cam.GetPosition()
		d1 = self.cam.GetDirectionOfProjection()
		f = 0.2

		diff = (p0[0]-p1[0],p0[1]-p1[1],p0[2]-p1[2],d0[0]-d1[0],d0[1]-d1[1],d0[2]-d1[2])
		if sum(diff) != 0:
			self.diskActor.AddPosition(f*(d1[0] - d0[0]) + p1[0] - p0[0], \
				f*(d1[1] - d0[1]) + p1[1] - p0[1], f*(d1[2] - d0[2]) + p1[2] - p0[2])
			self.triangleActor.AddPosition(f*(d1[0] - d0[0]) + p1[0] - p0[0], \
				f*(d1[1] - d0[1]) + p1[1] - p0[1], f*(d1[2] - d0[2]) + p1[2] - p0[2])

			self.p = p1
			self.d = d1

	def Rotate(self, angle):
		"""Rotate the lens."""
		self.diskActor.RotateZ(angle)
		self.triangleActor.RotateZ(angle)
