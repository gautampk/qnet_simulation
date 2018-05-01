import qutip as q
import numpy as np

class qubit:
    def __init__(self, *args):
        if len(args) == 1 and type(args[0]) == type(q.Qobj()):
            if args[0].shape == (2, 2):
                self.a = args[0].matrix_element(q.basis(2, 0), q.basis(2, 0))
                self.b = args[0].matrix_element(q.basis(2, 0), q.basis(2, 1))
                self.c = args[0].matrix_element(q.basis(2, 1), q.basis(2, 0))
                self.d = args[0].matrix_element(q.basis(2, 1), q.basis(2, 1))
            else:
                raise TypeError("The Qobj must be a one-qubit density matrix.")
        elif len(args) == 2:
            self.a = args[0] * np.conj(args[0])
            self.b = args[0] * np.conj(args[1])
            self.c = args[1] * np.conj(args[0])
            self.d = args[1] * np.conj(args[1])
        elif len(args) == 4:
            self.a = args[0]
            self.b = args[1]
            self.c = args[2]
            self.d = args[3]
        else:
            raise TypeError("You must pass 2 or 4 floats or NumPy complex numbers, or a one-qubit density matrix.")

    def __getattr__(self, attr):
        if attr == 'state':
            return(
                self.a * q.basis(2, 0) * q.basis(2, 0).dag() + \
                self.b * q.basis(2, 0) * q.basis(2, 1).dag() + \
                self.c * q.basis(2, 1) * q.basis(2, 0).dag() + \
                self.d * q.basis(2, 1) * q.basis(2, 1).dag()
            )