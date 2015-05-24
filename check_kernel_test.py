#!/usr/bin/python
from __future__ import division
import sys

# Require Python 3 for unittest.mock
if sys.version_info[0] < 3:
    print("This script requires Python version 3")
    sys.exit(1)

import unittest
import unittest.mock

from check_kernel import clean_kernel_version, Version
import check_kernel


class CleanKernelVersionTestCase(unittest.TestCase):
    def testDebian(self):
        versions = [('3.16.7-ckt9-3~deb8u2', '3.16.7-ckt9-3~deb8u2')]
        for dirty, clean in versions:
            self.assertEqual(clean_kernel_version(dirty), Version(clean))

    def testFedora(self):
        versions = [('4.0.4-301.fc22.x86_64', '4.0.4-301'),
                    ('4.0.0-1.fc22', '4.0.0-1')]
        for dirty, clean in versions:
            self.assertEqual(clean_kernel_version(dirty), Version(clean))


class RunningKernelVersionTestCase(unittest.TestCase):
    def testFedora(self):
        with unittest.mock.patch.object(check_kernel, 'proc_version', return_value='Linux version 4.0.3-301.fc22.x86_64 (mockbuild@bkernel02.phx2.fedoraproject.org) (gcc version 5.1.1 20150422 (Red Hat 5.1.1-1) (GCC) ) #1 SMP Thu May 21 13:10:33 UTC 2015'):
            self.assertEqual(check_kernel.running_kernel_version(),
                             Version('4.0.3-301'))

    def testDebian(self):
        with unittest.mock.patch.object(check_kernel, 'proc_version', return_value='Linux version 3.16.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.8.4 (Debian 4.8.4-1) ) #1 SMP Debian 3.16.7-ckt9-3~deb8u1 (2015-04-24)'):
            self.assertEqual(check_kernel.running_kernel_version(),
                             Version('3.16.7-ckt9-3~deb8u1'))

        with unittest.mock.patch.object(check_kernel, 'proc_version', return_value='Linux version 2.6.32-5-amd64 (Debian 2.6.32-48squeeze11) (ben@decadent.org.uk) (gcc version 4.3.5 (Debian 4.3.5-4) ) #1 SMP Wed Feb 18 13:14:10 UTC 2015'):
            self.assertEqual(check_kernel.running_kernel_version(),
                             Version('2.6.32-48squeeze11'))


class VersionTestCase(unittest.TestCase):
    def testStr(self):
        self.assertEqual(str(Version('1.0')), '1.0')

    def testComparingTrivial(self):
        self.assertEqual(Version('1.0'), Version('1.0'))
        self.assertEqual(Version('2.6.32-5foo1'), Version('2.6.32-5foo1'))

        self.assertGreater(Version('2.0'), Version('1.0'))

    def testComparingNonTrivial(self):
        self.assertGreater(Version('2.12'), Version('2.2'))
        self.assertGreater(Version('3.12-12'), Version('3.12-2'))
        self.assertGreater(Version('2.6.32-5foo1'), Version('2.6.32-5foo0'))


if __name__ == '__main__':
    unittest.main()
