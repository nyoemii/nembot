# update_RTSS_overlay.py
#
# Copyright (C) 2025  <https://github.com/upgradeQ>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import threading
from random import randint
from time import sleep
from pathlib import Path

p = Path(__file__).resolve().parent
sys.path.append(p)  # dll must be in path
import clr  # python -m pip install pythonnet

clr.AddReference("RTSSSharedMemoryNET")
from RTSSSharedMemoryNET import OSD

overlay = OSD("st")
overlay2 = OSD("test2")


def update_status_multi():
	osds = [OSD(f"overlay_{i}_instance") for i in range(8)]
	for osd in osds:
		data = "random run #" + str(randint(0, 100))
		osd.Update(data)
		osd.UpdateColor(randint(0, 0xFFFFFFFF))
		osd.UpdatePosition(randint(0, 1920), randint(0, 1080))
		sleep(1 / 0.5)


def update_status():
	data = "random run #" + str(randint(0, 100))
	overlay.Update(data)
	overlay.UpdatePosition(randint(0, 1920), randint(0, 1080))
	overlay2.UpdateColor(randint(0, 0xFFFFFFFF))
	sleep(1 / 1)
	data = "random run #" + str(randint(0, 100))
	overlay2.UpdatePosition(randint(0, 1920), randint(0, 1080))
	overlay2.Update(data)
	overlay.UpdateColor(randint(0, 0xFFFFFFFF))
	app = overlay.GetAppEntries()[0]
	print(app.ProcessId, app.Name)
	print("{0}, {1}FPS", app.Flags, app.InstantaneousFrames)


def update_thread():
	while True:
		try:
			update_status()
			# update_status_multi()
		except:
			pass


t = threading.Thread(target=update_thread, daemon=True)
t.start()
try:
	while 1:
		sleep(60)
except KeyboardInterrupt:
	print("shutting down")
