from .qubit import qubit
from .utils import measure, proj
import qutip as q
import numpy as np
import math

class node:
    def __init__(self, qubits):
        self.qubits = qubits

    def __getattr__(self, attr):
        if attr in self.qubits.keys():
            return(self.qubits[attr])

    def Bell(self, a, b):
        # Make a Bell basis measurement on the two qubits specified.
        results = [
            proj(1/math.sqrt(2) * (q.tensor(q.basis(2, 0), q.basis(2, 0)) + q.tensor(q.basis(2, 1), q.basis(2, 1)))),
            proj(1/math.sqrt(2) * (q.tensor(q.basis(2, 0), q.basis(2, 0)) - q.tensor(q.basis(2, 1), q.basis(2, 1)))),
            proj(1/math.sqrt(2) * (q.tensor(q.basis(2, 0), q.basis(2, 1)) + q.tensor(q.basis(2, 1), q.basis(2, 0)))),
            proj(1/math.sqrt(2) * (q.tensor(q.basis(2, 0), q.basis(2, 1)) - q.tensor(q.basis(2, 1), q.basis(2, 0))))
        ]
        state = q.tensor(self.qubits[a].state, self.qubits[b].state)
        output = measure(state, results)

        self.qubits[a] = qubit(output.ptrace(0))
        self.qubits[b] = qubit(output.ptrace(1))
    
    def X(self, a):
        # Make a |±> basis measurement on the qubit specified.
        results = [
            qubit(1/math.sqrt(2), 1/math.sqrt(2)).state,
            qubit(1/math.sqrt(2), -1/math.sqrt(2)).state
        ]

        self.qubits[a] = qubit(measure(self.qubits[a].state, results))