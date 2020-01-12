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

from typing import Callable, Any


class DataDescriptor:
    """
        An abstraction describing a single piece of data:
            - its name,
            - a way how to obtain the value,
            - an algorithm which should be applied in order to transform the data after obtaining it.

        Workflow with this class should looks as follow:

        [1] Creation: pass name and algorithms for obtaining and transforming data into the initializer parameters.
        [2] Reaching piece of the data: call the data() member, passing to it arguments for data obtaining algorithm,
            if any is necessary. The DataDescriptor object is then:

            [2a] calling the data obtaining algorithm, passing to it any arguments provided to the data() member function,
            [2b] calling the data transformation algorithm on the obtained data.
            [2c] returning the obtained data after the transformation.
    """
    def __init__(self,
                 name: str,
                 data_retrieving_functor: Callable[..., Any],
                 data_transformation_functor: Callable[[Any], Any] = lambda d: d):
        self.name = name
        self.data_retrieving_functor = data_retrieving_functor
        self.data_transformation_functor = data_transformation_functor

    def data(self, *args_for_data_retrieving_functor: ...) -> Any:
        retrieved_data = self.data_retrieving_functor(*args_for_data_retrieving_functor)
        return self.data_transformation_functor(retrieved_data)
