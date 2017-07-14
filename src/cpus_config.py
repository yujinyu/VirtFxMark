import os
import glob
from variables_defined import path_proc, path_sys


def is_int(s):
    if s.isdigit():
        return int(s)
    return s


#
# processor Range syntax
#

def parse_range(r):
    """
        Parse an integer sequence such as '0-3,8-11'.
        '' is the empty sequence.
    """
    if not r.strip ():
        return []

    res = []
    for piece in r.strip().split (","):
        lr = piece.split("-")
        if len (lr) == 1 and lr[0].isdigit ():
            res.append (int (lr[0]))
        elif len (lr) == 2 and lr[0].isdigit () and lr[1].isdigit ():
            res.extend (range (int (lr[0]), int (lr[1]) + 1))
        else:
            raise ValueError ("Invalid range syntax: %r" % r)
    return res


def get_cpus_parse_from_sys(name):
    return parse_range(file(path_sys + name).read ())


def get_cpus_info_from_proc():
    """
        Read a cpuinfo file and return [{field : value}].
    """

    res = []
    for block in file(path_proc, "r").read().split("\n\n"):
        if len(block.strip()):
            res.append({})
            for line in block.splitlines():
                k, v = map(str.strip, line.split(":", 1))
                res[-1][k] = is_int(v)
            # Try to get additional info
            processor = res[-1]["processor"]
            node_files = glob.glob(path_sys + "cpu%d/node*" % processor)
            if len(node_files):
                res[-1]["node"] = int(os.path.basename(node_files[0])[4:])
    return res


def set_cpus_onoff(cpuid, onoff):
    res = parse_range(cpuid)
    for ids in res:
        path = path_sys + "cpu%d/online" % int(ids)
        print >> file(path, "w"), onoff


def get_num_cpus():
    return len(parse_range(file(path_sys + "online").read()))

