"""Independently check selected foundation identities and boundary examples.

Passing this script does not mean every statement in the blog was reviewed.
"""
import sympy as s

x, a, b, c, d = s.symbols('x a b c d', real=True)
n = s.symbols('n', integer=True, positive=True)
k = s.symbols('k', integer=True, positive=True)

# Algebra, Heron, and polynomial sums are checked from expanded expressions.
assert s.expand((a+b)**3-(a**3+3*a*a*b+3*a*b*b+b**3)) == 0
assert s.expand((a+b)*(a*a-a*b+b*b)-(a**3+b**3)) == 0
assert s.expand(a*(x+b/(2*a))**2-(b*b-4*a*c)/(4*a)-(a*x*x+b*x+c)) == 0
assert s.simplify(s.summation(k*k, (k, 1, n))-n*(n+1)*(2*n+1)/6) == 0
assert s.simplify(s.summation(k**3, (k, 1, n))-(n*(n+1)/2)**2) == 0
semiperimeter = (a+b+c)/2
assert s.expand(4*a*a*b*b-(a*a+b*b-c*c)**2
                -16*semiperimeter*(semiperimeter-a)*(semiperimeter-b)*(semiperimeter-c)) == 0

# The sign change of f' alone does not control a discontinuous value at 0.
f = s.Piecewise((-100, s.Eq(x, 0)), (-s.Abs(x), True))
assert f.subs(x, 0) < f.subs(x, s.Rational(1, 10))
assert f.subs(x, 0) < f.subs(x, -s.Rational(1, 10))
assert s.diff(-x, x) == -1 and s.diff(x, x) == 1

# Trigonometric identities are tested symbolically rather than at a picture.
t, u = s.symbols('t u', real=True)
assert s.trigsimp(s.sin(t+u)-s.sin(t)*s.cos(u)-s.cos(t)*s.sin(u), method='fu') == 0
assert s.trigsimp(s.cos(t+u)-s.cos(t)*s.cos(u)+s.sin(t)*s.sin(u), method='fu') == 0
assert s.trigsimp(s.sin(t)*s.sin(u)-(s.cos(t-u)-s.cos(t+u))/2, method='fu') == 0

# Examples spanning geometry, regression, combinatorics and statistics.
assert s.sqrt((s.Rational(8, 3))**2 + 2**2) == s.Rational(10, 3)
assert s.sqrt((4-s.Rational(8, 3))**2 + 1) == s.Rational(5, 3)
ellipse_distance_sum = 2*s.sqrt(4**2+3**2)
assert ellipse_distance_sum == 10 and ellipse_distance_sum + 2*4 == 18
assert s.binomial(2, 1)*s.binomial(3, 1)/s.binomial(5, 2) == s.Rational(3, 5)
assert s.binomial(5, 3)*2**2 == 40
observations = [(1, 2), (2, 3), (3, 5)]
xbar = s.Rational(sum(i for i, _ in observations), len(observations))
ybar = s.Rational(sum(j for _, j in observations), len(observations))
slope = sum((i-xbar)*(j-ybar) for i, j in observations) / sum((i-xbar)**2 for i, _ in observations)
assert slope == s.Rational(3, 2) and ybar-slope*xbar == s.Rational(1, 3)
assert all(s.Rational(w, 100)/s.Rational(h, 100)**2 == bmi
           for h, w, bmi in [(160, 6400, 25), (170, 5780, 20), (175, 6125, 20), (180, 9720, 30)])

print('Checked selected foundation identities, boundary counterexamples, and worked examples.')
print('This is a limited regression check, not a complete proof or site-wide audit.')
