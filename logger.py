#!/usr/bin/env python3

import sys, os, logging, errno
from pathlib import Path

from cli_args import *

conf.log_file = Path(conf.log_file)

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG if conf.debug else logging.INFO)
log = logging.getLogger(conf.log_user)

if os.path.dirname(conf.log_file) and \
    not os.path.isdir(os.path.dirname(conf.log_file)):
        os.mkdir(os.path.dirname(conf.log_file))
open(conf.log_file, 'w').close()

if os.path.dirname(conf.log_file) and \
    not os.path.exists(os.path.dirname(conf.log_file)):
        try: os.makedirs(os.path.dirname(conf.log_file))
        except OSError as exc:
            if exc.errno != errno.EEXIST: raise # Guard against race condition

with open(conf.log_file, "w") as f: pass

fh = logging.FileHandler(conf.log_file)  #Path(conf.saved_models) / 'log.txt'
log.addHandler(fh)

if __name__ == "__main__":
    pass