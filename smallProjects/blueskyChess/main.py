import chess
import chess.engine
import chess.svg

import cairosvg

board = chess.Board()
# print(board)

# boardSvg = chess.svg.board(board)
# cairosvg.svg2png(bytestring=boardSvg, scale=4.0, write_to="test.png")

def intInput(prompt: str) -> int:
	textInput = input(prompt)

	while textInput.isdigit() != True:
		textInput = input(prompt)
	
	return int(textInput)

class BlueskyMoveSource:
	pass

class TerminalMoveSource:
	def __init__(self):
		pass

	def _getMovesInput(self):
		moveVoteDict = dict()
		
		moveVotingActing = True
		while moveVotingActing == True:
			moveInput = input('Enter move (\'STOP\' to end voting): ')

			if moveInput != 'STOP':
				numberOfVotes = intInput('Enter the number of votes for move: ')

				if moveInput in moveVoteDict:
					moveVoteDict[moveInput] += numberOfVotes
			else:
				moveVotingActing = False

	def getMoveVoteDict(self):
		self._getMovesInput()


class ChessMoveFeeder:
	pass

class CommunityChessGame:
	def __init__(self):
		pass

if __name__ == '__main__':
	terminalSource = TerminalMoveSource()
	terminalSource.getMoveVoteDict()