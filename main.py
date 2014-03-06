"""HysTrainer main module.

HysTrainer is a prototype application developed in 2014 by David
Castillo Bolado as part of a Master Thesis Project in the ULPGC,
in colaboration with the ITC.

Its purpose is to show the capabilites of the ESQUI environment,
in conjunction with some additional free software, to build
a virtual surgical simulation. In particular, HysTrainer is
intended to simulate hysteroscopy-alike scenarios.

This software has been proposed, managed and advised by Miguel Angel 
Rodriguez Florido (ITC and CTM-ULPGC).

The software is based in VTK (www.vtk.org) and Tcl/Tk (www.tcl.tk). Both 
packages used under the terms of the Free Software Foundation license BSD
(www.fsf.org). It is also based in Python and wxPython, used under the
terms of the Python Software Fundation (www.python.org/psf) and the LGPL.

This software is free software; you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License (LGPL) as published
by the Free Software Foundation, either version 3 of the License, or (at 
your option) any later version.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1) Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2) Redistributions in binary form must reproduce the above copyright 
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

You should have received a copy of the GNU Lesser General Public License 
along with this program.  If not, see <http://www.gnu.org/licenses/>.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
''AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
"""

from common import *
from SimulationApp import *

if __name__ == '__main__':
	# Redirect vtk errors to txt in stead of pop-up window
	""" NOT DESIRED IN FINAL APP
	if os.name == 'nt':
		fout = vtk.vtkFileOutputWindow()
		fout.SetFileName('c:/david/12-finalApp-errors.txt')
		fout.SetInstance(fout)
	"""
	# Run app
	app = SimulationApp()
	app.MainLoop()