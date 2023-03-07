from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Parameter
from qiskit.quantum_info import Statevector
import numpy as np
import pickle
import os
import shutil
from scipy.optimize import minimize

from utils.TwoQubitUnitary import TwoQubitUnitary
from utils.Hamiltonian import makeObservable, returnStringObservable