import i3, os, subprocess, time, pickle
from multiprocessing import Process
def doOrientation(layout):
    if layout == "horizontal":
        i3.split("h")
    elif layout == "vertical":
        i3.split("v")
    else:
        print "WARNING: Unsupported orientation option %s." % layout

def resize((width, height)):
    rect = i3.filter(focused = True)[0]["rect"]
    delta_w = (width - rect["width"]) / 19
    delta_h = (height - rect["height"]) / 19
    print "Will resize by", (delta_w, delta_h)
    if delta_w < 0:
        i3.resize("shrink", "width", "{x} px or {x} ppt".format(x = -delta_w))
    else:
        i3.resize("grow", "width", "{x} px or {x} ppt".format(x = delta_w))    
    if delta_h < 0:
        i3.resize("shrink", "height", "{x} px or {x} ppt".format(x = -delta_h))
    else:
        i3.resize("grow", "height", "{x} px or {x} ppt".format(x = delta_h))

def make(tasks):
    for task in tasks:
        if task[0] == "run":
            Process(
                target = subprocess.call, args = (tuple(task[1].split(" ")), )
            ).start()
            time.sleep(1)
        elif task[0] == "resize":
            resize(task[1])
        elif task[0] == "orientation":
            doOrientation(task[1])
        elif task[0] == "layout":
            i3.layout(task[1])    
        time.sleep(1)

print "Workspace file?"
data = pickle.load(open(raw_input(), "r"))
print "Workspace name?"
name = raw_input()
curr = [ws for ws in i3.get_workspaces() if ws["focused"]][0]["name"]
i3.workspace(name)
make(data)
i3.workspace(curr)
