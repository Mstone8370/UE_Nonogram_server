"""
code from: https://rosettacode.org/wiki/Nonogram_solver#Python_3
and modified for app's purpose
"""

from functools import reduce

def gen_row_deprecated(width, line_info):
    """Create all patterns of a row or col that match given runs."""
    def gen_seg(hints, remaining_space):
        if not hints:
            return [[2] * remaining_space]
        return [[2] * x + hints[0] + tail
                for x in range(1, remaining_space - len(hints) + 2)
                for tail in gen_seg(hints[1:], remaining_space - x)]
    
    if line_info == [0]:
        return [[2] * width]
    else:
        return [x[1:] for x in gen_seg([[1] * i for i in line_info], width + 1 - sum(line_info))]

def gen_row(width, line_info):
    """Create all patterns of a row or col that match given runs."""
    def gen_seg(hints, remaining_space):
        if not hints or hints == [[]]:
            return [[2] * remaining_space]
        
        result = []
        for x in range(1, remaining_space - len(hints) + 2):
            for tail in gen_seg(hints[1:], remaining_space - x):
                result.append([2] * x + hints[0] + tail)
        return result

    result = []
    for x in gen_seg([[1] * i for i in line_info], width + 1 - sum(line_info)): # [1, 3] --> [[1], [1, 1, 1]], [0] -> [[]]
        result.append(x[1:])
    return result

 
 
def deduce(horizontal_runs, vertical_runs, bf_search=False):
    """Fix inevitable value of cells, and propagate."""
    def allowable(row):
        return reduce(lambda a, b: [x | y for x, y in zip(a, b)], row)
 
    def fits(a, b):
        return all(x & y for x, y in zip(a, b))
 
    def fix_col(n):
        """See if any value in a given column is fixed;
        if so, mark its corresponding row for future fixup."""
        c = [x[n] for x in can_do]
        cols[n] = [x for x in cols[n] if fits(x, c)]
        for i, x in enumerate(allowable(cols[n])):
            if x != can_do[i][n]:
                mod_rows.add(i)
                can_do[i][n] = x
 
    def fix_row(n):
        """Ditto, for rows."""
        c = can_do[n]
        rows[n] = [x for x in rows[n] if fits(x, c)]
        for i, x in enumerate(allowable(rows[n])):
            if x != can_do[n][i]:
                mod_cols.add(i)
                can_do[n][i] = x
 
    def show_gram(m):
        # If there's 'x', something is wrong.
        # If there's '?', needs more work.
        for x in m:
            print(" ".join("x#.?"[i] for i in x))
        print()
 
    width, height = len(vertical_runs), len(horizontal_runs)
    rows = [gen_row(width, x) for x in horizontal_runs]
    cols = [gen_row(height, x) for x in vertical_runs]
    can_do = list(map(allowable, rows))
 
    # Initially mark all columns for update.
    mod_rows, mod_cols = set(), set(range(width))
 
    while mod_cols:
        for i in mod_cols:
            fix_col(i)
        mod_cols = set()
        for i in mod_rows:
            fix_row(i)
        mod_rows = set()

    n = 0
    if any(0 in row for row in can_do):
        print("Something's wrong")
    elif all(can_do[i][j] in (1, 2) for j in range(width) for i in range(height)):
        print("Solution would be unique")  # but could be incorrect!
        n = 1
    else:
        print("Solution may not be unique")
        n = 2

    if bf_search:
        # We actually do exhaustive search anyway. Unique solution takes
        # no time in this phase anyway, but just in case there's no
        # solution (could happen?).
        out = [0] * height
    
        def try_all(n = 0):
            if n >= height:
                for j in range(width):
                    if [x[j] for x in out] not in cols[j]:
                        return 0
                show_gram(out)
                return 1
            sol = 0
            for x in rows[n]:
                out[n] = x
                sol += try_all(n + 1)
                if sol > 1:
                    break
            return sol

        n = try_all()
    else:
        show_gram(can_do)
    return (n, [str(x) + "|" + str(y) for x in range(len(can_do[0])) for y in range(len(can_do)) if can_do[y][x] == 3])
 
 
def solve(p, show_runs=True, bf_search=False):
    s = [
            [
                [
                  ord(c) - ord('A') if ord(c) < ord('a') else ord(c) - 71 # ord(c) - ord('A') - (ord('a') - ord('Z') - 1)
                  for c in w
                ]
                for w in l.split(';')
            ]
            for l in p.split('|')
        ]
    if show_runs:
        print("Horizontal runs:", s[0])
        print("Vertical runs:", s[1])
    n = 0
    result = [[]]
    try:
        n, result = deduce(s[0], s[1], bf_search)
    except Exception:
        pass
    
    if not n:
        print("No solution.")
    elif n == 1:
        print("Unique solution.")
    else:
        print(n, "solutions.")
    print()

    ret = {}
    ret["num"] = n
    ret["ambiguous"] = result
    return ret
