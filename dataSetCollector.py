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

from typing import Callable, List, Any
from dataDescriptor import DataDescriptor


class DataSetCollector:
    """
        An abstraction describing a data set from a common source.

        Workflow with this class should looks as follow:

        [1] Creation: prepare list of DataDescriptors and an algorithm - data descriptors feeder - which will be
        producing arguments for obtaining the data from the DataDescriptors.
        [2] Reaching set of data: call the data() member, passing to it arguments for data descriptors feeder algorithm,
            if any is necessary. The DataSetCollector object is then:

            [2a] obtaining the arguments for data descriptors by calling the data descriptor feeder algorithm and passing
             to it any arguments provided to the data() member function,
            [2b] for all data descriptors - calling their data obtaining algorithm with arguments from [2a],
            [2c] returning a dictionary of obtained data, where the keys are the names of the data descriptors.


        Keep in mind that every DataDescriptor will get the same set of arguments for a single data set, so this have
        to be considered when constructing data-obtaining-algorithms for all of the DataDescriptors.

        For example, when obtaining collection of data from a database, algorithms for DataDescriptors should take
        as a parameter common base for all data - some database connection object to work with, maybe with some more
        details for making the query, so the data descriptors feeder should return such object(s).

        Another example - when obtaining collection of data, stored as a content of some files inside some directory,
        algorithms for DataDescriptors should take as a parameter a path to the directory where all the files are stored,
        so the data descriptors feeder should return that path.
    """
    def __init__(self,
                 data_descriptors_feeder: Callable[..., Any],
                 data_descriptors: List[DataDescriptor]):
        self.data_descriptors = data_descriptors
        self.data_descriptors_feeder = data_descriptors_feeder

    def data(self, *data_descriptors_feeder_args):
        data_descriptors_args = self.data_descriptors_feeder(*data_descriptors_feeder_args)
        name_data_tuples = [
            (data_descriptor.name, data_descriptor.data(data_descriptors_args))
            for data_descriptor in self.data_descriptors
        ]
        return dict(name_data_tuples)

    def data_list(self, *data_descriptors_feeder_args):
        data_descriptors_args = self.data_descriptors_feeder(*data_descriptors_feeder_args)
        return [data_descriptor.data(data_descriptors_args) for data_descriptor in self.data_descriptors]


def get_data_sets_based_on_string_list(string_list: List[str],
                                       data_descriptors_feeder: Callable[..., Any],
                                       data_descriptors: List[DataDescriptor]):

    collector = DataSetCollector(data_descriptors_feeder=data_descriptors_feeder,
                                 data_descriptors=data_descriptors)

    return [collector.data(data_location) for data_location in string_list]