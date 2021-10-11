import numpy as np

states = [i for i in range(1, 24)]

states_num = len(states)
end_states = [18,23]
start_state = 1
act2num = {"L": 0, "R": 1, "0": 2, "1": 3}  # 四种操作
num2act = {0: "L", 1: "R", 2: "0", 3: "1"}

next_state = np.zeros((states_num, states_num), dtype=int)
next_act = np.zeros((states_num, states_num), dtype=int)

f = open("./finite_automaton2.txt", "r", encoding='utf-8')
data = f.readlines()
for line in data:
    line_data = line.split(" ")
    from_state, scan_symbol, act, to_state = int(line_data[0]), int(
        line_data[1]), line_data[2], int(line_data[3])
    next_state[from_state][scan_symbol] = to_state
    next_act[from_state][scan_symbol] = act2num[act]
current_state = start_state
current_index = 7
tape = "001000001"
if(current_index>=len(tape)):
    for i in range(0,current_index-len(tape)+1):
        tape+="0"
input_conf = tape[0:current_index+1] + \
    "-["+str(current_state)+"]-"+tape[current_index+1:]
print(input_conf)
n = 0
while(current_state not in end_states and n < 100):
    n += 1
    print("step: ", n)
    scan_symbol = int(tape[current_index])
    act = next_act[current_state][scan_symbol]
    if act == 0:  # "L"
        if(current_index-1 < 0):
            tape = "0"+tape
        else:
            current_index -= 1
    elif act == 1:  # "R"
        if(current_index+1 >= len(tape)):
            tape = tape+"0"
        current_index += 1
    elif act == 2:  # "0"
        tape_list = list(tape)
        tape_list[current_index] = '0'
        tape = ''.join(tape_list)
    else:  # "1"
        tape_list = list(tape)
        tape_list[current_index] = '1'
        tape = ''.join(tape_list)
    current_state = next_state[current_state][scan_symbol]
    current_conf = tape[0:current_index+1] + \
        "-["+str(current_state)+"]-"+tape[current_index+1:]
    print(current_conf)
