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
from dataSetCollector import DataSetCollector, get_data_sets_based_on_string_list


class TestDataSetCollectorScenarioTypeA(TestCase):
    """
        Consider the following scenario:
        Data (name, surname and age) is stored in one file, with differentiator in a form of identifier with a colon at
        the beginning of the line. For example:
            name: A
            surname: B
            age: 300
        Each file represents different data set.
    """

    @staticmethod
    def get_data_from_line_starting_with(filecontent: str, what: str):
        """ simple helper function which looks for line with requested differentiator """

        for line in filecontent.split("\n"):
            if line.startswith(what):
                return line.split(":")[1][1:]
        raise ValueError("Cannot find" + what + " in file")

    def test_type_a(self):

        # we have 3 pieces of data: name, surname and age
        # Lets define data descriptors:
        # All of those data pieces are stored inside common file, so the obtaining algorithm should work on the file
        # content and extract from the file content the requested piece of data.
        # We additionally want treat the age as integer number and surname should be all upper case - for some
        # presentation reason or something.
        descriptors = [
            DataDescriptor(name="name",
                           data_retrieving_functor=lambda file_content: self.get_data_from_line_starting_with(file_content, "name:")),

            DataDescriptor(name="surname",
                           data_retrieving_functor=lambda file_content: self.get_data_from_line_starting_with(file_content, "surname:"),
                           data_transformation_functor=lambda s: s.upper()),

            DataDescriptor(name="age",
                           data_retrieving_functor=lambda file_content: self.get_data_from_line_starting_with(file_content, "age:"),
                           data_transformation_functor=lambda age: int(age)),
        ]

        # algorithm for feeding the data descriptors should produce the filecontent based on the location of the
        # data set:
        def read_file(file_path: str):
            with open(file_path, 'r') as file:
                return file.read()

        # create data set collector:
        collector = DataSetCollector(data_descriptors_feeder=read_file,
                                     data_descriptors=descriptors)

        # base path for our data sets:
        base_path = "test/data/typeA/"

        # obtain data from set1:
        set1 = collector.data(base_path + "set1/data.txt")

        # obtain data from set2:
        set2 = collector.data(base_path + "set2/data.txt")

        # check correctness of data:
        self.assertEqual(set1['name'], "Adam")
        self.assertEqual(set1['surname'], "NOWAK")
        self.assertEqual(set1['age'], 34)

        self.assertEqual(set2['name'], "Maja")
        self.assertEqual(set2['surname'], "BEE")
        self.assertEqual(set2['age'], 12)


class TestDataSetCollectorScenarioTypeB(TestCase):
    """
        Consider the following scenario:
        Data (name, surname and age) is stored each in separate files.
        Those files are collected into a catalogues with data sets - each catalogue represents
        different data set.
    """
    @staticmethod
    def read_file(filepath: str):
        """ simple helper function for 1-line reading file content """
        with open(filepath, 'r') as file:
            return file.read()

    def test_type_b(self):

        # we have 3 pieces of data: name, surname and age
        # Lets define data descriptors:
        # Each is stored inside separate file, so the obtaining algorithm should only get a path to the directory with
        # data set and read proper file from there.
        # We additionally want treat the age as integer number increased by 2000 - for some statistics or something.
        descriptors = [
            DataDescriptor(name="name",
                           data_retrieving_functor=lambda directory: self.read_file(directory + "/name.txt")),

            DataDescriptor(name="surname",
                           data_retrieving_functor=lambda directory: self.read_file(directory + "/surname.txt")),

            DataDescriptor(name="age",
                           data_retrieving_functor=lambda directory: self.read_file(directory + "/age.txt"),
                           data_transformation_functor=lambda age: int(age) + 2000),
        ]

        # algorithm for feeding the data descriptors should produce a path to the directory where the data set
        # is stored. This could be done via some disk searching or something, but here we only pass down
        # given parameter - for this test we will be giving directory path by hand:
        def just_pass_arg_down(arg): return arg

        # create data set collector:
        collector = DataSetCollector(data_descriptors_feeder=just_pass_arg_down,
                                     data_descriptors=descriptors)

        # base path for our data sets:
        base_path = "test/data/typeB/"

        # obtain data from set1:
        set1 = collector.data(base_path + "set1")

        # obtain data from set2:
        set2 = collector.data(base_path + "set2")

        # check correctness of data:
        self.assertEqual(set1['name'], "Adam")
        self.assertEqual(set1['surname'], "Nowak")
        self.assertEqual(set1['age'], 2034)

        self.assertEqual(set2['name'], "Maja")
        self.assertEqual(set2['surname'], "Bee")
        self.assertEqual(set2['age'], 2012)


class TestDataSetCollectorBothScenariosWithHelperFunction(TestCase):
    """ more or less this class is the real-world usage """

    @staticmethod
    def read_file(filepath: str):
        """ simple helper function for 1-line reading file content """
        with open(filepath, 'r') as file:
            return file.read()

    @staticmethod
    def get_data_from_line_starting_with(filecontent: str, what: str):
        """ simple function which looks for line with requested differentiator """

        for line in filecontent.split("\n"):
            if line.startswith(what):
                return line.split(":")[1][1:]
        raise ValueError("Cannot find" + what + " in file")

    def test_with_helper_function(self):
        # define 2 scenarios of getting the same data which is stored in a different way:
        type_a_data = get_data_sets_based_on_string_list(
            string_list=["test/data/typeA/set1", "test/data/typeA/set2"],
            data_descriptors_feeder=lambda dirpath: self.read_file(dirpath + "/data.txt"),
            data_descriptors=[
                DataDescriptor(name="name",
                               data_retrieving_functor=lambda file_content: self.get_data_from_line_starting_with(file_content, "name:")),
                DataDescriptor(name="surname",
                               data_retrieving_functor=lambda file_content: self.get_data_from_line_starting_with(file_content, "surname:")),
                DataDescriptor(name="age",
                               data_retrieving_functor=lambda file_content: self.get_data_from_line_starting_with(file_content, "age:")),
            ])

        type_b_data = get_data_sets_based_on_string_list(
            string_list=["test/data/typeB/set1", "test/data/typeB/set2"],
            data_descriptors_feeder=lambda arg: arg,
            data_descriptors=[
                DataDescriptor(name="name",
                               data_retrieving_functor=lambda directory: self.read_file(directory + "/name.txt")),
                DataDescriptor(name="surname",
                               data_retrieving_functor=lambda directory: self.read_file(directory + "/surname.txt")),
                DataDescriptor(name="age",
                               data_retrieving_functor=lambda directory: self.read_file(directory + "/age.txt"))
            ])

        self.assertEqual(type_a_data, type_b_data)

        self.assertEqual(type_a_data[0]['name'], "Adam")
        self.assertEqual(type_a_data[0]['surname'], "Nowak")
        self.assertEqual(type_a_data[0]['age'], "34")

        self.assertEqual(type_b_data[1]['name'], "Maja")
        self.assertEqual(type_b_data[1]['surname'], "Bee")
        self.assertEqual(type_b_data[1]['age'], "12")


class TestDataSetCollectorSynthetic(TestCase):
    def test_synthetic(self):
        data_desc = [
            DataDescriptor("a", lambda s: str(s.count("a"))),
            DataDescriptor("b", lambda s: str(s.count("b"))),
            DataDescriptor("c", lambda s: str(s.count("c"))),
            DataDescriptor("d", lambda s: str(s.count("d"))),
        ]
        collector = DataSetCollector(lambda s: s, data_desc)

        data = collector.data_list("abcdefgh")
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], "1")
        self.assertEqual(data[1], "1")
        self.assertEqual(data[2], "1")
        self.assertEqual(data[3], "1")

        data = collector.data_list("beef")
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], "0")
        self.assertEqual(data[1], "1")
        self.assertEqual(data[2], "0")
        self.assertEqual(data[3], "0")

        data = collector.data_list("abba")
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], "2")
        self.assertEqual(data[1], "2")
        self.assertEqual(data[2], "0")
        self.assertEqual(data[3], "0")

        data = collector.data("abcdefgh")
        self.assertEqual(len(data), 4)
        self.assertEqual(data['a'], "1")
        self.assertEqual(data['b'], "1")
        self.assertEqual(data['c'], "1")
        self.assertEqual(data['d'], "1")

        data = collector.data("beef")
        self.assertEqual(len(data), 4)
        self.assertEqual(data['a'], "0")
        self.assertEqual(data['b'], "1")
        self.assertEqual(data['c'], "0")
        self.assertEqual(data['d'], "0")

        data = collector.data("abba")
        self.assertEqual(len(data), 4)
        self.assertEqual(data['a'], "2")
        self.assertEqual(data['b'], "2")
        self.assertEqual(data['c'], "0")
        self.assertEqual(data['d'], "0")

