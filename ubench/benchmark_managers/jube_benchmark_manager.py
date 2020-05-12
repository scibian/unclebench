# -*- coding: utf-8 -*-
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
""" Define JubeBenchmarkManager class. """


import ubench.benchmarking_tools_interfaces.jube_benchmarking_api as jba
import ubench.benchmark_managers.standard_benchmark_manager as stdbm


class JubeBenchmarkManager(stdbm.StandardBenchmarkManager):
    """ Concrete class defining an interface to run jube benchmarks and
    manage their results.
    """

    def __init__(self, benchmark, platform):
        """ Class constructor """
        super(JubeBenchmarkManager, self).__init__(benchmark, platform)


    def get_benchmarking_api(self):
        """ Factory method to get a new JubeBenchmarkingAPI """

        return jba.JubeBenchmarkingAPI(self.benchmark, self.platform)
