#!/usr/bin/python
from __future__ import division
import sys

# Require Python 3 for unittest.mock
if sys.version_info[0] < 3:
    print("This script requires Python version 3")
    sys.exit(1)

from distutils.version import LooseVersion
import unittest
import unittest.mock

from check_kernel import clean_kernel_version
import check_kernel


class CleanKernelVersionTestCase(unittest.TestCase):
    def testFedora(self):
        versions = [('4.0.4-301.fc22.x86_64', '4.0.4-301'),
                    ('4.0.0-1.fc22', '4.0.0-1')]
        for dirty, clean in versions:
            self.assertEqual(clean_kernel_version(dirty), LooseVersion(clean))


class RunningKernelVersionTestCase(unittest.TestCase):
    def testFedora(self):
        with unittest.mock.patch.object(check_kernel, 'proc_version', return_value='Linux version 4.0.3-301.fc22.x86_64 (mockbuild@bkernel02.phx2.fedoraproject.org) (gcc version 5.1.1 20150422 (Red Hat 5.1.1-1) (GCC) ) #1 SMP Thu May 21 13:10:33 UTC 2015'):
            self.assertEqual(check_kernel.running_kernel_version(),
                             LooseVersion('4.0.3-301'))


if __name__ == '__main__':
    unittest.main()
