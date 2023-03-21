
from .adcutils import Node, BoundaryCondition


class Fort14Parser:
    """

    """

    def __init__(self, filename):
        """Inits Fort14 with a path to the file"""

        self.filename = filename
        self.parse()


    def parse(self):
        """Parses the fort.14, extracting the node and BC data"""

        with open(self.filename, 'r') as f:
            self.mesh_name = f.readline().rstrip()
            self.total_elements, self.total_nodes = [int(x) for x in f.readline().rstrip().split()]
            self.nodes = {}
            for i in range(1, self.total_nodes+1):
                index, lon, lat, depth = [float(x) for x in f.readline().rstrip().split()]
                self.nodes[i] = Node(i, lon, lat, depth)
            for i in range(1, self.total_elements+1):
                # connectivity section
                next(f)

            # Boundary conditions

            # Open boundaries
            self.num_open_bounds = int(f.readline().rstrip().split()[0])
            self.total_open_bound_nodes = int(f.readline().rstrip().split()[0])
            self.open_bounds = {}
            for i in range(1, self.num_open_bounds+1):
                line = f.readline().rstrip().split()
                num_nodes = int(line[0])
                bctype = 'open'
                bc_nodes = []
                for j in range(num_nodes):
                    bc_node_num = int(f.readline().rstrip())
                    bc_nodes.append(self.nodes[bc_node_num])
                self.open_bounds[i] = BoundaryCondition('open', num_nodes, bctype, bc_nodes)

            # Land boundaries
            self.num_land_bounds = int(f.readline().rstrip().split()[0])
            self.total_land_bound_nodes = int(f.readline().rstrip().split()[0])
            self.land_bounds = {}
            for i in range(1, self.num_land_bounds+1):
                line = f.readline().rstrip().split()
                num_nodes, bctype = [int(x) for x in line[:2]]
                bc_nodes = []
                for j in range(num_nodes):
                    bc_node_num = int(f.readline().rstrip().split()[0])
                    bc_nodes.append(self.nodes[bc_node_num])
                self.land_bounds[i] = BoundaryCondition('land', num_nodes, bctype, bc_nodes)

        # Concatenate bounds
        if self.open_bounds:
            self.all_bounds = dict(self.open_bounds)
            if self.land_bounds:
                self.all_bounds.update(self.land_bounds)
            else:
                self.all_bounds = {}
        elif self.land_bounds:
            self.all_bounds = self.land_bounds
        else:
            self.all_bounds = {}

    def get_bcs(self, bctype=None):
        if bctype:
            bclist = []
            for bc in self.all_bounds.values():
                if bc.bctype == bctype:
                    bclist.append(bc)
            return bclist
        else:
            return list(self.all_bounds.values())
