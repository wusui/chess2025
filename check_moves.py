# Copyright (C) 2025 Warren Usui, MIT License
"""
Chess problem solver -- check for checks
"""
from itertools import chain

def line_clear(lc_pkt):
    """
    Tests if all squares between two points are blank

    Input: lc_pkt is a dictionary containing the following:
        - board: 8x8 board representation
        - from: coordinates of the piece
        - to_sq: coordinates of the place piece is moving to

    Returns: True if all spaces between these points are blank,
             False if not.  Only applies to rows, columns, and diagonals
    """
    def lc_inner(diffs):
        def gen_list(indx):
            if diffs[indx] == 0:
                return (max([abs(diffs[0]), abs(diffs[1])]) - 1) * [
                        lc_pkt['from'][indx]]
            if diffs[indx] > 0:
                return list(range(lc_pkt['from'][indx] - 1,
                        lc_pkt['to_sq'][indx], -1))
            return list(range(lc_pkt['from'][indx] + 1,
                    lc_pkt['to_sq'][indx]))
        if 0 not in diffs and abs(diffs[0]) != abs(diffs[1]):
            return False
        if max([abs(diffs[0]), abs(diffs[1])]) < 2:
            return True
        return not list(filter(lambda a: lc_pkt['board'][a[0]][a[1]] != '.',
                        list(zip(gen_list(0), gen_list(1)))))
    return lc_inner([lc_pkt['from'][0] - lc_pkt['to_sq'][0],
                     lc_pkt['from'][1] - lc_pkt['to_sq'][1]])

def can_move(mv_pkt):
    """
    Test if an individual piece can move to the location specified

    Input paramaeter mv_pkt is a dictionary with the following values:
        - row: row number of attacking piece
        - col: column number of attacking piece
        - brd: layout of the board
        - to_sq: location of square being attacked

    Returns True if this piece can move there, False if it cannot
    """
    def cm_inner(brd):
        def is_orth():
            return (mv_pkt['to_sq'][1] == mv_pkt['col']) or (
                mv_pkt['to_sq'][0] == mv_pkt['row'])
        def on_diag():
            return abs(mv_pkt['to_sq'][1] - mv_pkt['col']
                   ) == abs(mv_pkt['to_sq'][0] - mv_pkt['row'])
        def cm_line_clear():
            return line_clear({'board': brd, 'from': [mv_pkt['row'],
                        mv_pkt['col']], 'to_sq': mv_pkt['to_sq']})
        def one_away():
            return abs(mv_pkt['to_sq'][1] - mv_pkt['col']) <= 1 and abs(
                        mv_pkt['to_sq'][0] - mv_pkt['row']) <= 1
        def nmove():
            def nmove_h(horz):
                def nmove_v(vert):
                    return (horz == 2 and vert == 1) or (
                            horz == 1 and vert == 2)
                return nmove_v(abs(mv_pkt['to_sq'][0] - mv_pkt['row']))
            return nmove_h(abs(mv_pkt['to_sq'][1] - mv_pkt['col']))
        def pwn_take(piece):
            return abs(mv_pkt['to_sq'][1] - mv_pkt['col']) == 1 and (
                    mv_pkt['row'] + {'P': 1, 'p': -1}[piece] ==
                    mv_pkt['to_sq'][0])
        def pcan_move(piece):
            if piece in 'RrQq' and is_orth() and cm_line_clear():
                return [mv_pkt['row'], mv_pkt['col']]
            if piece in 'BbQq' and on_diag() and cm_line_clear():
                return [mv_pkt['row'], mv_pkt['col']]
            if piece in 'Kk' and one_away():
                return [mv_pkt['row'], mv_pkt['col']]
            if piece in 'nN' and nmove():
                return [mv_pkt['row'], mv_pkt['col']]
            if piece in 'pP' and pwn_take(piece):
                return [mv_pkt['row'], mv_pkt['col']]
            return []
        if brd[mv_pkt['row']][mv_pkt['col']] == '.':
            return []
        if (brd[mv_pkt['row']][mv_pkt['col']].isupper() ==
                brd[mv_pkt['to_sq'][0]]
                [mv_pkt['to_sq'][1]].isupper()):
            return []
        return pcan_move(mv_pkt['brd'][mv_pkt['row']][mv_pkt['col']])
    return cm_inner(mv_pkt['brd'])

def find_checks(b_kloc):
    """
    Find checks on a board

    Input:
        b_kloc is a dictionary with the following values:
            - board: 8x8 representation of the board
            - kloc: Pieced to be checked (k or K)

    Returns:
        list containing piece locations that are checking king indicated
        by b_kloc['kloc']
    """
    def move_to(tinfo):
        def mt_row(row):
            def mt_col(col):
                return can_move({'row': row, 'col': col,
                            'brd': tinfo['board'],
                            'to_sq': tinfo['to_loc']})
            return list(map(mt_col, range(0, 8)))
        return list(chain.from_iterable(filter(lambda a: len(a) > 0,
                                  map(mt_row, range(0, 8)))))
    def find_sq(bk_data):
        def get_coord(number):
            return [number // 8, number % 8]
        return get_coord(''.join(bk_data['board']).find(bk_data['kloc']))
    return list(filter(lambda a: len(a) > 0,
                move_to({'board': b_kloc['board'],
                'to_loc': find_sq(b_kloc)})))
  
