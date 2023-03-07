from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter
# from pennylane.operation import Operation
# import pennylane as qml
# from pennylane import numpy as np


class TwoQubitUnitary(QuantumCircuit):
    def __init__(self,):
        super().__init__()
        work = QuantumRegister(2, name='q')
        self.add_register(work)
        self.u(Parameter('p0'), Parameter('p1'), Parameter('p2'), work[0])
        self.u(Parameter('p3'), Parameter('p4'), Parameter('p5'), work[1])
        self.cx(work[1], work[0])
        self.rz(Parameter('p6'), work[0])
        self.ry(Parameter('p7'), work[1])
        self.cx(work[0], work[1])
        self.ry(Parameter('p8'), work[1])
        self.cx(work[1], work[0])
        self.u(Parameter('p9'), Parameter('p10'), Parameter('p11'), work[0])
        self.u(Parameter('p12'), Parameter('p13'), Parameter('p14'), work[1])

# class TwoQubitQML(Operation):
#     num_params = 1
#     num_wires = 2
#     par_method = "A"

#     grad_method = "A"

#     def __init__(self, params, wires):
#         super().__init__(params, wires=wires)

#     @staticmethod
#     def compute_decomposition(params, wires):
#         return [qml.U3(params[0], params[1], params[2], wires=wires[0]),
#         qml.U3(params[3], params[4], params[5], wires=wires[1]),
#         qml.CNOT(wires=[wires[1], wires[0]]),
#         qml.RZ(params[6], wires=wires[0]),
#         qml.RY(params[7], wires=wires[1]),
#         qml.CNOT(wires=[wires[0], wires[1]]),
#         qml.RY(params[8], wires=wires[1]),
#         qml.CNOT(wires=[wires[1], wires[0]]),
#         qml.U3(params[9], params[10], params[11], wires=wires[0]),
#         qml.U3(params[12], params[13], params[14], wires=wires[1])]