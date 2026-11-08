"""Selected algebra behind the written-proof corrections; not a proof checker."""
import sympy as s

# A rank-deficient echelon matrix: multiplying only nonzero pivots is wrong.
A = s.diag(2, 0)
assert A.det() == 0 and 2 != A.det()

# Dependent leading columns still permit a complete, upper-trapezoidal QR.
A = s.Matrix([[1, 2, 0], [0, 0, 1], [0, 0, 0]])
Q = s.eye(3)
R = Q.T*A
assert Q.T*Q == s.eye(3) and Q*R == A
assert all(R[i, j] == 0 for i in range(3) for j in range(i))
assert R[1, 1] == 0 and A.rank() == 2

# Slice-integral derivations independently evaluate the claimed volumes.
z, h, u, v, radius = s.symbols('z h u v radius', positive=True)
assert s.simplify(s.integrate((u+(v-u)*z/h)**2, (z, 0, h))
                  - h*(u*u+u*v+v*v)/3) == 0
assert s.integrate(s.pi*(radius**2-z**2), (z, -radius, radius)) == 4*s.pi*radius**3/3

# Hyperbola distance reconstruction uses y²=b²(x²/a²-1), c²=a²+b².
x, a, b, c = s.symbols('x a b c', real=True)
y2 = b*b*(x*x/(a*a)-1)
for sign in [-1, 1]:
    expr = s.expand((x+sign*c)**2+y2-(c*x/a+sign*a)**2)
    assert s.factor(expr.subs(c*c, a*a+b*b)) == 0
# Squared identities alone do not establish signs; the text requires x>=a>0.

# Full symbolic first-order contingency residual, including the cross term.
N, ai, bj = s.symbols('N ai bj', positive=True)
si, tj, Zij = s.symbols('si tj Zij', real=True)
ahat = ai+s.sqrt(ai/N)*si
bhat = bj+s.sqrt(bj/N)*tj
observed = N*ai*bj+s.sqrt(N*ai*bj)*Zij
residual = (observed-N*ahat*bhat)/s.sqrt(N*ai*bj)
assert s.simplify(residual-(Zij-s.sqrt(bj)*si-s.sqrt(ai)*tj-si*tj/s.sqrt(N))) == 0
print('Passed selected determinant, QR, volume, hyperbola and contingency algebra checks.')
print('Sign conditions, convergence, existence and external theorem dependencies require the written arguments.')
