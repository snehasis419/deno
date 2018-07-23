#!/usr/bin/env python
import os
from util import run, g

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
third_party_path = os.path.join(root_path, "third_party")
prettier = os.path.join(third_party_path, "node_modules", "prettier",
                        "bin-prettier.js")
tools_path = os.path.join(root_path, "tools")
rustfmt_config = os.path.join(tools_path, "rustfmt.toml")

os.chdir(root_path)

# TODO(ry) Use third_party/depot_tools/clang-format.
run(["clang-format", "-i", "-style", "Google"] + g("src", ".cc", ".h"))

for fn in ["BUILD.gn", ".gn"] + g("build_extra", ".gn", ".gni"):
    run(["gn", "format", fn])

# TODO(ry) Install yapf in third_party.
run(["yapf", "-i"] + g("tools/", ".py") + g("build_extra", ".py"))

run(["node", prettier, "--write"] + g("js/", ".js", ".ts") +
    ["tsconfig.json", "tslint.json"])

# Set RUSTFMT_FLAGS for extra flags.
rustfmt_extra_args = []
if 'RUSTFMT_FLAGS' in os.environ:
    rustfmt_extra_args += os.environ['RUSTFMT_FLAGS'].split()
run([
    "rustfmt", "--config-path", rustfmt_config, "--error-on-unformatted",
    "--write-mode", "overwrite"
] + rustfmt_extra_args + g("src/", ".rs"))
