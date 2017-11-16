#! /usr/bin/env python
import sys

try :
    assert sys.version_info >= (3,6)
except Exception :
    print("""
              Your Python version is %d.%d. Minimum required is 3.6.
              If you want help for running different Python versions,
              consider using pyenv https://github.com/pyenv/pyenv""" % (sys.version_info[0],sys.version_info[1]))
    sys.exit()

import fire
import json
import logging
import mimetypes
import os
import sys

from picturealliance.cmdline import cmdline


logging.basicConfig(stream=sys.stdout,format="%(message)")



if __name__== '__main__' :
    import fire
    fire.Fire(cmdline)
