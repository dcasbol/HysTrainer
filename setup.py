"""Setup script to make self-contained app."""

# Call this command to setup:
# python -OO setup.py (py2exe|py2app)

import os
import platform
from subprocess import call

if os.name == 'mac' or platform.system() == 'Darwin':

	# MACINTOSH
	from setuptools import setup

	APP = ['main.py']
	DATA_FILES = ['data', 'examples', 'resources']
	OPTIONS = {'argv_emulation': True,
	 'iconfile': 'resources/HysTrainer.icns'}
#	 'py2app':{'optimize':2}}

	setup(
	    app=APP,
	    data_files=DATA_FILES,
	    options={'py2app': OPTIONS},
	    setup_requires=['py2app'],
	)

elif os.name == 'nt':

	# WINDOWS
	from distutils.core import setup
	import py2exe

	setup(options = {'py2exe':{'optimize':2}},
		zipfile='lib/shared.zip',
		windows=[{'script':'main.py','icon_resources':[(1,'resources/HysTrainer.ico')]}])
