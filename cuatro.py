#! /usr/bin/env python
# coding: utf-8

## FEATURES:
	# - Partida individual:
	# 	- CPU con defensa inteligente (horizontal, vertical y diagonales)
	# - Partida multijugador
	# - Comprobacion de victoria en horizontal, vertical y diagonal
## TO DO:
	# - Ataque inteligente

from random import randint
from os import system

## Constantes y variables de configuracion
TITLE = "Conecta 4"
EMPTY_SYMBOL = "-"
ALLOWED_SYMBOLS = "@", "#", "X", "O"
DEFAULT_ROWS = 6
DEFAULT_COLS = 7

def quitAllowedSymbol(symbol):
	global ALLOWED_SYMBOLS
	res = ()
	for element in ALLOWED_SYMBOLS:
		if element != symbol:
			res = res + (element,)
	ALLOWED_SYMBOLS = res

def isNumber(value):
	try:
		int(value)
		return True

	except ValueError:
		return False

##################################################################################################

class Player(object):


	def __init__(self, name, symbol = False):
		self._name = name
		if not symbol:
			self.selectSymbol()
		elif symbol not in ALLOWED_SYMBOLS:
			print "ERROR: Simbolo elegido para jugador no permitido"
			raise ValueError	
		else:
			self._symbol = symbol


	@property
	def name(self):
	    return str(self._name)
	
	@property
	def symbol(self):
	    return str(self._symbol)

	def selectSymbol(self):
		self._symbol = ALLOWED_SYMBOLS[0]
		quitAllowedSymbol(self._symbol)

	def move(self):
		raise NotImplementedError("ERROR: El metodo move debe ser implementado en todas las subclases de  Player")
		

###################################################################################################

class HumanPlayer(Player):

	def __init__(self, name = "Jugador 1", symbol = False):
		Player.__init__(self, name, symbol)
		
	def selectSymbol(self):
		print self.name
		symbol = raw_input("Elige un simbolo con el que jugar: {0} ".format(ALLOWED_SYMBOLS))

		if symbol not in ALLOWED_SYMBOLS:
			print("ERROR: Simbolo introducido no contemplado entre los permitidos")
			self.selectSymbol()
		else:
			self._symbol = symbol
			quitAllowedSymbol(symbol)

	def move(self, board):
		print self._name
		col = raw_input("Introduce ficha: columnas 1 a {} ... ".format(board.cols))

		if isNumber(col):
			col = int(col) - 1
			if col in range(0, board.cols) and board.hasSpace(col):
				return board.insertChip(self._symbol, col)

		print "ERROR: El valor introducido debe ser un entero en el rango indicado"
		return self.move(board)		

######################################################################################################

class CpuPlayer(Player):

	def __init__(self, checker, enemySymbol, symbol = False, dangerNum = 2):
		Player.__init__(self, "CPU", symbol)
		self._checker = checker
		self._enemySymbol = enemySymbol
		self._dangerNum = dangerNum

	def move(self, board, lastRow, lastCol):
		theresDanger, sinceTo = self._checker.checkHorizontal(self._enemySymbol, lastRow, lastCol, self._dangerNum)
		if theresDanger:
			done, lastMovement = self._defendRowIfHaveTo(board, sinceTo[0], sinceTo[1])
			if done:
				return lastMovement

		theresDanger, sinceTo = self._checker.checkVertical(self._enemySymbol, lastRow, lastCol, self._dangerNum)
		if theresDanger:
			done, lastMovement = self._defendColumnIfHaveTo(board, sinceTo[0], sinceTo[1])
			if done:
				return lastMovement

		theresDanger, sinceTo = self._checker.checkDescDiag(self._enemySymbol, lastRow, lastCol, self._dangerNum)
		if theresDanger:
			done, lastMovement = self._defendDescDiagIfHaveTo(board, sinceTo[0], sinceTo[1])
			if done:
				return lastMovement

		theresDanger, sinceTo = self._checker.checkAscDiag(self._enemySymbol, lastRow, lastCol, self._dangerNum)
		if theresDanger:
			done, lastMovement = self._defendAscDiagIfHaveTo(board, sinceTo[0], sinceTo[1])
			if done:
				return lastMovement
			
		return board.insertChip(self._symbol, self._selectRandomColumn(board))

	def _defendRowIfHaveTo(self, board, since, to):
		if self._checker.canConnect4InHorizontal(since, to):
			leftPos = since[0], since[1]-1
			rightPos = to[0], to[1]+1
			if board.canInsertOn(leftPos[0], leftPos[1]):
				return True, board.insertChip(self._symbol, leftPos[1]);
			elif board.canInsertOn(rightPos[0], rightPos[1]):
				return True, board.insertChip(self._symbol, rightPos[1])

		return False, False

	def _defendColumnIfHaveTo(self, board, since, to):
		if self._checker.canConnect4InVertical(since, to):
			upPos = since[0]-1, since[1]
			if board.canInsertOn(upPos[0], upPos[1]):
				return True, board.insertChip(self._symbol, upPos[1])

		return False, False

	def _defendDescDiagIfHaveTo(self, board, since, to):
		if self._checker.canConnect4InDescDiag(since, to): 
			upPos = since[0]-1, since[1]-1
			downPos = to[0]+1, to[1]+1
			if board.canInsertOn(upPos[0], upPos[1]): 
				return True, board.insertChip(self._symbol, upPos[1]);
			elif board.canInsertOn(downPos[0], downPos[1]):
				return True, board.insertChip(self._symbol, downPos[1])

		return False, False

	def _defendAscDiagIfHaveTo(self, board, since, to):
		if self._checker.canConnect4InAscDiag(since, to): 
			downPos = since[0]+1, since[1]-1
			upPos = to[0]-1, to[1]+1
			if board.canInsertOn(downPos[0], downPos[1]):
				return True, board.insertChip(self._symbol, downPos[1])
			elif board.canInsertOn(upPos[0], upPos[1]): 
				return True, board.insertChip(self._symbol, upPos[1]);

		return False, False


	def _selectRandomColumn(self, board):
		fits = False

		while not fits:
			col = randint(0, board.cols);
			fits = col in range(0, board.cols) and board.hasSpace(col)

		return col

######################################################################################################

class Board():

	def __init__(self, rows = DEFAULT_ROWS, cols = DEFAULT_COLS, emptySymbol = EMPTY_SYMBOL):
		self._rows = rows
		self._cols = cols
		self._map = [[emptySymbol]*cols for row in range(rows)]
		self._emptySymbol = emptySymbol

	def __str__(self):
		result = ""

		for row in self._map:
			result += "\n"
			for col in row:
				result += "| {0} ".format(col)
			result += "|"

		result += "\n"

		for num in range(1, self._cols + 1):
			result += "  {0} ".format(num)
		return result + "\n"

	@property
	def rows(self):
	    return self._rows

	@property
	def cols(self):
	    return self._cols

	@property
	def emptySymbol(self):
	    return self._emptySymbol

	def insertChip(self, symbol, col):
		for row in range(self._rows -1, -1, -1):
			if self._map[row][col] == self._emptySymbol:
				self._map[row][col] = symbol
				return row, col
	
	def hasSpace(self, col):
		return self._map[0][col] == self._emptySymbol	

	def canInsertOn(self, row, col):
		cellExists = row in range(0, self._rows) and col in range(0, self._cols)
		if cellExists:
			isEmpty = self._map[row][col] == self.emptySymbol
			isReachable = row == self._rows-1 or self._map[row+1][col] != self.emptySymbol
			if isEmpty and isReachable:
				return True

		return False

######################################################################################################

class Game():

	def __init__(self):
		system("clear")
		print "### {} ###".format(TITLE.upper())
		self._board = Board()
		self._checker = Checker(self._board)
		self._selectType()		
		system("clear")
		print "TU {} VS. CPU {}".format(self._playerOne.symbol, self._playerTwo.symbol)

	def _selectType(self):
		option = 0
		print "Elije el tipo de partida:\n1. Un solo jugador (Jugador Vs. CPU)"
		print "2. Multijugador (Jugador 1 Vs. Jugador2 )"
		
		while option not in ("1", "2"):
			option = raw_input("... ")

		self._playerOne = HumanPlayer(name = "Jugador 1")
		if int(option) == 1:
			self._playerTwo = CpuPlayer(self._checker, self._playerOne.symbol, "@")
		else:
			self._playerTwo = HumanPlayer(name = "Jugador 2")

	def run(self):
		winner = False
		row = col = False, False
		print self._board

		while True:
			row, col = self._playerOne.move(self._board)
			system("clear")
			print "JUGADOR 1 mueve"
			print self._board
			if self._checker.isWinMovement(self._playerOne.symbol, row, col):
				winner = self._playerOne
				break

			if isinstance(self._playerTwo, CpuPlayer):
				row, col = self._playerTwo.move(self._board, row, col)
			else:
				row, col = self._playerTwo.move(self._board)
			print "{} mueve".format(self._playerTwo.name if self._playerTwo.name is not None else "CPU")
			print self._board
			if self._checker.isWinMovement(self._playerTwo.symbol, row, col):
				winner = self._playerTwo
				break

		self._end(winner)

	def _end(self, winner = False):
		print "{} ha ganado!!!".format(winner.name if winner.name is not None else "CPU")

######################################################################################################

class Checker():

	def __init__(self, board):
		self._board = board

	def isWinMovement(self, symbol, row, col, maxNum = 4):
		horizontal = self.checkHorizontal(symbol, row, col, maxNum)[0]
		vertical = self.checkVertical(symbol, row, col, maxNum)[0]
		descDiagonal = self.checkDescDiag(symbol, row, col, maxNum)[0]
		ascDiagonal = self.checkAscDiag(symbol, row, col, maxNum)[0]

		return horizontal or vertical or descDiagonal or ascDiagonal

	def checkHorizontal(self, symbol, row, col, maxNum):
		counter = 1
		since = to = row, col
		ret = brokenAtLeft = brokenAtRight = False

		if not brokenAtLeft and not brokenAtRight:

			for i in range(1, 4):
				if col-i >= 0 and not brokenAtLeft:
					if self._board._map[row][col-i] == symbol:
						counter += 1
						since = row, col-i
					else:
						brokenAtLeft = True
				if col+i < self._board.cols and not brokenAtRight:
					if self._board._map[row][col+i] == symbol:
						counter += 1
						to = row, col+i
					else:
						brokenAtRight = True

				if counter >= maxNum:
					ret = True

		return ret, (since, to)

	def checkVertical(self, symbol, row, col, maxNum):
		counter = 1
		since = to = row, col
		ret = brokenUp = brokenDown = False

		if not brokenUp and not brokenDown:
			for i in range(1, 4):
				if row-i >= 0 and not brokenUp:
					if self._board._map[row-i][col] == symbol:
						counter += 1
						since = row-i, col
					else:
						brokenUp = True
				if row+i < self._board.rows and not brokenDown:
					if self._board._map[row+i][col] == symbol:
						counter += 1
						to = row+i, col
					else:
						brokenDown = True

				if counter >= maxNum:
					ret = True
		return ret, (since, to)

	def checkDescDiag(self, symbol, row, col, maxNum):
		counter = 1
		since = to = row, col
		ret = brokenUp = brokenDown = False

		if not brokenUp and not brokenDown:

			for i in range(1, 4):
				if row-i >=	 0 and col-i >= 0 and not brokenUp:
					if self._board._map[row-i][col-i] == symbol:
						counter += 1
						since = row-i, col-i
					else:
						brokenUp = True
				if row+i < self._board.rows and col+i < self._board.cols and not brokenDown:
					if self._board._map[row+i][col+i] == symbol:
						counter += 1
						to = row+i, col+i
					else:
						brokenAtDown = True

				if counter >= maxNum:
					ret = True

		return ret, (since, to)

	def checkAscDiag(self, symbol, row, col, maxNum):
		counter = 1
		since = to = row, col
		ret = brokenUp = brokenDown = False

		if not brokenUp and not brokenDown:

			for i in range(1, 4):
				if row+i < self._board.rows and col-i >= 0 and not brokenDown:
					if self._board._map[row+i][col-i] == symbol:
						counter += 1
						since = row+i, col-i
					else:
						brokenDown = True
				if row-i >= 0 and col+i < self._board.cols and not brokenUp:
					if self._board._map[row-i][col+i] == symbol:
						counter += 1
						to = row-i, col+i
					else:
						brokenAtDown = True

				if counter >= maxNum:
					ret = True

		return ret, (since, to)

	def canConnect4InHorizontal(self, since, to):		
		quant = to[1] - since[1]
		counter = 0
		brokenAtLeft = brokenAtRight = False

		for i in range(0, quant):
			if since[1]-i >= 0:
				if self._board._map[since[0]][since[1]-i] != self._board.emptySymbol and not brokenAtLeft:
					counter += 1
				else:
					brokenAtLeft = True
			if to[1]+i	< self._board.cols:
				if self._board._map[to[0]][to[1]+i] != self._board.emptySymbol and not brokenAtRight:
					counter += 1
				else:
					brokenAtRight = True

			if counter >= quant:
				return True

		return False
		
	def canConnect4InVertical(self, since, to):		
		quant = to[0] - since[0]
		counter = 0
		brokenUp = brokenDown = False

		for i in range(0, quant):
			if since[0]-i >= 0:
				if self._board._map[since[0]-i][since[1]] != self._board.emptySymbol and not brokenUp:
					counter += 1
				else:
					brokenUp = True
			## DOWN USEFUL?
			if to[0]+i	< self._board.rows:
				if self._board._map[to[0]+i][to[1]] != self._board.emptySymbol and not brokenDown:
					counter += 1
				else:
					brokenDown = True

			if counter >= quant:
				return True

		return False	

	def canConnect4InDescDiag(self, since, to):		
		quant = to[0] - since[0]
		counter = 0
		brokenUp = brokenDown = False

		for i in range(0, quant):
			if since[0]-i >= 0 and since[1]-i >= 0:
				if self._board._map[since[0]-i][since[1]-i] != self._board.emptySymbol and not brokenUp:
					counter += 1
				else:
					brokenUp = True
			if to[0]+i	< self._board.rows and to[1]+i < self._board.cols:
				if self._board._map[to[0]+i][to[1]+i] != self._board.emptySymbol and not brokenDown:
					counter += 1
				else:
					brokenDown = True

			if counter >= quant:
				return True

		return False

	def canConnect4InAscDiag(self, since, to):		
		quant = since[0] - to[0]
		counter = 0
		brokenUp = brokenDown = False

		for i in range(0, quant):
			if since[0]+i < self._board.rows and since[1]-i >= 0:
				if self._board._map[since[0]+i][since[1]-i] != self._board.emptySymbol and not brokenUp:
					counter += 1
				else:
					brokenUp = True
			if to[0]-i	>= 0 and to[1]+i < self._board.cols:
				if self._board._map[to[0]-i][to[1]+i] != self._board.emptySymbol and not brokenDown:
					counter += 1
				else:
					brokenDown = True

			if counter >= quant:
				return True

		return False

######################################################################################################

thisGame = Game()
thisGame.run()