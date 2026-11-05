"""Independently verify documented exercises and selected formula identities.

This script uses SymPy and is not a proof of convergence, hypotheses, or the
complete collection of university-math theorems.
"""
import math
import sympy as s

x = s.symbols('x', real=True)
xp = s.symbols('xp', positive=True)
a, alpha = s.symbols('a alpha', positive=True)

# Verify the derivative table by symbolic differentiation (on the stated domains).
derivatives = [
    (s.Integer(3), 0, x), (xp**alpha, alpha*xp**(alpha-1), xp),
    (s.exp(x), s.exp(x), x), (a**x, a**x*s.log(a), x),
    (s.log(xp), 1/xp, xp), (s.sin(x), s.cos(x), x),
    (s.cos(x), -s.sin(x), x), (s.tan(x), 1/s.cos(x)**2, x),
    (s.cot(x), -1/s.sin(x)**2, x),
    (s.asin(x), 1/s.sqrt(1-x*x), x),
    (s.acos(x), -1/s.sqrt(1-x*x), x),
    (s.atan(x), 1/(1+x*x), x),
]
for f, answer, variable in derivatives:
    assert s.trigsimp(s.simplify(s.diff(f, variable)-answer)) == 0, (f, answer)

# Each listed primitive is checked by differentiation.
primitives = [
    (xp**(alpha+1)/(alpha+1), xp**alpha, xp),
    (s.log(xp), 1/xp, xp), (s.exp(x), s.exp(x), x),
    (a**x/s.log(a), a**x, x), (-s.cos(x), s.sin(x), x),
    (s.sin(x), s.cos(x), x), (s.tan(x), 1/s.cos(x)**2, x),
    (-s.cot(x), 1/s.sin(x)**2, x),
    (s.atan(x), 1/(1+x*x), x), (s.asin(x), 1/s.sqrt(1-x*x), x),
]
for primitive, integrand, variable in primitives:
    assert s.trigsimp(s.simplify(s.diff(primitive, variable)-integrand)) == 0

# Check coefficients in the finite Taylor expansions independently.
assert s.series(s.exp(x), x, 0, 4).removeO() == 1+x+x**2/2+x**3/6
assert s.series(s.sin(x), x, 0, 4).removeO() == x-x**3/6
assert s.series(s.cos(x), x, 0, 5).removeO() == 1-x**2/2+x**4/24
assert s.series(s.log(1+x), x, 0, 4).removeO() == x-x**2/2+x**3/3
assert s.expand(s.series((1+x)**alpha, x, 0, 3).removeO()-(1+alpha*x+alpha*(alpha-1)*x**2/2)) == 0

# Linear algebra: all four numbered legacy exercises.
A = s.Matrix([[1, 2], [2, 4]])
assert A.rank() == 1 and A*s.Matrix([-2, 1]) == s.zeros(2, 1)
u, b = s.Matrix([1, 1]), s.Matrix([3, 1])
projection = (u.dot(b)/u.dot(u))*u
assert projection == s.Matrix([2, 2]) and u.dot(b-projection) == 0
D = s.diag(2, -1)
assert D.eigenvals() == {s.Integer(2): 1, s.Integer(-1): 1}
assert (s.Matrix([1, 0]).T*D*s.Matrix([1, 0]))[0] > 0
assert (s.Matrix([0, 1]).T*D*s.Matrix([0, 1]))[0] < 0
design = s.Matrix([[1, 0], [1, 1], [1, 2]])
obs = s.Matrix([1, 2, 2])
beta = (design.T*design).inv()*design.T*obs
assert beta == s.Matrix([s.Rational(7, 6), s.Rational(1, 2)])
assert design.T*(design*beta-obs) == s.zeros(2, 1)
M = s.Matrix([[1, 0], [0, 0]])
N = s.Matrix([[0, 1], [0, 0]])
assert M*N == N and N*M == s.zeros(2)
a1,b1,c1,d1 = s.symbols('a1 b1 c1 d1')
Q = s.Matrix([[a1,b1],[c1,d1]])
assert Q*s.Matrix([[d1,-b1],[-c1,a1]]) == Q.det()*s.eye(2)
assert (M*N).T == N.T*M.T
P = s.Matrix([[1, 1], [0, 1]])
E = s.diag(2, 3)
similar = P.inv()*E*P
assert similar.trace() == E.trace() and similar.det() == E.det()
assert similar.charpoly().as_expr() == E.charpoly().as_expr()
rank_one = s.Matrix([[1, 1]])
proj = rank_one.T*(rank_one*rank_one.T).inv()*rank_one
assert proj*proj == proj and proj.T == proj
svd_A = s.diag(3, 1)
svd_B = s.diag(3, 0)
assert sum(z*z for z in svd_A-svd_B) == 1

# Probability/statistics: all six numbered legacy exercises.
assert s.Rational(1, 4)/s.Rational(3, 4) == s.Rational(1, 3)
assert 10*s.Rational(3, 10) == 3
assert 10*s.Rational(3, 10)*s.Rational(7, 10) == s.Rational(21, 10)
assert s.integrate(2*s.exp(-2*x), (x, 1, s.oo)) == s.exp(-2)
assert s.sqrt(s.Rational(9, 100)) == s.Rational(3, 10)
assert 10-s.Rational(196,100)*s.Rational(2,10) == s.Rational(9608,1000)
assert 10+s.Rational(196,100)*s.Rational(2,10) == s.Rational(10392,1000)
assert (1+10, 1+5) == (11, 6) and s.Rational(11,17) != s.Rational(10,15)

# Cross-check representative moments and normalization in the new derivations.
z = s.symbols('z', real=True)
lam = s.symbols('lam', positive=True)
k = s.symbols('k', integer=True, nonnegative=True)
assert s.summation(s.exp(-lam)*lam**k/s.factorial(k), (k, 0, s.oo)) == 1
assert s.simplify(s.summation(k*s.exp(-lam)*lam**k/s.factorial(k), (k, 0, s.oo))-lam) == 0
assert s.integrate(lam*s.exp(-lam*xp), (xp, 0, s.oo)) == 1
assert s.integrate(xp*lam*s.exp(-lam*xp), (xp, 0, s.oo)) == 1/lam
assert s.integrate(z*z*s.exp(-z*z/2)/s.sqrt(2*s.pi), (z, -s.oo, s.oo)) == 1
assert s.Rational(2, 5)*s.Rational(3, 5)*2*s.Rational(3, 4) == s.Rational(9, 25)
Nsym, Msym = s.symbols('Nsym Msym', positive=True, integer=True)
p = Msym/Nsym
assert s.simplify(Msym*(Msym-1)/(Nsym*(Nsym-1))-p*p+p*(1-p)/(Nsym-1)) == 0
# Check the normal likelihood stationary variance and regression covariance.
v,n,S = s.symbols('v n S', positive=True)
ll = -n*s.log(v)/2-S/(2*v)
assert s.solve(s.diff(ll,v),v) == [S/n]
K = (design.T*design).inv()*design.T
assert s.simplify(K*K.T-(design.T*design).inv()) == s.zeros(2)

# Separately recompute the selected inline legacy examples listed in the notes.
assert s.limit((x*x-1)/(x-1), x, 1) == 2
assert s.diff((3*x+1)**2, x).subs(x, 1) == 24
Pvar = s.symbols('Pvar', positive=True)
assert s.expand(x*(Pvar/2-x)-(Pvar**2/16-(x-Pvar/4)**2)) == 0
assert s.integrate(x, (x,0,2)) == 2
assert s.integrate(-x, (x,0,2)) == -2
assert (s.Matrix([4,6,3])-s.Matrix([1,2,3])).norm() == 5
assert s.integrate(s.Matrix([1,0]).dot(s.Matrix([2,0])), (x,0,1)) == 2
assert s.Matrix([[1,2],[0,1]])*s.Matrix([3,4]) == s.Matrix([11,4])
c = s.symbols('c', real=True)
assert s.expand(sum((c-i)**2 for i in (1,2,3))-(3*(c-2)**2+2)) == 0
samples = s.Matrix([[1,1],[-1,-1]])
cov = samples.T*samples/(samples.rows-1)
assert cov == s.Matrix([[2,2],[2,2]])
assert cov*s.Matrix([1,1]) == 4*s.Matrix([1,1])
assert cov*s.Matrix([1,-1]) == s.zeros(2,1)
assert s.Rational(9,1000)/(s.Rational(9,1000)+s.Rational(99,100)*s.Rational(5,100)) == s.Rational(2,13)
assert s.binomial(3,2)/2**3 == s.Rational(3,8)
assert s.integrate(1/(2*s.sqrt(x)),(x,0,1)) == 1
assert s.sqrt(s.Rational(1,1600)) == s.Rational(1,40)
assert 50-s.Rational(196,100)*s.Rational(2,10) == s.Rational(49608,1000)
assert 50+s.Rational(196,100)*s.Rational(2,10) == s.Rational(50392,1000)
assert s.Rational(8,8+4) == s.Rational(2,3)

# Independent algebraic checks for the newer proof steps.
R = s.symbols('R', positive=True)
assert s.simplify(s.diff(-s.cos(R)/R, R) - (s.sin(R)/R+s.cos(R)/R**2)) == 0
rr1, rr2 = s.symbols('rr1 rr2', real=True)
assert s.simplify(s.det(s.Matrix([[s.exp(rr1*x), s.exp(rr2*x)],
                                [rr1*s.exp(rr1*x), rr2*s.exp(rr2*x)]]))
                  -(rr2-rr1)*s.exp((rr1+rr2)*x)) == 0
rr = s.symbols('rr', real=True)
assert s.simplify(s.det(s.Matrix([[s.exp(rr*x), x*s.exp(rr*x)],
                                [s.diff(s.exp(rr*x),x), s.diff(x*s.exp(rr*x),x)]]))
                  -s.exp(2*rr*x)) == 0
aa, bb, cc = s.symbols('aa bb cc', real=True, nonzero=True)
low = s.Matrix([[1, 0], [bb/aa, 1]])
assert s.simplify(low*s.diag(aa, cc-bb**2/aa)*low.T-s.Matrix([[aa,bb],[bb,cc]])) == s.zeros(2)
ha, hb, hc = s.symbols('ha hb hc', positive=True)
semiperimeter = (ha+hb+hc)/2
assert s.expand(4*ha**2*hb**2-(ha**2+hb**2-hc**2)**2
                -16*semiperimeter*(semiperimeter-ha)*(semiperimeter-hb)*(semiperimeter-hc)) == 0
rho, phi, theta = s.symbols('rho phi theta', real=True)
spherical = s.Matrix([rho*s.sin(phi)*s.cos(theta), rho*s.sin(phi)*s.sin(theta), rho*s.cos(phi)])
assert s.trigsimp(spherical.jacobian([rho,phi,theta]).det()) == rho**2*s.sin(phi)
for standard_deviations, rounded in [(1, 0.68), (2, 0.95), (3, 0.997)]:
    assert abs(math.erf(standard_deviations / math.sqrt(2)) - rounded) < 0.005
# PCA counterexample: high-variance first coordinate is independent of label.
counterexample = s.Matrix([[10, 1], [10, -1], [-10, 1], [-10, -1]])
assert counterexample.T * counterexample == s.diag(400, 4)
assert {(row[0], row[1]) for row in counterexample.tolist()} == {
    (10, 1), (10, -1), (-10, 1), (-10, -1)
}

print(f'Checked {len(derivatives)} derivative identities, {len(primitives)} primitives, all 10 numbered linear/probability exercises, and selected distribution moments.')
print('Also checked selected inline examples, including PCA, elementary limits, integrals and probability calculations.')
print('Symbolic checks do not replace proofs of the stated analytic and probabilistic assumptions.')
