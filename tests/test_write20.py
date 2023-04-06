import numpy as np
from write_fort20.fort14parse import Fort14Parser
from write_fort20.fort20write import Fort20Writer
import os
import datetime
import pytest

# Write to 30m_cut_v8.20 file
@pytest.fixture(scope=module)
def create_fort20():
    command = "python ../write_fort20/fort20write.py " \
        "-f 30m_cut_v8.14 " \
        "-o 30m_cut_v8.20 " \
        "-i gauges_namo " \
        "-dt 3600 " \
        "-t \'2008-09-05-12:00\' " \
        "-d 9"
    os.system(command)

def create_const_fort20():
    command = "python ../write_fort20/fort20write.py " \
        "-f const.14 " \
        "-o const.20 " \
        "-dt 900 " \
        "-t \'2008-09-05-12:00\' " \
        "--const 5 " \
        "-d 5"
    os.system(command)

# Extract the first river from gauge file
#@pytest.fixture(scope="module")
def read_gauge():
    starttime = datetime.datetime.strptime('2008-09-05-12:00', '%Y-%m-%d-%H:%M')
    rivers = Fort20Writer("./30m_cut_v8.14", " ", interval=3600, input_dir="./gauges_namo",
                          start=starttime, rnday=9, num_rivers=45)
    # First river
    river = rivers.flows_cfs[rivers.infiles[0]]
    flow = []
    flow = [river[time] for time in rivers.times]
    print("Finished reading gauge data")
    return flow

# Return an array containing the total discharge time series of a river
#@pytest.fixture(scope="module")
def read_fort20(fort14, fort20):
    fort14 = Fort14Parser(fort14)
    # Get a list of flow boundary objects
    bcs = fort14.get_bcs(22)
    total_num_nodes = sum([bc.num_nodes for bc in bcs])

# Check only first river for now
    my_river = bcs[0]
    num_nodes = my_river.num_nodes
    my_total_length = my_river.avg_dist_between_nodes() * (num_nodes-1)
    print("total length = %.3f m" % my_total_length)

# Read in the fort.20 file
    discharge = []
    with open(fort20) as f20:
        l = f20.readline() # dt label
        while True:
            # first node
            l = f20.readline().strip()
            if not l:
                break
            flux = float(l)
            # Convert from CMS to CFS
            discharge.append(flux * my_total_length / (0.3048**3))

            for i in range(num_nodes-1):
                l = f20.readline().strip()
                #flux += float(l)

        # Total discharge in m^3/s

            # skip the other rivers
            for i in range(total_num_nodes - num_nodes):
                l = f20.readline()

    print("Finished reading fort.20")
    return discharge

@pytest.mark.skip()
def test_length():
    #discharge = read_fort20()
    #flow = read_gauge()
    assert len(read_fort20) == len(read_gauge)

@pytest.mark.skip()
def test_flow(read_fort20, read_gauge):
    np.testing.assert_almost_equal(read_fort20, read_gauge)

def test_const_flow(create_const_fort20):
    discharge = 5.
    fort20 = read_fort20('const.14', 'const.20')
    assert(np.allclose(fort20, discharge))
