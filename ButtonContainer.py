"""Button management module.

Includes the class ButtonContainer."""

import vtkesqui
import wx

class ButtonContainer:
	"""Manage a set of tool buttons in a wxSizer.

	After creation and before usage, the sizer must
	have been set and the buttons must have been added.

	All buttons will be indexed by Model ID and by Name.
	Model ID for camera button is -1.
	"""

	def __init__(self):
		"""Constructor of ButtonContainer."""
		self.__visible_count = 0
		self.__button_by_id = list()
		self.__button_by_model = dict()
		self.__button_by_name = dict()
		self.__button_ids = dict()
		self.__button_names = dict()
		self.__selected_button = None
		self.__sizer = None

	def AddButton(self, button, name, model = -1):
		"""Add and index a button to the container.
		
		Usage:
			bc.AddButton(button, 'my_button', model = 4)

		Model ID is -1 by default (camera).
		"""
		self.__button_by_model[model] = button
		self.__button_by_name[name] = button
		self.__button_names[button] = name

	def RemoveAllButtons(self):
		"""Reset the button container."""
		self.__init__()

	def GetButtonById(self, bid):
		"""Get the button with the id given."""
		return self.__button_by_id[bid]

	def GetButtonByModel(self, model):
		"""Get the button with the model id given."""
		return self.__button_by_model[model]

	def GetButtonIdByName(self, name):
		"""Get the button with the name given."""
		return self.__button_ids[self.__button_by_name[name]]

	def GetNumberOfVisibleButtons(self):
		"""Get the number of buttons, except the camera one, that are not hidden."""
		return self.__visible_count

	def GetSelectedButton(self):
		"""Get the button that is currently selected."""
		return self.__selected_button

	def GetSelectedButtonId(self):
		"""Get the id of the currently selected button."""
		return self.__button_ids[self.__selected_button]

	def GetSelectedButtonName(self):
		"""Get the name of the currently selected button."""
		return self.__button_names[self.__selected_button]

	def HideAllButtons(self):
		"""Hide all buttons in the container, except the camera one."""
		for button in self.__button_by_id:
			button.Hide()
		
		size = len(self.__sizer.GetChildren())
		for i in range(size):
			self.__sizer.Remove(size-1-i)

		self.__visible_count = 0
		self.__button_by_id = list()
		self.__button_ids = dict()

	def SelectButton(self, button):
		"""Select a button by its reference.

		Change its image in order to highlight it.
		"""
		if self.__selected_button:
			self.__selected_button.SetBitmapLabel(self.__selected_button.default_img)
		button.SetBitmapLabel(button.selected_img)
		self.__selected_button = button

	def SelectButtonById(self, bid):
		"""Select a button by its id."""
		if bid >= 0:
			button = self.__button_by_id[bid]
			self.SelectButton(button)
		else:
			self.SelectButtonByName('camera')

	def SelectButtonByName(self, name):
		"""Select a button by its name."""
		button = self.__button_by_name[name]
		self.SelectButton(button)
		
	def SetSizer(self, sizer):
		"""Assign the sizer where the buttons will be managed."""
		self.__sizer = sizer

	def ShowButton(self, button, camera = False):
		"""Show a button and prepare it to be used.

		Set camera=True if the button represents a camera.
		"""
		if not camera:
			self.__button_by_id.append(button)
			self.__button_ids[button] = self.__visible_count
			self.__visible_count += 1
		else:
			self.__button_ids[button] = -1
			
		self.__sizer.Add(button, 0, wx.FIXED_MINSIZE | wx.ALL, border = 10)
		button.SetBitmapLabel(button.default_img)
		button.Show()

	def ShowButtonByName(self, name):
		"""Show the button with the name given."""
		button = self.__button_by_name[name]
		if name == 'camera':
			self.ShowButton(button, camera = True)
		else:
			self.ShowButton(button)

	def ShowButtonByModel(self, model):
		"""Show the button with the model id given."""
		button = self.__button_by_model[model]
		if model == -1:
			self.ShowButton(button, camera = True)
		else:
			self.ShowButton(button)
