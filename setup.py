# Copyright (C) 2025 Warren Usui, MIT License
"""
Chess problem solver -- data input module
"""
from check_moves import find_checks

def _fen_to_board(fen_data):
    """
    Read a board as defined in the first string in FEN-notation
    and translate into an 8x8 grid representation of the board.
    """
    def handle_line(line_data):
        def mk_spcs(val):
            if val.isdigit():
                return '........'[0:int(val)]
            return val
        return ''.join(list(map(mk_spcs, list(line_data[1]))))
    return list(map(handle_line, enumerate(fen_data.split('/'))))[::-1]

def setup_pieces(problem):
    """
    Read a problem, format data, set extra values.

    Input:
        problem -- String of three colon separated fields
            - Name of the problem
            - Layout of the board (FEN-notation of board layout)
            - Number of moves needed (mate in N problem)

    Output:
        dict containing the following fields
            - name: Problem name (first field of input)
            - board: 8x8 representation of the board.
            - num_moves: half moves requited before mate
            - ep_square: empty list at start of problem.  Contains square
                         passed over by previous move (value entered if
                         previous move was an initial two square pawn move)>
                         This notation is similar to what FEN notation uses.
            - cst_status: Castling Status.  Same as in FEN notation.
                         Note that this is set at the beginning of the
                         problem if the rooks and kings are in the right
                         locations.  It can only change from allowed to
                         not allowed.
            - checks: Locations of pieces delivering checks in the board
                         formation given.  List of two lists of squares
                         that the king is being attacked from.
    """
    def sp_inner(prob):
        def sp_havep(board):
            def start_can_castle(kvalue):
                def scc_kv(krow):
                    def scc_rvs(column):
                        def scc_chk(rvalue):
                            if board[krow][column] == rvalue:
                                return rvalue
                            return '-'
                        return scc_chk({'K': 'R', 'k': 'r'}[kvalue])
                    if board[krow][4] != kvalue:
                        return '--'
                    return ''.join(list(map(scc_rvs, [0, 7])))
                return scc_kv({'K': 0, 'k': 7}[kvalue])
            return {'name': prob[0], 'board': board,
                'num_moves': int(prob[2]) * 2 - 1, 'ep_square': [],
                'cst_status': ''.join(list(map(start_can_castle,
                                               ['K', 'k']))),
                'checks': [find_checks({'board': board, 'kloc': 'K'}),
                           find_checks({'board': board, 'kloc': 'k'})]}
        return sp_havep(_fen_to_board(prob[1]))
    return sp_inner(problem.split(':'))
