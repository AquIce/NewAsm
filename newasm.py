class NewAsm:
    __COMMANDS = (
        "grg",
        "reg",
        "upt",
        "mov",
        "cpy",
        "del",
        "eva",
        "nnd",
        "not",
        "and",
        "or",
        "xor",
    )
    __COMMAND_CALLS = []
    __ARGS_NB = (0, 2, 2, 2, 2, 1, -1, 3, 2, 3, 3, 3)
    __EVALUABLE =  7 * (False,) + 5 * (True,)
    __STD_OUTS = ("cout", "rout")
    __SYS_MEM = tuple([f"0x00000{i}" for i in "0123456789abcdef"])
    __MEMORY_REGS = {
        "SYS_OUT": ["0x000000"],
        "SYS_MEM": [f"0x00000{i}" for i in "123456789abcdef"],
    }

    def __init__(self, std_out=""):
        self.reg = {}
        self.code = ""
        self.out = std_out if std_out in self.__STD_OUTS else self.__STD_OUTS[0]
        self.__COMMAND_CALLS = [
            self._grg,
            self._reg,
            self._upt,
            self._mov,
            self._cpy,
            self._del,
            self._eva,
            self._nnd,
            self._not,
            self._and,
            self._or,
            self._xor,
        ]

    def check_mem_addr(self, mem_addr: str, admin=False) -> bool:
        if (not admin) and (mem_addr in self.__SYS_MEM):
            return False
        if mem_addr[0:2] != "0x" or len(mem_addr) != 8:
            return False
        for i in mem_addr[2:]:
            if i not in "0123456789abcdef":
                return False
        return True

    def eva_cast(self, argval:list) -> tuple:
        if argval[0] not in self.__COMMANDS:
            return -1, self.error("eva::implicit", "Invalid command to evaluate", 1)
        if not self.__EVALUABLE[self.__COMMANDS.index(argval[0])]:
            return -1, self.error("eva::implicit", "Command is not evaluatable", 1)
        tmp = self.__COMMAND_CALLS[self.__COMMANDS.index(argval[0])](argval + ['0x000000'], True), ''
        if tmp != (None, ''):
            return -1, tmp[0]
        return self.reg['0x000000'], ''

    def check_val(self, val: int) -> bool:
        return str(val) in "01"

    def get_memory_reg(self, mem_addr: str) -> str:
        for i in self.__MEMORY_REGS.keys():
            if mem_addr in self.__MEMORY_REGS[i]:
                return i
        return "USR_MEM"

    def read_file(self, file: str):
        with open(file, "r") as f:
            self.code = [i.replace("\n", "") for i in f.readlines()]

    def error(self, command, message, argnb):
        return f"[NewAsm:({command}):error] {message} (arg[{argnb}])"

    def get_abs_arg_val(self, arg, command, argnb) -> tuple:
        if not arg in self.reg.keys():
            if not self.check_val(arg):
                return -1, self.error(command, "Invalid operand value", argnb)
            return int(arg), ""
        return self.reg[arg], ""

    def _grg(self, args, admin=False):
        return self.reg

    def _reg(self, args, admin=False):
        if not self.check_mem_addr(args[1]):
            return self.error("reg", "Invalid registry address", 1)
        if args[1] in self.reg.keys() and args[1] not in self.__SYS_MEM:
            return self.error("reg", "Value already in registry", 1)
        print(len(args) - 1, self.__ARGS_NB[self.__COMMANDS.index("reg")])
        if len(args) - 1 == self.__ARGS_NB[self.__COMMANDS.index("reg")]:
            arg2 = self.get_abs_arg_val(args[2], "reg", 2)
            if arg2[0] == -1:
                return arg2[1]
            args[2] = arg2[0]
        elif (not self.check_val(args[2]) and len(args) == self.__ARGS_NB[self.__COMMANDS.index("reg")]):
            return self.error("reg", "Invalid registry value", 2)
        elif len(args) > self.__ARGS_NB[self.__COMMANDS.index("reg")]:
            tmp = self.eva_cast(args[2:])
            if tmp[0] == -1:
                return tmp[1]
            args[2] = tmp[0]
        self.reg[args[1]] = int(args[2])

    def _upt(self, args, admin=False):
        if not self.check_mem_addr(args[1]):
            return self.error("upt", "Invalid registry address", 1)
        if not args[1] in self.reg.keys() and args[1] not in self.__SYS_MEM:
            return self.error("upt", "Value does not exist in registry", 1)
        if len(args) - 1 == self.__ARGS_NB[self.__COMMANDS.index("upt")]:
            arg2 = self.get_abs_arg_val(args[2], "upt", 2)
            if arg2[0] == -1:
                return arg2[1]
            args[2] = arg2[0]
        elif (not self.check_val(args[2]) and len(args) == self.__ARGS_NB[self.__COMMANDS.index("upt")]):
            return self.error("upt", "Invalid registry value", 2)
        elif len(args) > self.__ARGS_NB[self.__COMMANDS.index("upt")]:
            tmp = self.eva_cast(args[2:])
            if tmp[0] == -1:
                return tmp[1]
            args[2] = tmp[0]
        self.reg[args[1]] = int(args[2])

    def _mov(self, args, admin=False):
        self._cpy(args, admin)
        del self.reg[args[1]]

    def _cpy(self, args, admin=False):
        if not self.check_mem_addr(args[1]):
            return self.error("mov", "Invalid source registry address", 1)
        if not self.check_mem_addr(args[2]):
            return self.error("mov", "Invalid destination registry address", 2)
        if not args[1] in self.reg.keys() and args[1] not in self.__SYS_MEM:
            return self.error("mov", "Value does not exist in registry", 1)
        self.reg[args[2]] = self.reg[args[1]]

    def _del(self, args, admin=False):
        if not self.check_mem_addr(args[1]):
            return self.error("del", "Invalid registry address", 1)
        if not args[1] in self.reg.keys() and args[1] not in self.__SYS_MEM:
            return self.error("del", "Value does not exist in registry", 1)
        del self.reg[args[1]]

    def _eva(self, args, admin=False):
        cmd = args[1]
        if not cmd in self.__COMMANDS:
            return self.error("eva", "Invalid command to evaluate", 1)
        if not self.__EVALUABLE[self.__COMMANDS.index(cmd)]:
            return self.error("eva", "Invalid command to evaluate", 1)
        argnb = self.__ARGS_NB[self.__COMMANDS.index(cmd)]
        if argnb != len(args) - 1:
            return self.error("eva", f"Invalid number of args for command \`{cmd}\`", 2)
        self.__COMMAND_CALLS[self.__COMMANDS.index(cmd)](args[1:] + ["0x000000"], True)
        tmp = self.reg["0x000000"]
        del self.reg["0x000000"]
        return tmp

    # BOOLEAN OPERATORS

    # NAND

    def _nnd(self, args, admin=False):
        arg1 = self.get_abs_arg_val(args[1], "nnd", 1)
        arg2 = self.get_abs_arg_val(args[2], "nnd", 2)
        if arg1[0] == -1:
            return arg1[1]
        if arg2[0] == -1:
            return arg2[1]
        if not self.check_mem_addr(args[3], admin):
            return self.error("nnd", "Invalid destination registry address", 3)
        self.reg[args[3]] = 1 if arg1[0] + arg2[0] != 2 else 0

    # BASE OPERATORS

    def _not(self, args, admin=False):
        arg = self.get_abs_arg_val(args[1], "not", 1)
        if arg[0] == -1:
            return arg[1]
        if not self.check_mem_addr(args[2], admin):
            return self.error("not", "Invalid destination registry address", 2)
        self._nnd(["nnd", arg[0], arg[0], args[2]], admin)

    def _and(self, args, admin=False):
        arg1 = self.get_abs_arg_val(args[1], "and", 1)
        arg2 = self.get_abs_arg_val(args[2], "and", 2)
        if arg1[0] == -1:
            return arg1[1]
        if arg2[0] == -1:
            return arg2[1]
        if not self.check_mem_addr(args[3], admin):
            return self.error("and", "Invalid destination registry address", 3)
        self._nnd(["nnd", arg1[0], arg2[0], "0x000001"], True)
        self._not(["not", "0x000001", args[3]], True)

    def _or(self, args, admin=False):
        arg1 = self.get_abs_arg_val(args[1], "or", 1)
        arg2 = self.get_abs_arg_val(args[2], "or", 2)
        if arg1[0] == -1:
            return arg1[1]
        if arg2[0] == -1:
            return arg2[1]
        if not self.check_mem_addr(args[3], admin):
            return self.error("or", "Invalid destination registry address", 3)
        self._not(["not", arg1[0], "0x000001"], True)
        self._not(["not", arg2[0], "0x000002"], True)
        self._nnd(["nnd", "0x000001", "0x000002", args[3]], True)

    # ADVANCED OPERATORS

    def _xor(self, args, admin=False):
        arg1 = self.get_abs_arg_val(args[1], "xor", 1)
        arg2 = self.get_abs_arg_val(args[2], "xor", 2)
        if arg1[0] == -1:
            return arg1[1]
        if arg2[0] == -1:
            return arg2[1]
        if not self.check_mem_addr(args[3], admin):
            return self.error("or", "Invalid destination registry address", 3)
        self._or(["or", arg1[0], arg2[0], "0x000001"], True)
        self._nnd(["nnd", arg1[0], arg2[0], "0x000002"], True)
        self._and(["and", "0x000001", "0x000002", args[3]], True)

    def compile(self, code: str = "") -> str:
        code = self.code if code == "" else code
        for i in self.code:
            args = i.split(" ")
            if not args[0] in self.__COMMANDS:
                return self.error(args[0], "Invalid command", 0)
            out = self.__COMMAND_CALLS[self.__COMMANDS.index(args[0])](args)
            if out != None:
                if self.out == "cout":
                    print(f"[NewAsm:({args[0]}):{self.out}] >> {out}")
                elif self.out == "rout":
                    print(f"[NewAsm:{args[0]}:{self.out}]")
                    return out
