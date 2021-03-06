# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2016 Canonical Ltd
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

import integration_tests


class MainTestCase(integration_tests.TestCase):

    def test_main(self):
        project_dir = 'assemble'
        output = self.run_snapcraft('list-plugins', project_dir)
        expected = ('ant        catkin  copy  jdk     kernel  maven  '
                    'nodejs   python3  tar-content\n'
                    'autotools  cmake   go    kbuild  make    nil    '
                    'python2  scons  \n')

        self.assertEqual(expected, output)
