import sys
alphabet = []
state_id = 0
gorder = 0
    #a system stack to store elements, use a list to implement the stack
class CStack:
    def __init__(self):
        self._elems = []
    def is_empty(self):
        return self._elems == []
    #to push a new element to the top of the stack,append it to the tail of the list
    def push(self, elem):
        global gorder
        elem.order = gorder
        gorder += 1
        self._elems.append(elem)
        #to pop the element in the top of the stack, remove it from the tail of the list
    def pop(self):
        if self._elems == []:
            raise Exception("stack underflow")
        return self._elems.pop()
    #access the element in the top of the stack
    def top(self):
        if self._elems == []:
            raise Exception("stack underflow")
        return self._elems[-1]
    def length(self):
        return len(self._elems)

class DFA:
    def __init__(self, states, alphabet, start_state, transitions, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.transitions = transitions
        self.accept_states = accept_states

    def read_string(self, input_str):
        curr = self.start_state

        for ch in input_str:
            if (not (curr in self.transitions)) or (not (ch in self.transitions[curr])):
                return 'false'            
            curr = self.transitions[curr][ch]

        if curr in self.accept_states:
            return 'true'
        else:
            return 'false'

    def default_new_state_ids(self):
        new_state_ids = {}
        next_id = 1
        for state_name in self.transitions.keys():
            new_state_ids[state_name] = next_id
            next_id += 1

        return new_state_ids

    def get_relabelled_dfa(self, new_state_ids=None):
        if new_state_ids == None:
            new_state_ids = self.default_new_state_ids()

        states = self.states
        alphabet = self.alphabet
        relabelled_start_state = new_state_ids[self.start_state]

        relabelled_transitions = {}
        for source_state in self.transitions:
            source_state_id = new_state_ids[source_state]
            relabelled_transitions[source_state_id] = {}

            for symbol in self.alphabet:
                if not (symbol in self.transitions[source_state]):
                    continue
                dest_state = self.transitions[source_state][symbol]
                dest_state_id = new_state_ids[dest_state]
                relabelled_transitions[source_state_id][symbol] = dest_state_id

        relabelled_accept_states = []
        for accept_state in self.accept_states:
            accept_state_id = new_state_ids[accept_state]
            relabelled_accept_states.append(accept_state_id)

        relabelled_dfa = DFA(states, alphabet, relabelled_start_state, relabelled_transitions, relabelled_accept_states)
        return relabelled_dfa

class NFA:
    def __init__(self, states, alphabet, start_state, transitions, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.transitions = transitions
        self.accept_states = accept_states

    def epsilon_closure(self, source_states):
        closure = set()
        queue = source_states[:]
        while len(queue) > 0:
            curr = queue.pop(0)
            closure.add(curr)
            if curr in self.transitions and 'e' in self.transitions[curr]:
                for dest in self.transitions[curr]['e']:
                    if dest not in closure:
                        queue.append(dest)

        return tuple(sorted(closure))

    def convert_to_dfa(self):
        dfa_states = set()
        dfa_transitions = {}

        dfa_start_state = self.epsilon_closure([self.start_state])
        queue = [dfa_start_state]
        while len(queue) > 0:
            dfa_source_state = queue.pop(0)
            assert dfa_source_state not in dfa_states
            assert dfa_source_state not in dfa_transitions


            dfa_states.add(dfa_source_state)
            dfa_transitions[dfa_source_state] = {}

            for symbol in self.alphabet:
                nfa_dest_states = set()
                for nfa_source_state in dfa_source_state:
                    if nfa_source_state in self.transitions and symbol in self.transitions[nfa_source_state]:
                        dest_states = self.transitions[nfa_source_state][symbol]
                        dest_states = self.epsilon_closure(dest_states)
                        nfa_dest_states.update(dest_states)
                dfa_dest_state = tuple(sorted(nfa_dest_states))
                dfa_transitions[dfa_source_state][symbol] = dfa_dest_state

                if dfa_dest_state not in dfa_states and dfa_dest_state not in queue:
                    queue.append(dfa_dest_state)

        dfa_accept_states = []
        for dfa_state in dfa_states:
            for nfa_accept_state in self.accept_states:
                if nfa_accept_state in dfa_state:
                    dfa_accept_states.append(dfa_state)
                    break

        dfa_states = len(dfa_states)
        dfa_alphabet = self.alphabet
        dfa = DFA(dfa_states, dfa_alphabet, dfa_start_state, dfa_transitions, dfa_accept_states)

        return dfa

op_stack = CStack()
val_stack = CStack()

class Node:
    def __init__(self,op,left,right):
        self.op = op
        self.left = left
        self.right = right
        self.order = 0

def has_concat():
    if val_stack.is_empty():
        return False
    elif op_stack.is_empty():
        return True
    else:
        return val_stack.top().order>op_stack.top().order
        
def prec(op):
    if op=='*':
        return 0
    elif op=='&':
        return 1
    elif op=='|':
        return 2
    elif op=='(':
        return 3
    else:
        return 4
        
def push_val(node):
    if has_concat():
        while (not op_stack.is_empty()) and prec(op_stack.top().op)<=prec('&'):
            if val_stack.length()<2:
                err_cnt += 1
                print("error:operand missing")
                break
            else:
                right = val_stack.pop()
                left = val_stack.pop()
                val_stack.push(Node(op_stack.pop().op,left,right))
        op_stack.push(Node('&',None,None))
    val_stack.push(node)
    
def parse_in(sregex):
    if True:
        err_cnt = 0
        regex = list(sregex)
        for c in regex:
            if c=='\n' or c=='\0' or err_cnt>0:
                break
            elif c==' ':
                continue
            elif c=='*':
                if val_stack.is_empty():
                    err_cnt += 1
                    print("error:operand missing")
                    break
                else:
                    node = Node(c,val_stack.pop(),None)
                    push_val(node)
            elif c=='|':
                while (not op_stack.is_empty()) and prec(op_stack.top().op)<=prec(c):
                    if val_stack.length()<2:
                        err_cnt += 1
                        print("error:operand missing")
                        break
                    else:
                        right = val_stack.pop()
                        left = val_stack.pop()
                        node = Node(op_stack.pop().op,left,right)
                        push_val(node)
                op_stack.push(Node(c,None,None))
            elif c=='(':
                op_stack.push(Node(c,None,None))
            elif c==')':
                op = ' '
                node = None
                while not op_stack.is_empty():
                    op = op_stack.pop().op
                    if op=='(':
                        break
                    elif val_stack.length()<2:
                        err_cnt += 1
                        print("error:operand missing")
                        break
                    else:
                        right = val_stack.pop()
                        left = val_stack.pop()
                        node = Node(op,left,right)
                        if (not op_stack.is_empty()) and op_stack.top().op!='(':
                            push_val(node)
                            node = None
                if op!='(':
                    err_cnt += 1
                    print("error:left and right paren mismach")
                    break
                elif node is not None:
                    push_val(node)
            elif c=='e' or c=='N' or c in alphabet:
                node = Node(c,None,None)
                push_val(node)
            else:
                err_cnt += 1
                print("error:invalid character found")
    while (not op_stack.is_empty()):
        if val_stack.length()<2:
            err_cnt += 1
            print("error:operand missing")
            break
        else:
            right = val_stack.pop()
            left = val_stack.pop()
            val_stack.push(Node(op_stack.pop().op,left,right))
    return err_cnt

def convert_to_nfa(node):
    global state_id
    eps = 'e'
    if node is None or node.op=='N':
        return NFA(0,alphabet,0,{},[])
    elif node.op=='e' or node.op in alphabet:
        states = 2
        start_state = state_id
        accept_states = [state_id+1]
        state_id += 2
        transitions = {}
        transitions[start_state] = {}
        transitions[start_state][node.op] = []
        transitions[start_state][node.op].append(accept_states[0])
        return NFA(states,alphabet,start_state,transitions,accept_states)
    elif node.op=='&':
        left = convert_to_nfa(node.left)
        right = convert_to_nfa(node.right)
        if left.states==0:
            return node.left
        elif right.states==0:
            return node.right
        states = left.states+right.states
        start_state = left.start_state
        transitions = left.transitions
        transitions.update(right.transitions)
        accept_states = right.accept_states
        for state in left.accept_states:
            if state not in transitions:
                transitions[state] = {}
            if eps not in transitions[state]:
                transitions[state][eps] = []
            transitions[state][eps].append(right.start_state)
        return NFA(states,alphabet,start_state,transitions,accept_states)
    elif node.op=='|':
        left = convert_to_nfa(node.left)
        right = convert_to_nfa(node.right)
        if left.states==0:
            return node.right
        elif right.states==0:
            return node.left
        left = convert_to_nfa(node.left)
        right = convert_to_nfa(node.right)
        states = left.states+right.states+1
        start_state = state_id
        state_id += 1
        transitions = left.transitions
        transitions.update(right.transitions)
        transitions[start_state] = {}
        transitions[start_state][eps] = []
        transitions[start_state][eps].append(left.start_state)
        transitions[start_state][eps].append(right.start_state)
        accept_states=left.accept_states+right.accept_states
        return NFA(states,alphabet,start_state,transitions,accept_states)
    elif node.op=='*':
        left = convert_to_nfa(node.left)
        states = left.states+2
        start_state = state_id
        accept_states = [state_id+1]
        state_id += 2
        transitions = left.transitions
        transitions[start_state] = {}
        transitions[start_state][eps] = []
        transitions[start_state][eps].append(accept_states[0])
        if left.states>0:
            transitions[start_state][eps].append(left.start_state)
            for state in left.accept_states:
                if state not in transitions:
                    transitions[state] = {}
                if eps not in transitions[state]:
                    transitions[state][eps] = []
                transitions[state][eps].append(left.start_state)
                transitions[state][eps].append(accept_states[0])
        return NFA(states,alphabet,start_state,transitions,accept_states)
    return NFA(0,alphabet,0,{},[])

def main(argv):
    global alphabet
    in_file = argv[1]
    out_file = argv[2]
    err_cnt = 0
    with open(in_file) as f:
        err_cnt = 0
        lines = f.read().splitlines()
        alphabet = list(lines[0])
        err_cnt = parse_in(lines[1])
    with open(out_file,'wt') as f:
        if val_stack.length()!=1 or err_cnt>0:
                f.write('invalid expression\n')
        else:
            nfa = convert_to_nfa(val_stack.top())
            dfa = nfa.convert_to_dfa().get_relabelled_dfa()
            del lines[0]
            del lines[0]
            for line in lines:
                line = line.strip()
                f.write(dfa.read_string(line))
                f.write('\n')

if __name__ == '__main__':
    main(sys.argv)
