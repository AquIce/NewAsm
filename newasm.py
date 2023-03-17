import json

class NewAsm:
	__REG = {}
	__COMMANDS = (
		'get',
		'reg',
		'upt',
		'mov',
		'cpy',
		'del',
		'eva',
		'nnd',
		'not',
		'and',
		'or',
		'xor',
		'mux',
		'dmx',
		'reg16',
		'upt16',
		'mov16',
		'cpy16',
		'del16',
		'eva16',
		'nnd16',
		'not16',
		'and16',
		'or16',
		'xor16',
		'mux16',
		'dmx16',
		'mux4w',
		'mux4w16',
		'mux8w',
		'mux8w16',
		'dmx4w',
		'dmx8w',
	)
	__COMMAND_CALLS = []
	__ARGS_NB = (0, 2, 2, 2, 2, 1, -1, 3, 2, 3, 3, 3, 4, 4, 2, 2, 2, 2, 1, -1, 3, 2, 3, 3, 3, 4, 4, 7, 7, 12, 12, 7, 12)
	__EVALUABLE =  7 * (False,) + 6 * (True,) + 14 * (False,) + 1 * (True,) + 1 * (False,) + 1 * (True,) + 3 * (False,)
	__EVALUABLE16 = 20 * (False,) + 7 * (True,) + 1 * (False,) + 1 * (True,) + 1 * (False,) + 1 * (True,) + 2 * (False,)
	__BIT_SIZABLE =  1 * (False,) + 13 * (True,) + 13 * (False,) + 1 * (True,) + 1 * (False,) + 1 * (True,) + 1 * (False,) + 2 * (False,)
	__STD_OUTS = ('cout', 'rout')
	__SYS_MEM = tuple([f'0x00000{i}' for i in '0123456789abcdef'] + [f'0xfffff{i}' for i in '0123456789abcdef'])
	__MEMORY_REGS = {
		'SYS_OUT': ['0x000000'],
		'SYS_MEM': [f'0x00000{i}' for i in '123456789abcdef'],
		'SYS_MEM16': [f'0xfffff{i}' for i in '0123456789abcdef']
	}
	__HEX = '0123456789abcdef'
	__DIRECTIVES = {
		'default': lambda x : x,
		'16bit': lambda x : ' '.join([i + '16' if i in NewAsm.__COMMANDS and NewAsm.__BIT_SIZABLE[NewAsm.__COMMANDS.index(i)] else i for i in x.split(' ')]),
	}

	def __init__(self, std_out=''):
		self.code = ''
		self.out = std_out if std_out in self.__STD_OUTS else self.__STD_OUTS[0]
		self.__COMMAND_CALLS = [
			self._get,
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
			self._mux,
			self._dmx,
			self._reg16,
			self._upt16,
			self._mov16,
			self._cpy16,
			self._del16,
			self._eva16,
			self._nnd16,
			self._not16,
			self._and16,
			self._or16,
			self._xor16,
			self._mux16,
			self._dmx16,
			self._mux4w,
			self._mux4w16,
			self._mux8w,
			self._mux8w16,
			self._dmx4w,
			self._dmx8w,
		]

	def check_mem_addr(self, mem_addr: str, admin=False) -> bool:
		if (not admin) and (mem_addr in self.__SYS_MEM):
			return False
		if mem_addr[0:2] != '0x' or len(mem_addr) != 8:
			return False
		for i in mem_addr[2:]:
			if i not in self.__HEX:
				return False
		return True

	def check_mem_addr16(self, mem_addr: str, admin=False) -> bool:
		if (not admin) and (mem_addr in self.__SYS_MEM):
			return False
		if mem_addr[0:2] != '0x' or len(mem_addr) != 8 or mem_addr[-1] != '0':
			return False
		for i in mem_addr[2:]:
			if i not in self.__HEX:
				return False
		return True

	def eva_cast(self, argval:list) -> tuple:
		if argval[0] not in self.__COMMANDS:
			return -1, self.error('eva::implicit', 'Invalid evaluation parameter', 1)
		if not self.__EVALUABLE[self.__COMMANDS.index(argval[0])]:
			return -1, self.error('eva::implicit', 'Command is not evaluatable', 1)
		tmp = self.__COMMAND_CALLS[self.__COMMANDS.index(argval[0])](argval + ['0x000000'], True), ''
		if tmp != (None, ''):
			return -1, tmp[0]
		return self.__REG['0x000000'], ''

	def check_val(self, val: int) -> bool:
		return str(val) in '01'

	def get_memory_reg(self, mem_addr: str) -> str:
		for i in self.__MEMORY_REGS.keys():
			if mem_addr in self.__MEMORY_REGS[i]:
				return i
		return 'USR_MEM'

	def read_file(self, file: str):
		with open(file, 'r') as f:
			self.code = [i.replace('\n', '') for i in f.readlines()]

	def error(self, command, message, argnb):
		return f'[NewAsm:({command}):error] {message} (arg[{argnb}])'

	def get_abs_arg_val(self, arg, command, argnb) -> tuple:
		if not arg in self.__REG.keys():
			if not self.check_val(arg):
				return -1, self.error(command, 'Invalid operand value', argnb)
			return int(arg), ''
		return self.__REG[arg], ''

	def get_abs_arg_val16(self, arg, command, argnb) -> tuple:
		if not arg in self.__REG.keys():
			if not self.check_val(arg):
				return -1, self.error(command, 'Invalid operand value', argnb)
			return arg, ''
		return ''.join([str(self.__REG[arg[:-1] + i]) for i in self.__HEX])

	# SECTION Memory Management (single bit)

	def _get(self, args, admin=False):
		return json.dumps({i: self.__REG[i] for i in self.__REG.keys() if self.get_memory_reg(i) == 'USR_MEM'}, indent=4)

	def _reg(self, args, admin=False):
		if not self.check_mem_addr(args[1]):
			return self.error('reg', 'Invalid registry address', 1)
		if args[1] in self.__REG.keys():
			return self.error('reg', 'Value already in registry', 1)
		if not self.check_val(args[2]):
			arg2 = self.get_abs_arg_val(args[2], 'reg', 2)
			if arg2[0] == -1:
				return arg2[1]
			args[2] = arg2[0]
		elif not self.check_val(args[2]):
			return self.error('reg', 'Invalid registry value', 2)
		elif len(args) - 1 > self.__ARGS_NB[self.__COMMANDS.index('reg')]:
			if args[2].isdigit():
				return self.error('reg', f'Too much arguments ({len(args) - 1} instead of {self.__ARGS_NB[self.__COMMANDS.index("reg")]})', '*')
			tmp = self.eva_cast(args[2:])
			if tmp[0] == -1:
				return tmp[1]
			args[2] = tmp[0]
		self.__REG[args[1]] = int(args[2])

	def _upt(self, args, admin=False):
		if not self.check_mem_addr(args[1]):
			return self.error('upt', 'Invalid registry address', 1)
		if not args[1] in self.__REG.keys():
			return self.error('upt', 'Value does not exist in registry', 1)
		if not self.check_val(args[2]):
			arg2 = self.get_abs_arg_val(args[2], 'upt', 2)
			if arg2[0] == -1:
				return arg2[1]
			args[2] = arg2[0]
		elif not self.check_val(args[2]):
			return self.error('upt', 'Invalid registry value', 2)
		elif len(args) - 1 > self.__ARGS_NB[self.__COMMANDS.index('reg')]:
			if args[2].isdigit():
				return self.error('upt', f'Too much arguments ({len(args) - 1} instead of {self.__ARGS_NB[self.__COMMANDS.index("upt")]})', '*')
			tmp = self.eva_cast(args[2:])
			if tmp[0] == -1:
				return tmp[1]
			args[2] = tmp[0]
		self.__REG[args[1]] = int(args[2])
	
	def _mov(self, args, admin=False):
		self._cpy(args, admin)
		del self.__REG[args[1]]

	def _cpy(self, args, admin=False):
		if not self.check_mem_addr(args[1]):
			return self.error('mov', 'Invalid source registry address', 1)
		if not self.check_mem_addr(args[2]):
			return self.error('mov', 'Invalid destination registry address', 2)
		if not args[1] in self.__REG.keys() and args[1] not in self.__SYS_MEM:
			return self.error('mov', 'Value does not exist in registry', 1)
		self.__REG[args[2]] = self.__REG[args[1]]

	def _del(self, args, admin=False):
		if not self.check_mem_addr(args[1]):
			return self.error('del', 'Invalid registry address', 1)
		for i in [f'{args[1][:-1]}' + j for j in self.__HEX]:
			print(i)
			if i not in self.__REG.keys():
				return self.error('del', 'Value does not exist in registry', 1)
			del self.__REG[i]

	# SECTION Memory Management (16-bit)

	def _reg16(self, args, admin=False):
		if not self.check_mem_addr16(args[1]):
			return self.error('reg16', 'Invalid registry address', 1)
		for i in [f'{args[1][:-1]}' + j for j in self.__HEX]:
			if i in self.__REG.keys():
				return self.error('reg16', 'Value already in registry', 1)
		if len(args) - 1 != self.__ARGS_NB[self.__COMMANDS.index('reg16')]:
			return self.error('reg16', f'Too much arguments ({len(args) - 1} instead of {self.__ARGS_NB[self.__COMMANDS.index("reg")]})', '*')
		if len(args[2]) != 16:
			return self.error('reg16', 'Invalid argument (need a 16-bit-value)', 2)
		cpt = 0
		for arg in args[2]:
			if not self.check_val(arg):
				return self.error('reg16', f'Invalid argument value at position {args[2].index(arg)} (must be a bit-value)', 2)
			self.__REG[args[1][:-1] + self.__HEX[cpt]] = int(arg)
			cpt += 1

	def _upt16(self, args, admin=False):
		if not self.check_mem_addr16(args[1]):
			return self.error('upt16', 'Invalid registry address', 1)
		for i in [f'{args[1][:-1]}' + j for j in self.__HEX]:
			if i not in self.__REG.keys():
				return self.error('upt16', 'Value does not exist in registry', 1)
		if len(args) - 1 != self.__ARGS_NB[self.__COMMANDS.index('reg16')]:
			return self.error('upt16', f'Too much arguments ({len(args) - 1} instead of {self.__ARGS_NB[self.__COMMANDS.index("reg")]})', '*')
		if len(args[2]) != 16:
			return self.error('upt16', 'Invalid argument (need a 16-bit-value)', 2)
		cpt = 0
		for arg in args[2]:
			if not self.check_val(arg):
				return self.error('upt16', f'Invalid argument value at position {args[2].index(arg)} (must be a bit-value)', 2)
			self.__REG[args[1][:-1] + self.__HEX[cpt]] = int(arg)
			cpt += 1

	def _mov16(self, args, admin=False):
		self._cpy16(args, admin)
		for i in [f'{args[1][:-1]}' + j for j in self.__HEX]:
			del self.__REG[i]

	def _cpy16(self, args, admin=False):
		if not self.check_mem_addr16(args[1]):
			return self.error('mov16', 'Invalid source registry address', 1)
		if not self.check_mem_addr16(args[2]):
			return self.error('mov16', 'Invalid destination registry address', 2)
		for i in self.__HEX:
			if args[1][:-1] + i not in self.__REG.keys():
				return self.error('mov16', 'Value does not exist in registry', 1)
			self.__REG[args[2][:-1] + i] = self.__REG[args[1][:-1] + i]

	def _del16(self, args, admin=False):
		if not self.check_mem_addr16(args[1]):
			return self.error('del16', 'Invalid registry address', 1)
		for i in [f'{args[1][:-1]}' + j for j in self.__HEX]:
			if i not in self.__REG.keys():
				return self.error('del16', 'Value does not exist in registry', 1)
			del self.__REG[i]

	# SECTION Evaluation (single bit + 16-bit)

	def _eva(self, args, admin=False):
		cmd = args[1]
		if not cmd in self.__COMMANDS:
			return self.error('eva', 'Invalid command to evaluate', 1)
		if not self.__EVALUABLE[self.__COMMANDS.index(cmd)]:
			return self.error('eva', 'Invalid command to evaluate', 1)
		argnb = self.__ARGS_NB[self.__COMMANDS.index(cmd)]
		if argnb != len(args) - 1:
			return self.error('eva', f'Invalid number of args for command {cmd}', 2)
		rt = self.__COMMAND_CALLS[self.__COMMANDS.index(cmd)](args[1:] + ['0x000000'], True)
		if rt != None:
			return rt
		tmp = self.__REG['0x000000']
		del self.__REG['0x000000']
		return tmp
	
	def _eva16(self, args, admin=False):
		cmd = args[1]
		cmd = args[1]
		if not cmd in self.__COMMANDS:
			return self.error('eva', 'Invalid command to evaluate', 1)
		if not self.__EVALUABLE16[self.__COMMANDS.index(cmd)]:
			return self.error('eva', 'Invalid command to evaluate', 1)
		argnb = self.__ARGS_NB[self.__COMMANDS.index(cmd)]
		if argnb != len(args) - 1:
			return self.error('eva', f'Invalid number of args for command {cmd}', 2)
		rt = self.__COMMAND_CALLS[self.__COMMANDS.index(cmd)](args[1:] + ['0xfffff0'], True)
		if rt != None:
			return rt
		tmp = [self.__REG['0xfffff' + i] for i in self.__HEX]
		for i in self.__HEX:
			del self.__REG['0xfffff' + i]
		return tmp

	# SECTION Boolean Operators (single bit)

	# BASE OPERATORS

	def _nnd(self, args, admin=False):
		arg1 = self.get_abs_arg_val(args[1], 'nnd', 1)
		arg2 = self.get_abs_arg_val(args[2], 'nnd', 2)
		if arg1[0] == -1:
			return arg1[1]
		if arg2[0] == -1:
			return arg2[1]
		if not self.check_mem_addr(args[3], admin):
			return self.error('nnd', 'Invalid destination registry address', 3)
		self.__REG[args[3]] = 1 if arg1[0] + arg2[0] != 2 else 0

	def _not(self, args, admin=False):
		arg = self.get_abs_arg_val(args[1], 'not', 1)
		if arg[0] == -1:
			return arg[1]
		if not self.check_mem_addr(args[2], admin):
			return self.error('not', 'Invalid destination registry address', 2)
		self._nnd(['nnd', arg[0], arg[0], args[2]], admin)

	def _and(self, args, admin=False):
		arg1 = self.get_abs_arg_val(args[1], 'and', 1)
		arg2 = self.get_abs_arg_val(args[2], 'and', 2)
		if arg1[0] == -1:
			return arg1[1]
		if arg2[0] == -1:
			return arg2[1]
		if not self.check_mem_addr(args[3], admin):
			return self.error('and', 'Invalid destination registry address', 3)
		self._nnd(['nnd', arg1[0], arg2[0], '0x000001'], True)
		self._not(['not', '0x000001', args[3]], True)

	def _or(self, args, admin=False):
		arg1 = self.get_abs_arg_val(args[1], 'or', 1)
		arg2 = self.get_abs_arg_val(args[2], 'or', 2)
		if arg1[0] == -1:
			return arg1[1]
		if arg2[0] == -1:
			return arg2[1]
		if not self.check_mem_addr(args[3], admin):
			return self.error('or', 'Invalid destination registry address', 3)
		self._not(['not', arg1[0], '0x000001'], True)
		self._not(['not', arg2[0], '0x000002'], True)
		self._nnd(['nnd', '0x000001', '0x000002', args[3]], True)

	def _xor(self, args, admin=False):
		arg1 = self.get_abs_arg_val(args[1], 'xor', 1)
		arg2 = self.get_abs_arg_val(args[2], 'xor', 2)
		if arg1[0] == -1:
			return arg1[1]
		if arg2[0] == -1:
			return arg2[1]
		if not self.check_mem_addr(args[3], admin):
			return self.error('or', 'Invalid destination registry address', 3)
		self._or(['or', arg1[0], arg2[0], '0x000003'], True)
		self._nnd(['nnd', arg1[0], arg2[0], '0x000004'], True)
		self._and(['and', '0x000003', '0x000004', args[3]], True)

	# ADVANCED OPERATORS

	def _mux(self, args, admin=False):
		sel = self.get_abs_arg_val(args[1], 'mux', 1)
		a = self.get_abs_arg_val(args[2], 'mux', 2)
		b = self.get_abs_arg_val(args[3], 'mux', 3)
		out = args[4]
		if sel[0] == -1:
			return sel[1]
		if b[0] == -1:
			return b[1]
		if a[0] == -1:
			return a[1]
		sel = sel[0]
		b = b[0]
		a = a[0]
		if not self.check_mem_addr(args[4], admin):
			return self.error('mux', 'Invalid destination registry address', 4)
		self._nnd(['nnd', b, sel, '0x000001'], True)
		self._nnd(['nnd', sel, sel, '0x000002'], True)
		self._nnd(['nnd', a, '0x000002', '0x000003'], True)
		self._nnd(['nnd', '0x000001', '0x000003', out], True)

	def _mux4w(self, args, admin=False):
		sel = [self.get_abs_arg_val(args[1], 'mux4w', 1), self.get_abs_arg_val(args[2], 'mux4w', 2)]
		a = self.get_abs_arg_val(args[3], 'mux4w', 3)
		b = self.get_abs_arg_val(args[4], 'mux4w', 4)
		c = self.get_abs_arg_val(args[5], 'mux4w', 5)
		d = self.get_abs_arg_val(args[6], 'mux4w', 6)
		out = args[7]
		if(sel[0][0] == -1):
			return sel[0][1]
		if(sel[1][0] == -1): 
			return sel[1][1]
		if a[0] == -1:
			return a[1]
		if b[0] == -1:
			return b[1]
		if c[0] == -1:
			return c[1]
		if d[0] == -1:
			return d[1]
		if not self.check_mem_addr(args[7], admin):
			return self.error('mux4w', 'Invalid destination registry address', 7)
		sel = [sel[0][0], sel[1][0]]
		a = a[0]
		b = b[0]
		c = c[0]
		d = d[0]
		self._mux(['mux', sel[0], a, b, '0x000004'], True)
		self._mux(['mux', sel[0], c, d, '0x000005'], True)
		self._mux(['mux', sel[1], '0x000004', '0x000005', out], True)

	def _mux8w(self, args, admin=False):
		sel = [self.get_abs_arg_val(args[1], 'mux8w', 1), self.get_abs_arg_val(args[2], 'mux8w', 2), self.get_abs_arg_val(args[3], 'mux8w', 3)]
		a = self.get_abs_arg_val(args[4], 'mux8w', 4)
		b = self.get_abs_arg_val(args[5], 'mux8w', 5)
		c = self.get_abs_arg_val(args[6], 'mux8w', 6)
		d = self.get_abs_arg_val(args[7], 'mux8w', 7)
		e = self.get_abs_arg_val(args[8], 'mux8w', 8)
		f = self.get_abs_arg_val(args[9], 'mux8w', 9)
		g = self.get_abs_arg_val(args[10], 'mux8w', 10)
		h = self.get_abs_arg_val(args[11], 'mux8w', 11)
		out = args[12]
		if(sel[0][0] == -1):
			return sel[0][1]
		if(sel[1][0] == -1): 
			return sel[1][1]
		if(sel[2][0] == -1): 
			return sel[2][1]
		if a[0] == -1:
			return a[1]
		if b[0] == -1:
			return b[1]
		if c[0] == -1:
			return c[1]
		if d[0] == -1:
			return d[1]
		if e[0] == -1:
			return e[1]
		if f[0] == -1:
			return f[1]
		if g[0] == -1:
			return g[1]
		if h[0] == -1:
			return h[1]
		if not self.check_mem_addr(args[12], admin):
			return self.error('mux8w', 'Invalid destination registry address', 12)
		sel = [sel[0][0], sel[1][0], sel[2][0]]
		a = a[0]
		b = b[0]
		c = c[0]
		d = d[0]
		e = e[0]
		f = f[0]
		g = g[0]
		h = h[0]
		self._mux4w(['mux4w', sel[0], sel[1], a, b, c, d, '0x000006'], True)
		self._mux4w(['mux4w', sel[0], sel[1], e, f, g, h, '0x000007'], True)
		self._mux(['mux', sel[2], '0x000006', '0x000007', out], True)

	def _dmx(self, args, admin=False):
		sel = self.get_abs_arg_val(args[1], 'dmx', 1)
		inp = self.get_abs_arg_val(args[2], 'dmx', 2)
		out1 = args[3]
		out2 = args[4]
		if inp[0] == -1:
			return inp[1]
		if sel[0] == -1:
			return sel[1]
		if not self.check_mem_addr(out1, admin):
			return self.error('dmx', 'Invalid destination registry address', 3)
		if not self.check_mem_addr(out2, admin):
			return self.error('dmx', 'Invalid destination registry address', 4)
		sel = sel[0]
		inp = inp[0]
		self._not(['not', sel, '0x000002'], True)
		self._and(['and', inp, '0x000002', out1], True)
		self._and(['and', inp, sel, out2], True)

	def _dmx4w(self, args, admin=False):
		sel = [self.get_abs_arg_val(args[1], 'dmx4w', 1), self.get_abs_arg_val(args[2], 'dmx4w', 2)]
		inp = self.get_abs_arg_val(args[3], 'dmx4w', 3)
		out1 = args[4]
		out2 = args[5]
		out3 = args[6]
		out4 = args[7]
		if inp[0] == -1:
			return inp[1]
		if sel[0][0] == -1:
			return sel[0][1]
		if sel[1][0] == -1:
			return sel[1][1]
		if not self.check_mem_addr(out1, admin):
			return self.error('dmx4w', 'Invalid destination registry address', 4)
		if not self.check_mem_addr(out2, admin):
			return self.error('dmx4w', 'Invalid destination registry address', 5)
		if not self.check_mem_addr(out3, admin):
			return self.error('dmx4w', 'Invalid destination registry address', 6)
		if not self.check_mem_addr(out4, admin):
			return self.error('dmx4w', 'Invalid destination registry address', 7)
		sel = [sel[0][0], sel[1][0]]
		inp = inp[0]
		self._dmx(['dmx', sel[1], inp, '0x000003', '0x000004'], True)
		self._dmx(['dmx', sel[0], '0x000003', out1, out2], True)
		self._dmx(['dmx', sel[0], '0x000004', out3, out4], True)
		
	def _dmx8w(self, args, admin=False):
		sel = [self.get_abs_arg_val(args[1], 'dmx8w', 1), self.get_abs_arg_val(args[2], 'dmx8w', 2), self.get_abs_arg_val(args[3], 'dmx8w', 3)]
		inp = self.get_abs_arg_val(args[4], 'dmx8w', 4)
		out1 = args[5]
		out2 = args[6]
		out3 = args[7]
		out4 = args[8]
		out5 = args[9]
		out6 = args[10]
		out7 = args[11]
		out8 = args[12]
		if sel[0][0] == -1:
			return sel[0][1]
		if sel[1][0] == -1:
			return sel[1][1]
		if inp[0] == -1:
			return inp[1]
		if not self.check_mem_addr(out1, admin):
			return self.error('dmx8w', 'Invalid destination registry address', 4)
		if not self.check_mem_addr(out2, admin):
			return self.error('dmx8w', 'Invalid destination registry address', 5)
		if not self.check_mem_addr(out3, admin):
			return self.error('dmx8w', 'Invalid destination registry address', 6)
		if not self.check_mem_addr(out4, admin):
			return self.error('dmx8w', 'Invalid destination registry address', 7)
		if not self.check_mem_addr(out5, admin):
			return self.error('dmx8w', 'Invalid destination registry address', 8)
		if not self.check_mem_addr(out6, admin):
			return self.error('dmx8w', 'Invalid destination registry address', 9)
		if not self.check_mem_addr(out7, admin):
			return self.error('dmx8w', 'Invalid destination registry address', 10)
		if not self.check_mem_addr(out8, admin):
			return self.error('dmx8w', 'Invalid destination registry address', 11)
		sel = [sel[0][0], sel[1][0], sel[2][0]]
		inp = inp[0]

		self._dmx(['dmx', sel[2], inp, '0x000005', '0x000006'], True)
		self._dmx4w(['dmx4w', sel[0], sel[1], '0x000005', out1, out2, out3, out4], True)
		self._dmx4w(['dmx4w', sel[0], sel[1], '0x000006', out5, out6, out7, out8], True)

	# SECTION Boolean Operators (16-bit)

	# BASIC OPERATORS

	def _nnd16(self, args, admin=False):
		arg1 = self.get_abs_arg_val16(args[1], 'nnd16', 1)
		arg2 = self.get_abs_arg_val16(args[2], 'nnd16', 2)
		if arg1[0] == -1:
			return arg1[1]
		if arg2[0] == -1:
			return arg2[1]
		if not self.check_mem_addr16(args[3], admin):
			return self.error('nnd16', 'Invalid destination registry address', 3)
		for i in self.__HEX:
			if args[1][:-1] + i not in self.__REG.keys():
				return self.error('nnd16', 'Value does not exist in registry', 1)
			self._nnd(['nnd', args[1][:-1] + i, args[2][:-1] + i, args[3][:-1] + i], admin)

	def _not16(self, args, admin=False):
		arg = self.get_abs_arg_val16(args[1], 'not16', 1)
		if arg[0] == -1:
			return arg[1]
		if not self.check_mem_addr16(args[2], admin):
			return self.error('not16', 'Invalid destination registry address', 2)
		for i in self.__HEX:
			if args[1][:-1] + i not in self.__REG.keys():
				return self.error('not16', 'Value does not exist in registry', 1)
			self._not(['not', args[1][:-1] + i, args[2][:-1] + i], admin)

	def _and16(self, args, admin=False):
		arg1 = self.get_abs_arg_val16(args[1], 'and16', 1)
		arg2 = self.get_abs_arg_val16(args[2], 'and16', 2)
		if arg1[0] == -1:
			return arg1[1]
		if arg2[0] == -1:
			return arg2[1]
		if not self.check_mem_addr16(args[3], admin):
			return self.error('and16', 'Invalid destination registry address', 3)
		for i in self.__HEX:
			if args[1][:-1] + i not in self.__REG.keys():
				return self.error('and16', 'Value does not exist in registry', 1)
			self._and(['and', args[1][:-1] + i, args[2][:-1] + i, args[3][:-1] + i], admin)

	def _or16(self, args, admin=False):
		arg1 = self.get_abs_arg_val16(args[1], 'or16', 1)
		arg2 = self.get_abs_arg_val16(args[2], 'or16', 2)
		if arg1[0] == -1:
			return arg1[1]
		if arg2[0] == -1:
			return arg2[1]
		if not self.check_mem_addr16(args[3], admin):
			return self.error('or16', 'Invalid destination registry address', 3)
		for i in self.__HEX:
			if args[1][:-1] + i not in self.__REG.keys():
				return self.error('or16', 'Value does not exist in registry', 1)
			self._or(['or', args[1][:-1] + i, args[2][:-1] + i, args[3][:-1] + i], admin)

	def _xor16(self, args, admin=False):
		arg1 = self.get_abs_arg_val16(args[1], 'xor16', 1)
		arg2 = self.get_abs_arg_val16(args[2], 'xor16', 2)
		if arg1[0] == -1:
			return arg1[1]
		if arg2[0] == -1:
			return arg2[1]
		if not self.check_mem_addr16(args[3], admin):
			return self.error('xor16', 'Invalid destination registry address', 3)
		for i in self.__HEX:
			if args[1][:-1] + i not in self.__REG.keys():
				return self.error('xor16', 'Value does not exist in registry', 1)
			self._xor(['xor', args[1][:-1] + i, args[2][:-1] + i, args[3][:-1] + i], admin)

	# ADVANCED OPERATORS

	def _mux16(self, args, admin=False):
		a = self.get_abs_arg_val16(args[1], 'mux16', 1)
		i1 = self.get_abs_arg_val16(args[2], 'mux16', 2)
		i0 = self.get_abs_arg_val16(args[3], 'mux16', 3)
		if a[0] == -1:
			return a[1]
		if i0[0] == -1:
			return i0[1]
		if i1[0] == -1:
			return i1[1]
		a = a[0]
		i0 = i0[0]
		i1 = i1[0]
		if not self.check_mem_addr16(args[4], admin):
			return self.error('mux16', 'Invalid destination registry address', 4)
		for i in self.__HEX:
			if args[2][:-1] + i not in self.__REG.keys():
				return self.error('mux16', 'Value does not exist in registry', 2)
			if args[3][:-1] + i not in self.__REG.keys():
				return self.error('mux16', 'Value does not exist in registry', 3)
			self._mux(['mux', args[1], args[2][:-1] + i, args[3][:-1] + i, args[4][:-1] + i], admin)

	def _mux4w16(self, args, admin=False):
		sel = [self.get_abs_arg_val16(args[1], 'mux4w16', 1), self.get_abs_arg_val16(args[2], 'mux4w16', 2)]
		a = self.get_abs_arg_val16(args[3], 'mux4w16', 3)
		b = self.get_abs_arg_val16(args[4], 'mux4w16', 4)
		c = self.get_abs_arg_val16(args[5], 'mux4w16', 5)
		d = self.get_abs_arg_val16(args[6], 'mux4w16', 6)
		out = args[7]
		if sel[0][0] == -1:
			return sel[0][1]
		if sel[1][0] == -1:
			return sel[1][1]
		if a[0] == -1:
			return a[1]
		if b[0] == -1:
			return b[1]
		if c[0] == -1:
			return c[1]
		if d[0] == -1:
			return d[1]
		sel = [sel[0][0], sel[1][0]]
		a = a[0]
		b = b[0]
		c = c[0]
		d = d[0]
		if not self.check_mem_addr16(out, admin):
			return self.error('mux4w16', 'Invalid destination registry address', 7)
		for i in self.__HEX:
			if args[3][:-1] + i not in self.__REG.keys():
				return self.error('mux4w16', 'Value does not exist in registry', 3)
			if args[4][:-1] + i not in self.__REG.keys():
				return self.error('mux4w16', 'Value does not exist in registry', 4)
			if args[5][:-1] + i not in self.__REG.keys():
				return self.error('mux4w16', 'Value does not exist in registry', 5)
			if args[6][:-1] + i not in self.__REG.keys():
				return self.error('mux4w16', 'Value does not exist in registry', 6)
			self._mux4w(['mux4w', args[1], args[2], args[3][:-1] + i, args[4][:-1] + i, args[5][:-1] + i, args[6][:-1] + i, args[7][:-1] + i], admin)

	def _mux8w16(self, args, admin=False):
		sel = [self.get_abs_arg_val16(args[1], 'mux8w16', 1), self.get_abs_arg_val16(args[2], 'mux8w16', 2), self.get_abs_arg_val16(args[3], 'mux8w16', 3)]
		a = self.get_abs_arg_val16(args[4], 'mux8w16', 4)
		b = self.get_abs_arg_val16(args[5], 'mux8w16', 5)
		c = self.get_abs_arg_val16(args[6], 'mux8w16', 6)
		d = self.get_abs_arg_val16(args[7], 'mux8w16', 7)
		e = self.get_abs_arg_val16(args[8], 'mux8w16', 8)
		f = self.get_abs_arg_val16(args[9], 'mux8w16', 9)
		g = self.get_abs_arg_val16(args[10], 'mux8w16', 10)
		h = self.get_abs_arg_val16(args[11], 'mux8w16', 11)
		out = args[12]
		if sel[0][0] == -1:
			return sel[0][1]
		if sel[1][0] == -1:
			return sel[1][1]
		if sel[2][0] == -1:
			return sel[2][1]
		if a[0] == -1:
			return a[1]
		if b[0] == -1:
			return b[1]
		if c[0] == -1:
			return c[1]
		if d[0] == -1:
			return d[1]
		if e[0] == -1:
			return e[1]
		if f[0] == -1:
			return f[1]
		if g[0] == -1:
			return g[1]
		if h[0] == -1:
			return h[1]
		sel = [sel[0][0], sel[1][0], sel[2][0]]
		a = a[0]
		b = b[0]
		c = c[0]
		d = d[0]
		e = e[0]
		f = f[0]
		g = g[0]
		h = h[0]
		if not self.check_mem_addr16(out, admin):
			return self.error('mux8w16', 'Invalid destination registry address', 12)
		for i in self.__HEX:
			if args[4][:-1] + i not in self.__REG.keys():
				return self.error('mux8w16', 'Value does not exist in registry', 4)
			if args[5][:-1] + i not in self.__REG.keys():
				return self.error('mux8w16', 'Value does not exist in registry', 5)
			if args[6][:-1] + i not in self.__REG.keys():
				return self.error('mux8w16', 'Value does not exist in registry', 6)
			if args[7][:-1] + i not in self.__REG.keys():
				return self.error('mux8w16', 'Value does not exist in registry', 7)
			if args[8][:-1] + i not in self.__REG.keys():
				return self.error('mux8w16', 'Value does not exist in registry', 8)
			if args[9][:-1] + i not in self.__REG.keys():
				return self.error('mux8w16', 'Value does not exist in registry', 9)
			if args[10][:-1] + i not in self.__REG.keys():
				return self.error('mux8w16', 'Value does not exist in registry', 10)
			if args[11][:-1] + i not in self.__REG.keys():
				return self.error('mux8w16', 'Value does not exist in registry', 11)
			self._mux8w(['mux8w', args[1], args[2], args[3], args[4][:-1] + i, args[5][:-1] + i, args[6][:-1] + i, args[7][:-1] + i, args[8][:-1] + i, args[9][:-1] + i, args[10][:-1] + i, args[11][:-1] + i, args[12][:-1] + i], admin)

	def _dmx16(self, args, admin=False):
		a = self.get_abs_arg_val16(args[1], 'dmx16', 1)
		i1 = self.get_abs_arg_val16(args[2], 'dmx16', 2)
		i0 = self.get_abs_arg_val16(args[3], 'dmx16', 3)
		if a[0] == -1:
			return a[1]
		if i0[0] == -1:
			return i0[1]
		if i1[0] == -1:
			return i1[1]
		a = a[0]
		i0 = i0[0]
		i1 = i1[0]
		if not self.check_mem_addr16(args[4], admin):
			return self.error('dmx16', 'Invalid destination registry address', 4)
		for i in self.__HEX:
			if args[2][:-1] + i not in self.__REG.keys():
				return self.error('dmx16', 'Value does not exist in registry', 2)
			if args[3][:-1] + i not in self.__REG.keys():
				return self.error('dmx16', 'Value does not exist in registry', 3)
			self._dmx(['dmx', args[1], args[2][:-1] + i, args[3][:-1] + i, args[4][:-1] + i], admin)

	# SECTION Compilation

	def compile(self, code: str = '') -> str:
		code = self.code if code == '' else code
		fn = self.__DIRECTIVES['default']
		for i in self.code:
			line = fn(i)
			if line == '' or line.startswith(':'):
				continue
			if line.startswith('@'):
				if line[1:] in self.__DIRECTIVES.keys():
					fn = self.__DIRECTIVES[line[1:]]
					continue
				else:
					print(self.error(line, 'Invalid directive', 0))
					return
			args = line.split(' ')
			if not args[0] in self.__COMMANDS:
				return self.error(args[0], 'Invalid command', 0)
			out = self.__COMMAND_CALLS[self.__COMMANDS.index(args[0])](args)
			if out != None:
				if self.out == 'cout':
					print(f'[NewAsm:({args[0]}):{self.out}] >> {out}')
				elif self.out == 'rout':
					print(f'[NewAsm:{args[0]}:{self.out}]')
					return out
