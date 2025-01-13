import simulator, grn
import numpy as np

simulator_output={'inputs': ['s', 'b', 'a'], 'outputs': ['o'], 'values': [[0], [0], [0], [1], [0], [1], [1], [1]]}
new_grn = grn.grn()
truth_table = []
products = []

for i in range(len(simulator_output['values'])):
    table_line = []
    values = (len(simulator_output['inputs'])-len(bin(i)[2:]))*'0' + bin(i)[2:] + str(simulator_output['values'][i])[1]
    for j in range(len(values)):
        table_line.append(int(values[j]))
    truth_table.append(table_line)

for input in simulator_output['inputs']:
    new_grn.add_input_species(input)

for output in simulator_output['outputs']:
    new_grn.add_species(output, 0.1)
    products.append({'name': output})

for i in range(len(truth_table)):
    regulators = []
    if truth_table[i][len(truth_table[i])-1]==1:
        for j in range(len(truth_table[i])-1): 
            regulators.append({'name': simulator_output['inputs'][j], 'type': (1 if truth_table[i][j]==1 else -1), 'Kd': 5, 'n': 2})
        new_grn.add_gene(10, regulators, products)
