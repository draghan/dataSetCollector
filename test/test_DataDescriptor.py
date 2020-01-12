#
#    This file is distributed under MIT License.
#    Copyright (c) 2020 draghan
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#

from unittest import TestCase
from dataDescriptor import DataDescriptor


class TestDataDescriptor(TestCase):
    @staticmethod
    def get_a(count: int):
        s = ""
        for i in range(0, count):
            s = s + "a"
        return s

    @staticmethod
    def get_b(count: int, suffix: str):
        s = ""
        for i in range(0, count):
            s = s + "b"
        return s + suffix

    def test_basic_init(self):
        a = DataDescriptor("a", self.get_a)

        self.assertEqual(a.name, "a")
        self.assertEqual(a.data(1), "a")
        self.assertEqual(a.data(3), "aaa")

        b = DataDescriptor("b", self.get_b)
        self.assertEqual(b.name, "b")
        self.assertEqual(b.data(1, "a"), "ba")
        self.assertEqual(b.data(3, "123"), "bbb123")

    def test_transformation(self):
        c = DataDescriptor("a", self.get_a, lambda s: s.replace("a", "c"))
        self.assertEqual(c.name, "a")
        self.assertEqual(c.data(1), "c")
        self.assertEqual(c.data(3), "ccc")
