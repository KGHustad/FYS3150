from common import *

if __name__ == '__main__':
    if weave_imported:
        A = np.zeros((2, 2), dtype=np.float64)
        find_max_nondiagonal_symmetrical_weave(A)
    else:
        print "WARNING: Weave is not installed"
