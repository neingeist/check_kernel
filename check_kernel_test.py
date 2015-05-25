#!/usr/bin/python
from __future__ import division
import sys

import unittest

from check_kernel import clean_kernel_version, Version
import check_kernel


def patch_object(obj, function, return_value=None):
    """A simple replacement for unittest.mock.patch_object()

    It is not meant to used with the 'with' statement or as a decorator, unlike
    unittest.mock.patch_object(). To support Python <= 3.2."""
    def our_function():
        return return_value
    obj.__dict__[function] = our_function


# Patch up unittest.TestCase
if not hasattr(unittest.TestCase, 'assertGreater'):
    unittest.TestCase.assertGreater = lambda self, a, b: self.assertTrue(a > b)
if not hasattr(unittest.TestCase, 'assertLess'):
    unittest.TestCase.assertLess = lambda self, a, b: self.assertTrue(a < b)


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
        patch_object(check_kernel, 'proc_version', return_value='Linux version 4.0.3-301.fc22.x86_64 (mockbuild@bkernel02.phx2.fedoraproject.org) (gcc version 5.1.1 20150422 (Red Hat 5.1.1-1) (GCC) ) #1 SMP Thu May 21 13:10:33 UTC 2015')
        self.assertEqual(check_kernel.running_kernel_version(),
                         Version('4.0.3-301'))

    def testDebian(self):
        patch_object(check_kernel, 'proc_version', return_value='Linux version 3.16.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.8.4 (Debian 4.8.4-1) ) #1 SMP Debian 3.16.7-ckt9-3~deb8u1 (2015-04-24)')
        self.assertEqual(check_kernel.running_kernel_version(),
                         Version('3.16.7-ckt9-3~deb8u1'))

        patch_object(check_kernel, 'proc_version', return_value='Linux version 2.6.32-5-amd64 (Debian 2.6.32-48squeeze11) (ben@decadent.org.uk) (gcc version 4.3.5 (Debian 4.3.5-4) ) #1 SMP Wed Feb 18 13:14:10 UTC 2015')
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
        versions = [('2.2', '2.12'),
                    ('3.12-2', '3.12-12'),
                    ('2.6.32-5foo0', '2.6.32-5foo1'),
                    ('3.4.15-2', '3.16.7-ckt9-3~deb8u1'),
                    ('3.2.4', '3.2.4+2')]

        for lower, greater in versions:
            self.assertGreater(Version(greater), Version(lower))
            self.assertLess(Version(lower), Version(greater))

    def testSorting(self):
        l = [Version('3.16.5-1'), Version('3.2.60-1+deb7u3'),
             Version('3.16.3-2'), Version('3.16.7-ckt9-3~deb8u1'),
             Version('3.14.15-2')]
        self.assertEqual(sorted(l)[0], Version('3.2.60-1+deb7u3'))
        self.assertEqual(sorted(l)[-1], Version('3.16.7-ckt9-3~deb8u1'))


if __name__ == '__main__':
    unittest.main()
