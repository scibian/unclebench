##############################################################################
#  This file is part of the UncleBench benchmarking tool.                    #
#        Copyright (C) 2019 EDF SA                                           #
#                                                                            #
#  UncleBench is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  UncleBench is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with UncleBench. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                            #
##############################################################################
""" Define BenchmarkManager abstract class """


import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BenchmarkManager():
    """  Abtract class that defines the interface to manage a benchmark.
    """


    @abc.abstractmethod
    def __init__(self, benchmark_names, platform_name):
        """ Class constructor

        Args:
            benchmark_name (string): name of the benchmark
            platform_name (string): name fo the platform
            uconf (UbenchConfig): ubench configuration
        """


    @abc.abstractmethod
    def run(self):  # pylint: disable=dangerous-default-value
        """ Run benchmark on a given platform and write a ubench.log file in
        the benchmark run directory.

        Args:
            platform (string):  name of the platform used to retrieve parameters
                      needed to run the benchmark.
            opt_dict (dictionnary): with the options invoked at the command line
        """


    @abc.abstractmethod
    def list_parameters(self, default_values):
        """ List parameters on standard output.

        Args:
            default_values (bool): if true, tries to interpret parameters.
        """


    # # # # #      Analyze part      # # # # #
     # # # #                          # # # #
      # # #                            # # #
       # #                              # #
        #                                #


    @abc.abstractmethod
    def print_log(self, idb=-1):
        """ Print log from a benchmark run

        Args:
            idb: (int) id of the benchmark
        """


    @abc.abstractmethod
    def list_runs(self):
        """ List benchmark runs with their IDs and status """

    @abc.abstractmethod
    def result(self, benchmark_id):
        """ Generate and print results """

    def print_result_array(self, output_file=None):
        """ Asciidoc printing result array

        Args:
            output_file (string): path of a file where to write the array.
                                  If not set the array is printed to stdout.
            debug_mode (boolean):
        """


    @abc.abstractmethod
    def print_transposed_result_array(self, output_file=None):
        """ Asciidoc printing of transposed result array

        Args:
            output_file (string): path of a file where to write the array.
                                  If not set the array is printed to stdout.
        """
