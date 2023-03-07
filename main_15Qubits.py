from utils.import_list import *

#kindly change for different runs
manualAttemptNum = 0
repeat_depth = 4


connectivity = [[0,1],[7,8],[10,11],[13,14],[4,5],[2,12],[1,2],[8,9],[11,12],[14,3],[5,6],[0,4],[2,0],[9,10],[12,13],[3,4],[6,7],[1,8],[1,7],[2,11],[0,3],[1,9],[2,13],[0,5],[1,10],[2,14],[0,6],[1,11],[2,3],[0,7]]
boundary = [[3,4], [4,5], [5,6], [6,7], [7,8], [8,9], [9,10], [10,11], [11,12], [12,13], [13,14], [14,3]]

connectivity = list(map(tuple, connectivity))
boundary = list(map(tuple, boundary))

num_qubits = 15
boundary_start = 3

observable = makeObservable(boundary_start, num_qubits)

paramsList = list()
energyList = list()


if num_qubits == 15:
    folderOpen = "triangle"
    unique = 3
elif num_qubits == 8:
    folderOpen = "center"
    unique = 2

parameters = np.random.normal(0, 0.1, repeat_depth * unique * 15)

name_for_run = "repeat_depth_" + str(repeat_depth) + "_" + str(len(parameters)) + "_parameters_attempt_" + str(manualAttemptNum)

folderPath = "data/" + folderOpen + "/" + name_for_run
#Make directory for run
os.mkdir(folderPath)
#Make directory for run results
os.mkdir(folderPath + "/results")
#Make copy of code
shutil.copy("./main_15Qubits.py", folderPath)

num = 0

def cost_function(parameters):

    # Deducing nums of gates required from number of parameters
    num_gates = len(parameters)/15

    #using parameters to make unique gates
    gates = list()
    for i in range(int(num_gates)):
        gate = TwoQubitUnitary()
        gate = gate.bind_parameters({gate.parameters.data[index]: val for (index, val) in enumerate(parameters[i*15:(i*15)+15])})
        gates.append(gate)
    
    #define ansatz
    ansatz = QuantumCircuit(num_qubits)

    for depth in range(repeat_depth):
        for (index, (i, j)) in enumerate(connectivity[::pow(-1,depth)]):
            if (i, j) in boundary:
                a = 0
            elif i in range(boundary_start, num_qubits) or j in range(boundary_start, num_qubits):
                a = 1
            else:
                a = 2
            a = (unique * depth) + a
            ansatz.append(gates[a], [i, j])

    stv = Statevector.from_instruction(ansatz)
    right = observable.dot(stv)
    res  = stv.conjugate().data.dot(right)
    global num

    if num == 0:
        ansatz.draw(output="text", filename=folderPath + "/ansatz.txt")

    if num % 1000 == 0:   
        print(res, num)
        pickle.dump([res, parameters], open(folderPath + "/results/" + str(num) + ".pkl", "wb"))
    paramsList.append(parameters)
    energyList.append(res)
    num += 1
    
    return np.real(res)


result = minimize(cost_function, parameters)

pickle.dump([result, paramsList, energyList], open(folderPath + "/result_list.pkl", "wb"))
