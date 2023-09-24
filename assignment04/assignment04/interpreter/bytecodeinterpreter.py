class BytecodeInterpreter:
    def __init__(self, am: tuple[str, str], args=[]):
        self.memory = {}
        # Method stack is a list of Local variables, operand stack, and program counter with method id

        args = {i: args[i] for i in range(0, len(args))}

        self.mstack = [(args, [], (am, 0))]
        self.MAX_OPERATIONS = 10000

    def run(self, program: dict[str, any]) -> any:
        for i in range(0, self.MAX_OPERATIONS):
            print(f"-> {self.mstack}", end=" ")
            (lv, os, (am, pc)) = self.mstack[-1]

            code = program[am[0]][am[1]]

            bc = code["bytecode"][pc]

            if bc["opr"] == "return":
                if bc["type"] is None:
                    print("(return)")
                    if len(self.mstack) > 1:
                        self.mstack.pop()
                    else:
                        return None
                elif bc["type"] == "int":
                    print("(return)")
                    if len(self.mstack) > 1:
                        (lv_, os_, (am_, pc_)) = self.mstack[-2]
                        self.mstack[-2] = (lv_, os_ + [os[-1]], (am_, pc_))
                        self.mstack.pop()
                    else:
                        return os[-1]
                else:
                    print(f"Operation not implemented {bc}")
                    return
            elif bc["opr"] == "push":
                print("(push)")
                value = bc["value"]["value"]
                self.mstack[-1] = (lv, os + [value], (am, pc + 1))
            elif bc["opr"] == "load":
                print("(load)")
                index = bc["index"]
                value = lv[index]
                self.mstack[-1] = (lv, os + [value], (am, pc + 1))
            elif bc["opr"] == "binary":
                if bc["operant"] == "add":
                    print("(add)")
                    left = os[-2]
                    right = os[-1]
                    self.mstack[-1] = (lv, os[:-2] + [left + right], (am, pc + 1))
                elif bc["operant"] == "mul":
                    print("(mul)")
                    left = os[-2]
                    right = os[-1]
                    self.mstack[-1] = (lv, os[:-2] + [left * right], (am, pc + 1))
                elif bc["operant"] == "sub":
                    print("(sub)")
                    left = os[-2]
                    right = os[-1]
                    self.mstack[-1] = (lv, os[:-2] + [left - right], (am, pc + 1))
                else:
                    print(f"Operation not implemented {bc}")
                    return
            elif bc["opr"] == "if":
                left = os[-2]
                right = os[-1]
                if bc["condition"] == "gt":
                    print("(if gt)")
                    if left > right:
                        self.mstack[-1] = (lv, os[:-2], (am, bc["target"]))
                    else:
                        self.mstack[-1] = (lv, os[:-2], (am, pc + 1))
                elif bc["condition"] == "ge":
                    print("(if ge)")
                    if left >= right:
                        self.mstack[-1] = (lv, os[:-2], (am, bc["target"]))
                    else:
                        self.mstack[-1] = (lv, os[:-2], (am, pc + 1))
                elif bc["condition"] == "le":
                    print("(if le)")
                    if left <= right:
                        self.mstack[-1] = (lv, os[:-2], (am, bc["target"]))
                    else:
                        self.mstack[-1] = (lv, os[:-2], (am, pc + 1))
                else:
                    print(f"Operation not implemented {bc}")
                    return
            elif bc["opr"] == "ifz":
                left = os[-1]
                right = 0
                if bc["condition"] == "le":
                    print("(ifz le)")
                    if left <= right:
                        self.mstack[-1] = (lv, os[:-1], (am, bc["target"]))
                    else:
                        self.mstack[-1] = (lv, os[:-1], (am, pc + 1))
                else:
                    print(f"Operation not implemented {bc}")
                    return
            elif bc["opr"] == "incr":
                print("(incr)")
                index = bc["index"]
                amount = bc["amount"]
                lv[index] = lv[index] + amount
                self.mstack[-1] = (lv, os, (am, pc + 1))
            elif bc["opr"] == "store":
                print("(store)")
                index = bc["index"]
                value = os[-1]
                lv[index] = value
                self.mstack[-1] = (lv, os[:-1], (am, pc + 1))
            elif bc["opr"] == "goto":
                print("(goto)")
                self.mstack[-1] = (lv, os, (am, bc["target"]))
            elif bc["opr"] == "invoke":
                print("(invoke)")
                method = bc["method"]
                args = {
                    i: value for i, value in enumerate(
                        os[-len(method["args"]):]
                    )
                }

                self.mstack[-1] = (lv, os[:-len(method["args"])], (am, pc + 1))
                self.mstack.append((args, [], ((method["ref"]["name"], method["name"]), 0)))
            elif bc["opr"] == "newarray":
                print("(newarray)")
                size = os[-1]
                self.mstack[-1] = (lv, os[:-1] + [[None] * size], (am, pc + 1))
            elif bc["opr"] == "array_store":
                print("(array_store)")
                array = os[-3]
                index = os[-2]
                value = os[-1]
                array[index] = value
                self.mstack[-1] = (lv, os[:-2], (am, pc + 1))
            elif bc["opr"] == "dup":
                # I have no idea, what "dup" does, so it just skips it for now
                print("(dup)")
                self.mstack[-1] = (lv, os, (am, pc + 1))
            elif bc["opr"] == "array_load":
                print("(array_load)")
                array = os[-2]
                index = os[-1]
                value = array[index]
                self.mstack[-1] = (lv, os[:-2] + [value], (am, pc + 1))
            elif bc["opr"] == "arraylength":
                array = os[-1]
                length = len(array)
                self.mstack[-1] = (lv, os[:-1] + [length], (am, pc + 1))
            else:
                print(f"Operation not implemented {bc}")
                return

            print(bc)
        print("Max operations reached")
