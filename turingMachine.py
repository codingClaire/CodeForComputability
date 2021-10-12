import numpy as np
from graphviz import Digraph

class turingMachine:
    def __init__(self, states, start_state, end_states, file_name):
        self.states = states
        self.states_num = len(states)
        self.start_state = start_state
        self.end_states = end_states
        self.next_state = np.zeros(
            (self.states_num, self.states_num), dtype=int)
        self.next_act = np.zeros((self.states_num, self.states_num), dtype=int)
        self.file_name=file_name
        self.get_machine_quadruples()

    def get_machine_quadruples(self):
        f = open(self.file_name, "r", encoding='utf-8')
        self.linedata = f.readlines() # 图灵机四元组
        act2num = {"L": 0, "R": 1, "0": 2, "1": 3}  # 四种操作
        for line in self.linedata:
            line_data = line.split(" ")
            from_state, scan_symbol, act, to_state = int(line_data[0]), int(
                line_data[1]), line_data[2], int(line_data[3])
            self.next_state[from_state][scan_symbol] = to_state
            self.next_act[from_state][scan_symbol] = act2num[act]
    
    def get_machine_picture(self):
        save_name=self.file_name.split(".")[0]
        print(save_name)
        tm_graph = Digraph("G",format="png")
        for state in self.states:
            if state in self.end_states:
                tm_graph.node(str(state),label=str(state),shape="doublecircle")
            else:
                tm_graph.node(str(state), label=str(state))
        for line in self.linedata:
            line_data = line.split(" ")
            tm_graph.edge(str(line_data[0]),str(line_data[3]),label=str(line_data[1])+":"+str(line_data[2]))
        tm_graph.render(save_name, view=False)


    def scan_tape(self, stop_step,tape,current_index=0):
        current_state = self.start_state
        input_conf = tape[0:current_index+1] + \
            "-["+str(current_state)+"]-"+tape[current_index+1:]
        print(input_conf)
        n = 0
        while(current_state not in self.end_states and n < stop_step):
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
    
    def test_tm(self):
        print("==Test for ",self.__class__.__name__, "==")
        while(1):
            tape = input("input the current tape(input exit to exit):")
            if tape=='exit':
                break
            current_index=input("input the current index of the scanning head:")
            stop_step=input("input the largest time to act(in case no halt):")
            self.scan_tape(int(stop_step),str(tape),int(current_index))


class minValueTuringMachine(turingMachine):
    def __init__(self):
        states=[i for i in range(1, 32)]
        end_states=[26, 25, 20, 16, 28, 31]
        start_state=1
        file_name="min_fa.txt"
        super(minValueTuringMachine,self).__init__(states,start_state,end_states,file_name)

class blankNoHaltTuringMachine(turingMachine):
    def __init__(self):
        states = [i for i in range(1, 26)]
        end_states = [18,23,25]
        start_state = 1
        file_name="1halt_fa.txt"
        super(blankNoHaltTuringMachine,self).__init__(states,start_state,end_states,file_name)

if __name__ == '__main__':
    tm1=minValueTuringMachine()
    tm1.get_machine_picture()
    tm1.test_tm()

    tm2 = blankNoHaltTuringMachine()
    tm2.get_machine_picture()
    tm2.test_tm()
