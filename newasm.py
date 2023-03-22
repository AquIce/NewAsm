class NewAsm:
	# BASE OPERATORS
	def NAND(self, a:int, b:int) -> int:
		"""NAND

		Args:
			a (int): First value
			b (int): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			int: Result
		"""
		for i in (a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return 1 if a + b != 2 else 0
	
	def NAND16(self, a:list[int], b:list[int]) -> list[int]:
		"""NAND16

		Args:
			a (list[int]): First value
			b (list[int]): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		if len(a) != 16 or len(b) != 16:
			raise AttributeError('Invalid value')
		return [self.NAND(a[i], b[i]) for i in range(16)]

	def NOT(self, a:int) -> int:
		"""NOT
		
		Args:
			a (int): Value

		Raises:
			AttributeError: Invalid value

		Returns:
			int: Result
		"""
		if a not in (0, 1):
			raise AttributeError('Invalid value')
		return self.NAND(a, a)
	
	def NOT16(self, a:list[int]) -> list[int]:
		"""NOT16

		Args:
			a (list[int]): Value

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		if len(a) != 16:
			raise AttributeError('Invalid value')
		return [self.NOT(a[i]) for i in range(16)]

	def AND(self, a:int, b:int) -> int:
		"""AND

		Args:
			a (int): First value
			b (int): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			int: Result
		"""
		for i in (a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.NOT(
			self.NAND(a, b)
		)

	def AND16(self, a:list[int], b:list[int]) -> list[int]:
		"""AND16

		Args:
			a (list[int]): First value
			b (list[int]): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		if len(a) != 16 or len(b) != 16:
			raise AttributeError('Invalid value')
		return [self.AND(a[i], b[i]) for i in range(16)]
	
	def OR(self, a:int, b:int) -> int:
		"""OR
		
		Args:
			a (int): First value
			b (int): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			int: Result
		"""
		for i in (a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.NAND(
			self.NOT(a),
			self.NOT(b)
		)
	
	def OR16(self, a:list[int], b:list[int]) -> list[int]:
		"""OR16

		Args:
			a (list[int]): First value
			b (list[int]): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		if len(a) != 16 or len(b) != 16:
			raise AttributeError('Invalid value')
		return [self.OR(a[i], b[i]) for i in range(16)]

	def XOR(self, a:int, b:int) -> int:
		"""XOR

		Args:
			a (int): First value
			b (int): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			int: Result
		"""
		for i in (a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.AND(
			self.OR(a, b),
			self.NAND(a, b)
		)

	def XOR16(self, a:list[int], b:list[int]) -> list[int]:
		"""XOR16

		Args:
			a (list[int]): First value
			b (list[int]): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		if len(a) != 16 or len(b) != 16:
			raise AttributeError('Invalid value')
		return [self.XOR(a[i], b[i]) for i in range(16)]

	# ADVANCED OPERATORS

	def MUX(self, sel:int, a:int, b:int) -> int:
		"""MUX

		Args:
			sel (int): Selector
			a (int): First value
			b (int): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			int: Result
		"""
		for i in (sel, a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.NAND(
			self.NAND(b, sel),
			self.NAND(
				a,
				self.NAND(sel, sel)
			)
		)
	
	def MUX16(self, sel:int, a:list[int], b:list[int]) -> list[int]:
		"""MUX16

		Args:
			sel (int): Selector
			a (list[int]): First value
			b (list[int]): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		if len(a) != 16 or len(b) != 16:
			raise AttributeError('Invalid value')
		return [self.MUX(sel, a[i], b[i]) for i in range(16)]

	def MUX4W(self, sel:list[int], a:int, b:int, c:int, d:int) -> int:
		"""MUX4W

		Args:
			sel (list[int]): Selector (2 bits)
			a (int): First value
			b (int): Second value
			c (int): Third value
			d (int): Fourth value

		Raises:
			AttributeError: Invalid value

		Returns:
			int: Result
		"""
		for i in (sel[0], sel[1], a, b, c, d):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.MUX(
			sel[1],
			self.MUX(sel[0], a, b),
			self.MUX(sel[0], c, d)
		)
	
	def MUX4W16(self, sel:list[int], a:list[int], b:list[int], c:list[int], d:list[int]) -> list[int]:
		"""MUX4W16

		Args:
			sel (list[int]): Selector (2 bits)
			a (list[int]): First value
			b (list[int]): Second value
			c (list[int]): Third value
			d (list[int]): Fourth value

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		if len(a) != 16 or len(b) != 16 or len(c) != 16 or len(d) != 16:
			raise AttributeError('Invalid value')
		return [self.MUX4W(sel, a[i], b[i], c[i], d[i]) for i in range(16)]

	def MUX8W(self, sel:list[int], a:int, b:int, c:int, d:int, e:int, f:int, g:int, h:int) -> int:
		"""MUX8W

		Args:
			sel (list[int]): Selector (3 bits)
			a (int): First value
			b (int): Second value
			c (int): Third value
			d (int): Fourth value
			e (int): Fifth value
			f (int): Sixth value
			g (int): Seventh value
			h (int): Eighth value

		Raises:
			AttributeError: Invalid value

		Returns:
			int: Result
		"""
		for i in (sel[0], sel[1], sel[2], a, b, c, d, e, f, g, h):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.MUX(
			sel[2],
			self.MUX4W([sel[0], sel[1]], a, b, c, d),
			self.MUX4W([sel[0], sel[1]], e, f, g, h)
		)
	
	def MUX8W16(self, sel:list[int], a:list[int], b:list[int], c:list[int], d:list[int], e:list[int], f:list[int], g:list[int], h:list[int]) -> list[int]:
		"""MUX8W16

		Args:
			sel (list[int]): Selector (3 bits)
			a (list[int]): First value
			b (list[int]): Second value
			c (list[int]): Third value
			d (list[int]): Fourth value
			e (list[int]): Fifth value
			f (list[int]): Sixth value
			g (list[int]): Seventh value
			h (list[int]): Eighth value

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		if len(a) != 16 or len(b) != 16 or len(c) != 16 or len(d) != 16 or len(e) != 16 or len(f) != 16 or len(g) != 16 or len(h) != 16:
			raise AttributeError('Invalid value')
		return [self.MUX8W(sel, a[i], b[i], c[i], d[i], e[i], f[i], g[i], h[i]) for i in range(16)]

	def DEMUX(self, sel:int, inp:int) -> list[int]:
		"""DEMUX

		Args:
			sel (int): Selector
			inp (int): Input

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		for i in (sel, inp):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return [
			self.AND(
				inp,
				self.NOT(sel)
			), self.AND(inp, sel)
		]
	
	def DEMUX16(self, sel:int, inp:list[int]) -> list[list[int]]:
		"""DEMUX16

		Args:
			sel (int): Selector
			inp (list[int]): Input

		Raises:
			AttributeError: Invalid value

		Returns:
			list[list[int]]: Result
		"""
		if len(inp) != 16:
			raise AttributeError('Invalid value')
		return [list(i) for i in zip(*[self.DEMUX(sel, inp[j]) for j in range(0, 16)])]

	def DEMUX4W(self, sel:list[int], inp:int) -> list[int]:
		"""DEMUX4W

		Args:
			sel (list[int]): Selector (2 bits)
			inp (int): Input

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		for i in (sel[0], sel[1], inp):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		tmp = self.DEMUX(sel[1], inp)
		return self.DEMUX(sel[0], tmp[0]) + self.DEMUX(sel[0], tmp[1])
	
	def DEMUX4W16(self, sel:list[int], inp:list[int]) -> list[list[int]]:
		"""DEMUX4W16

		Args:
			sel (list[int]): Selector (2 bits)
			inp (list[int]): Input

		Raises:
			AttributeError: Invalid value

		Returns:
			list[list[int]]: Result
		"""
		if len(inp) != 16:
			raise AttributeError('Invalid value')
		return [list(i) for i in zip(*[self.DEMUX4W(sel, inp[j]) for j in range(0, 16)])]
		
	def DEMUX8W(self, sel:list[int], inp:int) -> list[int]:
		"""DEMUX8W

		Args:
			sel (list[int]): Selector (3 bits)
			inp (int): Input

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		for i in (sel[0], sel[1], sel[2], inp):
			if i not in (0, 1):
				raise AttributeError('Invalid value')

		tmp = self.DEMUX(sel[2], inp)
		return self.DEMUX4W([sel[0], sel[1]], tmp[0]) + self.DEMUX4W([sel[0], sel[1]], tmp[1])
	
	def DEMUX8W16(self, sel:list[int], inp:list[int]) -> list[list[int]]:
		"""DEMUX8W16

		Args:
			sel (list[int]): Selector (3 bits)
			inp (list[int]): Input

		Raises:
			AttributeError: Invalid value

		Returns:
			list[list[int]]: Result
		"""
		if len(inp) != 16:
			raise AttributeError('Invalid value')
		return [list(i) for i in zip(*[self.DEMUX8W(sel, inp[j]) for j in range(0, 16)])]
	
	# ALU
	
	def HalfAdder(self, a:int, b:int) -> tuple[int, int]:
		"""HalfAdder

		Args:
			a (int): First value
			b (int): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			tuple[int, int]: (sum, carry)
		"""
		for i in (a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.XOR(a, b), self.AND(a, b)
	
	def ADDER(self, a:int, b:int, c:int) -> tuple[int, int]:
		"""ADDER

		Args:
			a (int): First value
			b (int): Second value
			c (int): Carry

		Raises:
			AttributeError: Invalid value

		Returns:
			tuple[int, int]: (sum, carry)
		"""
		for i in (a, b, c):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		tmp = self.HalfAdder(a, b)
		return self.XOR(tmp[0], c), self.OR(tmp[1], self.AND(tmp[0], c))
	
	def ADDER16(self, a:list[int], b:list[int]) -> tuple[list[int], int]:
		"""ADDER16

		Args:
			a (list[int]): First value
			b (list[int]): Second value

		Raises:
			AttributeError: Invalid value

		Returns:
			tuple[list[int], int]: (sum, carry)
		"""
		if len(a) != 16 or len(b) != 16:
			raise AttributeError('Invalid value')
		for i in a + b:
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		sum = []
		carry = 0
		for i in range(16):
			tmp = self.ADDER(a[i], b[i], carry)
			sum.append(tmp[0])
			carry = tmp[1]
		return sum, carry
	
	def INC16(self, a:list[int]) -> list[int]:
		"""INC16

		Args:
			a (list[int]): Value

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Sum
		"""
		if len(a) != 16:
			raise AttributeError('Invalid value')
		for i in a:
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.ADDER16(a, [0]*16)[0]
	
	def TRUE(self) -> int:
		"""TRUE

		Returns:
			int: 1
		"""
		return 1
	
	def TRUE16(self) -> list[int]:
		"""TRUE16

		Returns:
			list[int]: 1
		"""
		return [self.TRUE()]*16
	
	def FALSE(self) -> int:
		"""FALSE

		Returns:
			int: 0
		"""
		return 0
	
	def FALSE16(self) -> list[int]:
		"""FALSE16

		Returns:
			list[int]: 0
		"""
		return [self.FALSE()]*16
	
	def ALU(self, x:list[int], y:list[int], zx:int, nx:int, zy:int, ny:int, f:int, no:int) -> list[int]:
		"""ALU

		Args:
			x (list[int]): First value
			y (list[int]): Second value
			zx (int): Zero x
			nx (int): Not x
			zy (int): Zero y
			ny (int): Not y
			f (int): Function
			no (int): Not out

		Raises:
			AttributeError: Invalid value

		Returns:
			list[int]: Result
		"""
		if len(x) != 16 or len(y) != 16:
			raise AttributeError('Invalid value')
		for i in (zx, nx, zy, ny, f, no):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		tmp = 0
		if zx:
			x = self.FALSE16()
		if nx:
			x = self.NOT16(x)
		if zy:
			y = self.FALSE16()
		if ny:
			y = self.NOT16(y)
		if f:
			tmp = self.ADDER16(x, y)
		else:
			tmp = self.AND16(x, y)
		if no:
			tmp = self.NOT16(tmp)