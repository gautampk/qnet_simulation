# Python modules
import itertools

# Third party modules
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt 

# My modules
from .utils import entangled

class qnet:
    def __init__(self, qubits, nodes, state):
        try:
            # Verify that the state is the correct dimension.
            assert len(state.dims[0]) == len(qubits)

            # Verify that the substates are all qubit substates.
            assert np.all(np.array(state.dims[0]) == 2)
            assert np.all(np.array(state.dims[1]) == 2)

            # Verify that the nodes contain only qubits that are listed.
            nodesPerQubit = {qubit: 0 for qubit in qubits}
            for node in nodes:
                for qubit in nodes[node]:
                    assert qubit in qubits
                    nodesPerQubit[qubit] = nodesPerQubit[qubit] + 1

            # Verify that every qubit is in exactly one node.
            assert np.all(np.array(list(nodesPerQubit.values())) == 1)
        except AssertionError as e:
            raise e from None
        else:
            self.qubits = qubits
            self.nodes = nodes
            self.state = state

    def nodeOf(self, a):
        for node in self.nodes:
            if a in self.nodes[node]:
                return node

    def draw(self):
        nx.draw(self._graph(), with_labels=True, font_weight='bold')
        plt.show()

    def swap(self, a, b, c):
        # Get a pair of qubits bridging a & b and b & c
        for pair in self._getEntangled():
            if self.nodeOf(pair[0]) == a and self.nodeOf(pair[1]) == b:
                aTOb = pair
            elif self.nodeOf(pair[0]) == b and self.nodeOf(pair[1]) == c:
                bTOc = pair

        try:
            assert aTOb
            assert bTOc
        except Exception:
            raise self.NetworkOperationError('No valid path found.') from None

    def _graph(self):
        # Create graph object.
        graph = nx.Graph()

        # Add nodes with list of qubits as an attribute.
        for node in self.nodes:
            graph.add_node(node, qubits=self.nodes[node])

        # Generate edges.
        graph.add_edges_from([
            (self.nodeOf(pair[0]), self.nodeOf(pair[1]))
            for pair in self._getEntangled()
        ])

        # Return.
        return graph

    def _getEntangled(self):
        # Find those qubits which are entagled using the Peres-Horodecki
        #   criterion.
        entagledPairs = [
            (a, b)
            for a, b in itertools.product(self.qubits, self.qubits)
            if entangled(
                self.state.ptrace([
                    self.qubits.index(a),
                    self.qubits.index(b)
                ])
            )
        ]

        # Return.
        return entagledPairs

    def __getattr__(self, attr):
        if attr == 'graph':
            return self._graph()
        elif attr == 'edges':
            return list(self._graph().edges)
        elif attr == 'order':
            return len(self._graph().nodes)
        elif attr == 'size':
            return len(self._graph().edges)
        else:
            raise AttributeError('No such attribute.')

    class NetworkOperationError(Exception):
        pass