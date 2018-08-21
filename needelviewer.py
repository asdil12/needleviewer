#!/usr/bin/python3

# Author: Dominik Heidler <dheidler@suse.de>
# Copyright 2018 SUSE Linux LLC
# Licensed under the GPLv3 License

from tkinter import *
import sys
import os
import re
import json

if len(sys.argv) != 2:
	print("openQA Needle Viewer")
	print("")
	print("Usage (everything does the same):")
	print("  %s myneedle.png" % sys.argv[0])
	print("  %s myneedle.json" % sys.argv[0])
	print("  %s myneedle." % sys.argv[0])
	print("  %s myneedle" % sys.argv[0])
	sys.exit(2)

needle = sys.argv[1]
needle = re.sub(r"\.(png|json)?$", "", needle)

needle_name = os.path.basename(needle)
needle_png = needle + '.png'
needle_json = needle + '.json'


master = Tk(className="needleviewer")
master.title("Needle: %s" % needle_name)

c = Canvas(master, width=1024, height=768)
c.pack()

# load needle png into canvas
png = PhotoImage(file=needle_png)
c.create_image(0, 0, image=png, anchor=NW)

# load needle json
j = json.load(open(needle_json))

# draw areas
for area in j.get('area', []):
	x0 = area['xpos']
	y0 = area['ypos']
	x1 = x0 + area['width']
	y1 = y0 + area['height']

	if area['type'] == 'match':
		color = "green"
	elif area['type'] == 'ocr':
		color = 'yellow'
	elif area['type'] == 'exclude':
		color = 'red'

	c.create_line(x0, y0, x1, y0, fill=color, width=3)
	c.create_line(x0, y1, x1, y1, fill=color, width=3)
	c.create_line(x0, y0, x0, y1, fill=color, width=3)
	c.create_line(x1, y0, x1, y1, fill=color, width=3)

mainloop()
