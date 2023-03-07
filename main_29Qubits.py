from utils.import_list import *

#kindly change for different runs
manualAttemptNum = 0
repeat_depth = 1

connectivity = [[0, 1], [6, 7], [2, 8], [3, 11], [4, 14], [5, 17], [12, 13], [19, 20], [26, 27], 
                [0, 2], [1, 7], [3, 12], [4, 15], [5, 18], [6, 20], [9, 10], [16, 17], [23, 24],
                [0, 3], [1, 2], [4, 16], [5, 19], [6, 21], [7, 23], [10, 11], [17, 18], [24, 25],
                [0, 4], [2, 3], [5, 20], [6, 22], [7, 24], [1, 26], [13, 14], [27, 28],
                [0, 5], [3, 4], [6, 23], [7, 25], [1, 27], [2, 9], [14, 15], [21, 22], [28, 8],
                [0, 6], [4, 5], [7, 26], [1, 8], [2, 10], [3, 13], [11, 12], [18, 19],
                [0, 7], [5, 6], [1, 28], [2, 11], [3, 14], [4, 17], [15, 16], [8, 9], [20, 21], [22, 23], [25, 26]]
connectivity = list(map(tuple, connectivity))

num_qubits = 29
boundary_start = 8

boundaryFirst = range(1, boundary_start)
boundarySecond = range(boundary_start, num_qubits)


paramsList = list()
energyList = list()


if num_qubits == 15:
    folderOpen = "triangle"
    unique = 3
elif num_qubits == 8:
    folderOpen = "center_8"
    unique = 2
elif num_qubits == 29:
    folderOpen = "center_29"
    unique = 4

parameters = np.random.normal(0, 0.1, repeat_depth * unique * 15)

name_for_run = "repeat_depth_" + str(repeat_depth) + "_" + str(len(parameters)) + "_parameters_attempt_" + str(manualAttemptNum)

folderPath = "data/" + folderOpen + "/" + name_for_run
# Make directory for run
os.mkdir(folderPath)
#Make directory for run results
os.mkdir(folderPath + "/results")
#Make copy of code
shutil.copy("./main_29Qubits.py", folderPath)

num = 0
observable = makeObservable(boundary_start, num_qubits)

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
            if i in boundaryFirst and j in boundaryFirst:
                a = 0
            elif i in boundarySecond and j in boundarySecond:
                a = 1
            elif (i in boundaryFirst and j in boundarySecond) or (i in boundarySecond and j in boundaryFirst):
                a = 2
            else:
                a = 3
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
