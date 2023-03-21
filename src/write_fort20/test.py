from fort14parse import Fort14Parser
import numpy as np

#def fluxesToDischarge(

fort14 = Fort14Parser("30m_cut_v8.14")
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
with open("30m_cut_v8.20") as f20:
    l = f20.readline() # dt label
    while True:
        # first node
        l = f20.readline().strip()
        if not l:
            break
        flux = float(l)
        # Convert to CFS
        discharge.append(flux * my_total_length / (0.3048**3))

        for i in range(num_nodes-1):
            l = f20.readline().strip()
            #flux += float(l)

        # Total discharge in m^3/s

        # skip the other rivers
        for i in range(total_num_nodes - num_nodes):
            l = f20.readline()

    np.savetxt("test.20", discharge, fmt='%.5f')
