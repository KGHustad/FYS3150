from common import *
import tabulate

table_format = 'simple'
if '--latex' in sys.argv:
    table_format = 'latex'
elif '--markdown' in sys.argv:
    table_format = 'pipe'

n_values = [1000*2**i for i in xrange(4)]
iterations = 100
kappa = 0.1
data = np.zeros((len(n_values), 3))
for i, n in enumerate(n_values):
    v_original = np.random.random((n, n))

    data[i, 0] = n

    v = v_original.copy()
    data[i, 1] = diffusion_2d(v, iterations, kappa, omp=False, silent=True)

    v = v_original.copy()
    data[i, 2] = diffusion_2d(v, iterations, kappa, omp=True, silent=True)


headers = ['n', 'Serial', 'OpenMP']
if table_format == 'latex':
    headers = ['$n$', 'Serial', 'OpenMP']

print tabulate.tabulate(data, headers, floatfmt='.1E', tablefmt=table_format)
