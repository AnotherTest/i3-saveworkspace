import i3, os, subprocess, time, pickle
from multiprocessing import Process
def moveMouse(x, y):
    os.system("xdotool mousemove %d %d" % (x, y))
 
def clickMouse():
    os.system("xdotool click 1")

def doOrientation(layout):
    print "%s split." % layout
    if layout == "horizontal":
        i3.split("h")
    elif layout == "vertical":
        i3.split("v")
    else:
        print "WARNING: Unsupported orientation option %s." % layout

def focus((x, y)):
    # Move mouse to focus the container
    moveMouse(x + 2, y + 2)
    clickMouse()

def make(tasks):
    for task in tasks:
        if task[0] == "run":
            Process(
                target = subprocess.call, args = (tuple(task[1].split(" ")), )
            ).start()
            time.sleep(1)
        elif task[0] == "focus":
            focus(task[1])
        elif task[0] == "layout":
            doOrientation(task[1])
        time.sleep(1)
print "Workspace file?"
data = pickle.load(open(raw_input(), "r"))
print "Workspace name?"
name = raw_input()
curr = [ws for ws in i3.get_workspaces() if ws["focused"]][0]["name"]
i3.workspace(name)
make(data)
i3.workspace(curr)
