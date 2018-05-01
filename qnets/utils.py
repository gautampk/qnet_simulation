import qutip as q
import numpy as np

def measure(state, results):
    probs = np.array([
        np.real((state * result.dag() * result).tr())
        for result in results
    ])
    probs = probs / probs.sum()
    result = np.random.choice(np.arange(len(probs)), p=probs)

    return((results[result] * state * results[result].dag()) / probs[result])

def proj(state):
    return(state * state.dag())

def entangled(state):
    if state.shape == (4, 4):
        return(np.any(q.partial_transpose(state, [1, 0]).eigenenergies() < 0))
    else:
        raise TypeError('The Peres-Horodecki criterion only works for pairs of qubits.')