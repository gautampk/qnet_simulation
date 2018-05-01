import qutip as q
import numpy as np
from math import sqrt
from qnets.qnet import qnet
from qnets.utils import proj

def main():
    qubits = ['A', 'B1', 'B2', 'C']
    nodes = {
        'A': ['A'],
        'B': ['B1', 'B2'],
        'C': ['C']
    }
    state = proj(q.tensor(
        1/sqrt(2) * (q.qubit_states(2, [0, 0]) + q.qubit_states(2, [1, 1])),
        1/sqrt(2) * (q.qubit_states(2, [0, 0]) + q.qubit_states(2, [1, 1]))
    ))
    network = qnet(qubits, nodes, state)

    print(network.edges)

if __name__ == '__main__':
    main()