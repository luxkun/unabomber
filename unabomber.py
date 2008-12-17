#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008  Ferraro Luciano (aka lux) <luciano.ferraro@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import getopt

import main as Main

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr::v", ["help", "res="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    res = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-r", "--res"):
            res = tuple(map(lambda x: int(x), a.split("x")))
        else:
            assert False, "unhandled option"
    
    Main.Core(res).run()

if __name__ == "__main__":
    main()