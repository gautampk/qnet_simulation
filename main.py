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
        q.bell_state(),
        q.bell_state()
    ))
    network = qnet(qubits, nodes, state)
    network.draw()
    
if __name__ == '__main__':
    main()