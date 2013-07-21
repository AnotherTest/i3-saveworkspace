import i3, os, pickle

def getPid(win_id):
    """ Gets the proccess ID from a window ID """
    with os.popen("xprop -id %d _NET_WM_PID" % win_id) as p:
        return p.read().split("=")[1].strip()

def getCmd(win_id):
    with os.popen("ps w -p " + getPid(win_id)) as p:
        return p.readlines()[1].split(" ")[-1].strip()

class Container:
    def __init__(self, node):
        self._left = Container(node["nodes"][0]) if len(node["nodes"]) > 0 else None
        self._right = Container(node["nodes"][1]) if len(node["nodes"]) > 1 else None
        self._is_win = bool(node["window"])
        self._cmd = getCmd(node["window"]) if self._is_win else None
        rect = node["rect"]
        self._xy = (int(rect["x"]), int(rect["y"]))
        self._wh = (int(rect["width"]), int(rect["height"]))
        self._orientation = node["orientation"] if not self._is_win else None
        self._layout = node["layout"] if not self._is_win else None

    def makeTasks(self, tasks, resize = False):
        if self._is_win:
            tasks.append(("run", self._cmd))
            if resize:
                tasks.append(("resize", self._wh))
        else:
            should_resize = False # Unimplemented
            self._left.makeTasks(tasks, should_resize)
            tasks.append(("orientation", self._orientation))
            tasks.append(("layout", self._layout))
            if self._right:
                self._right.makeTasks(tasks, should_resize)

def findWorkspace(tree, workspace):
    find = lambda nodes, name: next(n for n in nodes if n["name"] == name)
    content = find(tree["nodes"][1]["nodes"], "content")
    return find(content["nodes"], workspace)

current = [ws for ws in i3.get_workspaces() if ws["focused"]][0]
tree = i3.get_tree()
workspace = findWorkspace(tree, current["name"])
tasks = []
wins = Container(workspace)
wins.makeTasks(tasks)
print tasks
pickle.dump(tasks, open(current["name"] + ".workspace", "w"))
