#!/usr/bin/env python3

import angr
import claripy

PROG_END = 0x401177

file = 'darn_mice.exe'

proj = angr.Project(file, load_options={
    'auto_load_libs': False,
    'main_opts': {
        'base_addr': 0x00400000
    }
})

args = claripy.BVS("arg1", 35*8)
stat = proj.factory.entry_state(args=[proj.filename, args])  # start from sub_401000

sims = proj.factory.simulation_manager(stat)
sims.explore(find=PROG_END)
print(sims.found)
