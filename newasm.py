class NewAsm:
	# BASE OPERATORS
	def NAND(self, a, b):
		for i in (a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return 1 if a + b != 2 else 0

	def NOT(self, a):
		if a not in (0, 1):
			raise AttributeError('Invalid value')
		return self.NAND(a, a)

	def AND(self, a, b):
		for i in (a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.NOT(
			self.NAND(a, b)
		)

	def OR(self, a, b):
		for i in (a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.NAND(
			self.NOT(a),
			self.NOT(b)
		)

	def XOR(self, a, b):
		for i in (a, b):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.AND(
			self.OR(a, b),
			self.NAND(a, b)
		)

	# ADVANCED OPERATORS

	def MUX(self, sel, a, b):
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

	def MUX4W(self, sel, a, b, c, d):
		for i in (sel[0], sel[1], a, b, c, d):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.MUX(
			sel[1],
			self.MUX(sel[0], a, b),
			self.MUX(sel[0], c, d)
		)

	def MUX8W(self, sel, a, b, c, d, e, f, g, h):
		for i in (sel[0], sel[1], sel[2], a, b, c, d, e, f, g, h):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.MUX(
			sel[2],
			self.MUX4W([sel[0], sel[1]], a, b, c, d),
			self.MUX4W([sel[0], sel[1]], e, f, g, h)
		)

	def DEMUX(self, sel, inp):
		for i in (sel, inp):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		return self.AND(
			inp,
			self.NOT(sel)
		), self.AND(inp, sel)

	def DEMUX4W(self, sel, inp):
		for i in (sel[0], sel[1], inp):
			if i not in (0, 1):
				raise AttributeError('Invalid value')
		tmp = self.DEMUX(sel[1], inp)
		return self.DEMUX(sel[0], tmp[0]) + self.DEMUX(sel[0], tmp[1])
		
	def DEMUX8W(self, sel, inp):
		for i in (sel[0], sel[1], sel[2], inp):
			if i not in (0, 1):
				raise AttributeError('Invalid value')

		tmp = self.DEMUX(sel[2], inp)
		return self.DEMUX4W([sel[0], sel[1]], tmp[0]) + self.DEMUX4W([sel[0], sel[1]], tmp[1])