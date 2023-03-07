from qiskit.quantum_info import SparsePauliOp

def makeObservable(boundary_start, num_qubits):
    strX = ""
    size = num_qubits
    strX_list = list()
    for i in range(boundary_start, num_qubits):
        s = ['I'] * size
        s[i] = 'X'
        strX = "".join([str(j) for j in s])
        strX_list.append(strX)
    strZZ_list = list()
    
    boundary_size = num_qubits - boundary_start
    for i in range(boundary_size):
            temp = ['I'] * boundary_size
            temp[i%boundary_size] = 'Z'
            temp[(i+1)%boundary_size] = 'Z'
            strZZ = "".join([str(j) for j in ['I'] * boundary_start + temp])
            strZZ_list.append(strZZ)
    str_list = strZZ_list + strX_list
    params = list()
    for s in str_list:
        params.append((s[::-1], -1)) 
    operator_full = SparsePauliOp.from_list(params)
    operator_sparse = operator_full.to_matrix(True)
    return operator_sparse

def returnStringObservable(boundary_start, num_qubits):
    strX = ""
    size = num_qubits
    strX_list = list()
    for i in range(boundary_start, num_qubits):
        s = ['I'] * size
        s[i] = 'X'
        strX = "".join([str(j) for j in s])
        strX_list.append(strX)
    strZZ_list = list()
    
    boundary_size = num_qubits - boundary_start
    for i in range(boundary_size):
            temp = ['I'] * boundary_size
            temp[i%boundary_size] = 'Z'
            temp[(i+1)%boundary_size] = 'Z'
            strZZ = "".join([str(j) for j in ['I'] * boundary_start + temp])
            strZZ_list.append(strZZ)
    return strZZ_list + strX_list