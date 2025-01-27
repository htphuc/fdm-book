import odespy
import numpy as np
import sys
#import matplotlib.pyplot as plt
import scitools.std as plt

def f(s, t):
    u, v = s
    return np.array([v, -u])

def u_exact(t):
    return I*np.cos(w*t)

I = 1; V = 0; u0 = np.array([I, V])
w  = 1; T = 100
tol = float(sys.argv[1])
solver = odespy.DormandPrince(f, atol=tol, rtol=0.1*tol)

Nt = 1 # just one step - let scheme find its intermediate points
t_mesh = np.linspace(0, T, Nt+1)
t_fine = np.linspace(0, T, 10001)

solver.set_initial_condition(u0)
u, t = solver.solve(t_mesh)

# u and t will only consist of [I, u^Nt] and [0,T], i.e. 2 values 
# each, while solver.u_all and solver.t_all contain all computed 
# points. solver.u_all is a list with arrays, one array (with 2 
# values) for each point in time.
u_adaptive = np.array(solver.u_all)

# For comparison, we solve also with simple FDM method
Nt_simple = len(solver.t_all)   # get no of time steps from ad. meth.
t_simple = np.linspace(0, T, Nt_simple+1)   # create equal steps
dt = t_simple[1] - t_simple[0]          # constant time step
u_simple = np.zeros(Nt_simple+1)
u_simple[0] = I
u_simple[1] = u_simple[0] - 0.5*dt**2*w**2*u_simple[0]
for n in range(1, Nt_simple):
    u_simple[n+1] = 2*u_simple[n] - u_simple[n-1] - \
    dt**2*w**2*u_simple[n]

plt.plot(solver.t_all, u_adaptive[:,0], 'k-')
plt.hold('on')
plt.plot(t_simple, u_simple, 'r--')
plt.plot(t_fine, u_exact(t_fine), 'b-')
plt.legend(['tol=%.0E' % tol, 'u simple', 'exact'])
plt.savefig('tmp_odespy_adaptive.png')
plt.savefig('tmp_odespy_adaptive.pdf')
plt.show()

