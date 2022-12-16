#!/usr/bin/env python3

import angr
import claripy
import logging

logging.getLogger('angr').setLevel(logging.ERROR)
logging.getLogger('cle').setLevel(logging.ERROR)
BASE = 0x400000
good = BASE+0x1876
bad = [BASE+0x11b1, BASE+0x1182, BASE+0x1889]

flag = claripy.BVS('flag', 8*32)

proj = angr.Project('./spookylicence', auto_load_libs=False)
args = [proj.filename, flag]
state = proj.factory.entry_state(args=args)
simgr = proj.factory.simulation_manager(state)
simgr.explore(find=good, avoid=bad)

if len(simgr.found) < 1:
    quit(1)
print(simgr.found[0].solver.eval(flag, cast_to=bytes).decode('utf-8'))
