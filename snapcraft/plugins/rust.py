# Copyright (C) 2016 Marius Gripsgard (mariogrip@ubuntu.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This rust plugin is useful for building rust based parts.

Rust uses cargo to drive the build.

This plugin uses the common plugin keywords as well as those for "sources".
For more information check the 'plugins' topic for the former and the
'sources' topic for the latter.

Additionally, this plugin uses the following plugin-specific keywords:

    - rust-channel
      (string)
      select rust channel (stable, beta, nightly)
    - rust-revision
      (string)
      select rust version
"""

import os
import snapcraft


class RustPlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()
        schema['properties']['rust-channel'] = {
            'type': 'string',
        }
        schema['properties']['rust-revision'] = {
            'type': 'string',
        }
        return schema

    def __init__(self, name, options, project):
        super().__init__(name, options, project)
        self._rustpath = os.path.join(self.partdir, "rust")
        self._rustc = os.path.join(self._rustpath, "bin", "rustc")
        self._rustdoc = os.path.join(self._rustpath, "bin", "rustdoc")
        self._cargo = os.path.join(self._rustpath, "bin", "cargo")
        self._rustlib = os.path.join(self._rustpath, "lib")

    def build(self):
        super().build()
        self.run([self._cargo, "install",
                  "-j{}".format(self.project.parallel_build_count),
                  "--root", self.installdir])

    def env(self, root):
        env = ["RUSTC=%s" % self._rustc,
               "RUSTDOC=%s" % self._rustdoc,
               "RUST_PATH=%s" % self._rustlib]
        return env

    def pull(self):
        super().pull()
        self._fetch_rust()

    def _fetch_rust(self):
        options = []

        if self.options.rust_revision:
            options.append("--revision=%s" % self.options.rust_revision)

        if self.options.rust_channel:
            if self.options.rust_channel in ["stable", "beta", "nightly"]:
                options.append("--channel=%s" % self.options.rust_channel)
            else:
                raise EnvironmentError("%s is not a valid rust channel"
                                       % self.options.rust_channel)

        rustup = "rustup.sh"
        self.run(["wget", "-N", "https://static.rust-lang.org/rustup.sh",
                  "-O", rustup])
        self.run(["chmod", "+x", rustup])
        self.run(["./%s" % rustup,
                  "--prefix=%s" % self._rustpath,
                  "--disable-sudo", "--save"])
