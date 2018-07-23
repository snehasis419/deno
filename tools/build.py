#!/usr/bin/env python
# Copyright 2018 the Deno authors. All rights reserved. MIT license.
import argparse
import os
import sys
from os.path import join
from util import run
import distutils.spawn

parser = argparse.ArgumentParser(description='')
parser.add_argument(
    '--build_path', default='', help='Directory to build into.')
parser.add_argument('--args', default='', help='Extra gn args.')
parser.add_argument(
    '--mode',
    default='default',
    help='Build configuration: default, debug, release.')
options, targets = parser.parse_known_args()

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
third_party_path = join(root_path, "third_party")
depot_tools_path = join(third_party_path, "depot_tools")
gn_path = join(depot_tools_path, "gn")
ninja_path = join(depot_tools_path, "ninja")

os.chdir(root_path)

if options.build_path:
    build_path = options.build_path
else:
    build_path = join(root_path, "out", options.mode)

gn_args = []
gn_args += options.args.split()

if options.mode == "release":
    gn_args += ["is_official_build=true"]
elif options.mode == "debug":
    gn_args += ["is_debug=true"]
elif options.mode == "default":
    pass
else:
    print "Bad mode {}. Use release, debug, or default." % options.mode
    sys.exit(1)

ccache_path = distutils.spawn.find_executable("ccache")
if ccache_path:
    gn_args += ["cc_wrapper=\"%s\"" % ccache_path]

gn_cmd = [gn_path, "gen", build_path]
if len(gn_args) > 0:
    gn_cmd += ["--args='%s'" % " ".join(gn_args)]
run(gn_cmd)

target = " ".join(targets) if targets else ":all"
run([ninja_path, "-C", build_path, target])
