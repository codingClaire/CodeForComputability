import numpy as np


class TuringMachine:
    def __init__(self, states, start_state, end_states, file_name,stop_step):
        self.states = states
        self.states_num = len(states)
        self.start_state = start_state
        self.end_states = end_states
        self.stop_step = stop_step  # 防止无法停机的最大步数
        self.next_state = np.zeros(
            (self.states_num, self.states_num), dtype=int)
        self.next_act = np.zeros((self.states_num, self.states_num), dtype=int)
        f = open(file_name, "r", encoding='utf-8')
        self.linedata = f.readlines() # 图灵机四元组
        self.get_machine_quadruples()

    def get_machine_quadruples(self):
        act2num = {"L": 0, "R": 1, "0": 2, "1": 3}  # 四种操作
        for line in self.linedata:
            line_data = line.split(" ")
            from_state, scan_symbol, act, to_state = int(line_data[0]), int(
                line_data[1]), line_data[2], int(line_data[3])
            self.next_state[from_state][scan_symbol] = to_state
            self.next_act[from_state][scan_symbol] = act2num[act]


    def scan_tape(self, tape):
        current_state = start_state
        current_index = 0
        input_conf = tape[0:current_index+1] + \
            "-["+str(current_state)+"]-"+tape[current_index+1:]
        print(input_conf)
        n = 0
        while(current_state not in end_states and n < self.stop_step):
            n += 1
            print("step: ", n)
            scan_symbol = int(tape[current_index])
            act =self.next_act[current_state][scan_symbol]
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
            current_state = self.next_state[current_state][scan_symbol]
            current_conf = tape[0:current_index+1] + \
                "-["+str(current_state)+"]-"+tape[current_index+1:]
            print(current_conf)
        if(current_state not in self.end_states):
            print("the stop number is too small to complete the caculation!")
            print("Please reset the stop number")

if __name__ == '__main__':
    states = [i for i in range(1, 32)]
    end_states = [26, 25, 20, 16, 28, 31]
    start_state = 1
    file_name = "./min_fa.txt"
    stop_step=500
    while(1):
        stop_step=input("input the largest time to act(in case no halt):")
        tape = input("input the current tape:")
        stop_step,tape=int(stop_step),str(tape)
        tm_for_min = TuringMachine(states, start_state,end_states,file_name,stop_step)
        tm_for_min.scan_tape(tape)