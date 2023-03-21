import argparse
import datetime
import math
import os

import numpy as np
import pandas as pd

from fort14parse import Fort14Parser

FT_TO_M = 0.3048

def cfs_to_adcirc(flow, factor):
    """Converts flow in ft^3/s to ADCIRC-compatible m^2/s"""

    flow *= pow(FT_TO_M, 3)
    #flow *= 0.28316847 # CFS to m^3/s
    flow *= factor # m^3/s to ADCIRC m^2/s
    return flow


class Fort20Writer:
    """Writes fort.20 flow boundary condition files for ADCIRC

    Works for short nodestrings with similar distances between nodes

    Attributes:
        fort14: Fort14Parser object or string path to the ADCIRC mesh file
        fort20: string path to save new flow BC file to
        interval: time (in s) between when ADCIRC model reads the fort.20
        input_dir: string path to flow input data
        use_depth: choose whether to use the node depth to give the boundary
            nodes slightly different amounts of flow. alternatively, distribute
            flow evenly across the boundary
        const_flow: total flow through the boundary, in CFS. Note that positive
            values correspond to flow INTO the mesh, and negative values
            correspond to flow OUT OF the mesh
        start: datetime object specifying when the simulation begins
        rnday: number of days to include in the fort.20

    """

    def __init__(self, fort14, fort20, interval=None, input_dir=None,
                 use_depth=False, const_flow=None, start=None, rnday=None):
        """Inits Fort20Writer with ___"""

        # Warn if time increment should be specified and is not
        if not const_flow and not interval:
            self.interval = 900
            import warnings
            warnings.warn('Time increment not specified,',
                          'using defaulf of 900 sec')
        else:
            self.interval = interval

        # Create Fort14Parser object
        if type(fort14) == str:
            self.fort14 = Fort14Parser(fort14)
        elif isinstance(fort14, Fort14Parser):
            self.fort14 = fort14
        else:
            raise Exception('fort.14 must be specified as str or Fort14Parser')
        self.fort20     = fort20
        self.input_dir  = input_dir
        self.use_depth  = use_depth
        self.const_flow = const_flow

        self.make_times_list(start, rnday)

        # associate input filenames with BCs
        if not self.const_flow:
            self.infiles = sorted(os.listdir(self.input_dir))

            self.flows_cfs = {}
            for infile in self.infiles:
                self.flows_cfs[infile] = self.extract_flow_cfs(infile)


    def make_times_list(self, start, rnday):
        """Creates datetime object for each time at which the fort.20 will be sampled"""
        if self.const_flow:
            self.times = [0, 1]
        else:
            self.times = [start]
            rnsec = rnday * 24 * 60 * 60
            num_times = math.ceil(rnsec/self.interval)
            time = start
            for _ in range(num_times):
                time += datetime.timedelta(seconds=self.interval)
                self.times.append(time)


    def extract_flow_cfs(self, infile):
        """Constructs a dictionary of the flow values at all considered times"""
        print('Extracting flow from ' + infile)
        flows = {}
        with open(self.input_dir + '/' + infile, 'r') as f:
            next(f)
            for line in f:
                t, flow = line.rstrip().split(',')
                time = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                if time in self.times:
                    flows[time] = float(flow)
        return flows


    def calculate_flow_factors(self):
        """Calculates the conversion factor between m^3/s and the m^2/s inputs
        in the fort.20. Units of factors are 1/m.
        """

        # calculate factors to translate from outflow data to ADCIRC
        self.flow_bcs = self.fort14.get_bcs(bctype=22)
        if self.const_flow:
            self.infiles = [None for bc in self.flow_bcs]
        for bc in self.flow_bcs:
            factors = []
            dist_between_nodes = bc.avg_dist_between_nodes()
            if self.use_depth:
                depths = bc.get_depths() # TODO write this
                for depth in depths:
                    factors.append(depth / (dist_between_nodes * sum(depths)))
            else:
                # share equally on the inner nodes, while the outer nodes
                # get 1/2 of that
                # Namo: no need for 1/2 factor if assume river has flat bottom
                factors = [1 / (dist_between_nodes * (bc.num_nodes - 1))
                           for n in range(bc.num_nodes)]
                # factors[ 0] /= 2
                # factors[-1] /= 2

            bc.set_factors(factors)


    def write(self):
        """Convert the input data to CFS and write the fort.20"""

        with open(self.fort20, 'w') as o:
            o.write(str(self.interval) + '\n')
            for time in self.times:
                for bc, infile in zip(self.flow_bcs, self.infiles):
                    for factor in bc.factors:
                        # add something to NOT convert from CFS later on,
                        # in case of different input units
                        #TODO fix this for const
                        if self.const_flow:
                            flow_cfs = self.const_flow
                        else:
                            flow_cfs = self.flows_cfs[infile][time]

                        flow = cfs_to_adcirc(flow_cfs, factor)
                        o.write(str(flow) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Write fort.20 file')
    parser.add_argument('-f',  '--fort14',    dest='fort14',
                        type=str,            default='fort.14')
    parser.add_argument('-o',  '--output',    dest='fort20',
                        type=str,            default='fort.20')
    parser.add_argument('-i',  '--inputdir',  dest='input_dir',
                        type=str,            default=None)
    parser.add_argument('-dt', '--interval',  dest='interval',
                        type=int,            default=10000000000,
                        help=('Time interval (in s) at which ADCIRC '
                              'should read new fort.20 lines'))
    parser.add_argument('-t',  '--starttime', dest='starttime',
                        type=str,            default='2008-09-05-12:00')
    parser.add_argument('-d',  '--rnday',     dest='rnday',
                        type=float,          default=10)
    parser.add_argument('-c',  '--const',     dest='const_flow',
                        type=float,          default=None,
                        help=('For the simplest case, specify a constant '
                              'flow at all BCs, in CFS'))
    parser.add_argument(       '--use_depth', dest='use_depth',
                        action='store_true', default=False,
                        help=('Flow can be calculated more accurately at each '
                              'node if the water depth is taken into account.'))

    args = parser.parse_args()

    starttime = datetime.datetime.strptime(args.starttime, '%Y-%m-%d-%H:%M')
    writer = Fort20Writer(args.fort14, args.fort20, interval=args.interval,
                          input_dir=args.input_dir, use_depth=args.use_depth,
                          const_flow=args.const_flow, start=starttime,
                          rnday=args.rnday)
    writer.calculate_flow_factors()
    writer.write()
