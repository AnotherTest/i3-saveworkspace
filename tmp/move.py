import i3, os, subprocess, time
from multiprocessing import Process

def moveMouse(x, y):
    os.system("xdotool mousemove %d %d" % (x, y))

def clickMouse():
    os.system("xdotool click 1")

def getPid(win_id):
    """ Gets the proccess ID from a window ID """
    with os.popen("xprop -id %d _NET_WM_PID" % win_id) as p:
        return p.read().split("=")[1].strip()

def getCmd(win_id):
    with os.popen("ps w -p " + getPid(win_id)) as p:
        return p.readlines()[1].split(" ")[-1].strip()

def doOrientation(layout):
    print "%s split." % layout
    if layout == "horizontal":
        i3.split("v")
    elif layout == "vertical":
        i3.split("h")
    else:
        print "WARNING: Unsupported orientation option %s." % layout

def focus(node):
    # Move mouse to focus the container
    moveMouse(int(node["rect"]["x"]) + 2, int(node["rect"]["y"]) + 2)
    clickMouse()

layout_tasks = []
def traverse(nodes):
    global layout_tasks
    for node in nodes:
        if node["window"]:
            cmd = getCmd(node["window"])
            print "Starting command: ", cmd
            Process(
                target = subprocess.call, args = (tuple(cmd.split(" ")), )
            ).start()
            time.sleep(1)
            focus(node)
            print layout_tasks
            if layout_tasks:
                doOrientation(layout_tasks[-1])
                del layout_tasks[-1]   
        else:
            # Note: should use "layout" but that doesn't work as expected
            layout_tasks.append(node["orientation"])
            time.sleep(1)
            traverse(node["nodes"])
        
def findWorkspace(tree, workspace):
    find = lambda nodes, name: next(n for n in nodes if n["name"] == name)
    content = find(tree["nodes"][1]["nodes"], "content")
    return find(content["nodes"], workspace)

current = [ws for ws in i3.get_workspaces() if ws["focused"]][0]
tree = i3.get_tree()
i3.workspace("new")
workspace = findWorkspace(tree, current["name"])
print workspace
traverse(workspace["nodes"])
i3.workspace(current['name'])
