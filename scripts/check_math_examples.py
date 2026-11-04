"""Independently check selected examples; install sympy to run this optional audit."""
import sympy as s

x = s.symbols('x', real=True)
assert s.solve(s.Eq((x-1)/2 + (x+1)/3, 3), x) == [s.Rational(19, 5)]
assert s.solve(s.Eq(2*x*x-3*x-2, 0), x) == [s.Rational(-1,2), 2]
assert s.expand((2*x-1)*(x+3)) == 2*x*x+5*x-3
assert s.simplify((1+2*s.I)/(3-s.I) - (1+7*s.I)/10) == 0
assert s.simplify(s.Rational(2,5)+s.Rational(3,5)-1) == 0
assert s.solve(s.Eq(20+2*x,50+x), x) == [30]
assert s.simplify(s.Rational(2)*s.sin(s.pi/6) - 1) == 0
assert s.simplify(s.Rational(1,2)*(1-s.Rational(1,2))) == s.Rational(1,4)
assert s.binomial(4,2) * s.Rational(1,2)**4 == s.Rational(3,8)
assert s.simplify((s.Rational(4,10)*s.Rational(2,100)) / (s.Rational(6,10)*s.Rational(1,100)+s.Rational(4,10)*s.Rational(2,100))) == s.Rational(4,7)
assert s.simplify(6*s.sqrt(3)/4*2**2) == 6*s.sqrt(3)
assert s.simplify(s.sqrt(12**2+3**2)-3*s.sqrt(17)) == 0
assert s.solve(s.Eq(40*(12-x), 2*20*x), x) == [6]
assert s.solve(s.Eq(x/s.Integer(6)+x/s.Integer(3), 1), x) == [2]
assert s.solve(s.Eq(s.Rational(4,5)*x, 80*s.Rational(6,5)), x) == [120]
assert -2**2+(-3)*(4-6) == 2
assert s.Rational(2,5)*80+s.Rational(3,5)*90 == 86
assert sum([70,80,80,90,100])/5 == 84
assert s.solve(s.Eq(100*(1+x)**2,144), x) == [s.Rational(-11,5),s.Rational(1,5)]
assert s.simplify(10*s.cos(s.pi/6)-5*s.sqrt(3)) == 0
assert s.simplify(s.Rational(1,3)*2*s.pi*6-4*s.pi) == 0
assert s.simplify(s.Rational(1,3)*s.pi*6**2-12*s.pi) == 0
assert s.Rational(8)**s.Rational(2,3) == 4
assert s.Rational(16)**s.Rational(-1,2) == s.Rational(1,4)
assert s.simplify(s.tan(5*s.pi/12)-(2+s.sqrt(3))) == 0
assert s.sin(7*s.pi/6) == -s.Rational(1,2)
assert s.cos(7*s.pi/6) == -s.sqrt(3)/2
assert sum(s.binomial(4,k) for k in range(5)) == 16
assert 4*s.Rational((30-25)**2,25) == 4
assert 0.045 < float(s.erfc(s.sqrt(2))) < 0.046
assert s.Matrix([-2,1]) == (s.Matrix([0,2])-s.Matrix([4,0]))/2
assert s.expand(2*x-2*(x-1)-2) == 0
assert s.Rational(27)**s.Rational(2,3) == 9
assert s.binomial(2,1)*s.binomial(3,1)/s.binomial(5,2) == s.Rational(3,5)
assert (s.Rational(2,5)*s.Rational(3,4)+s.Rational(3,5)*s.Rational(2,4)) == s.Rational(3,5)
assert s.expand((2+3*s.I)*(1-2*s.I)) == 8-s.I
assert all(px**2+py**2 == 25 and (px-6)**2+py**2 == 25 for px,py in [(3,4),(3,-4)])
assert sum((s.Rational(1,3)+s.Rational(3,2)*u-v)**2 for u,v in [(1,2),(2,3),(3,5)]) == s.Rational(1,6)
assert s.diff((x-20)*(100-x),x) == 120-2*x
assert ((60-20)*(100-60)) == 1600
assert s.Rational(64)/(s.Rational(160,100)**2) == 25
assert s.Rational(578,10)/(s.Rational(170,100)**2) == 20
assert s.Rational(6125,100)/(s.Rational(175,100)**2) == 20
assert s.Rational(972,10)/(s.Rational(180,100)**2) == 30
assert sum([25,20,20,30])/4 == 23.75
assert 90*60-(40*60+20) == 49*60+40
assert 180*60-(40*60+20) == 139*60+40
assert 2*(10*6+10*4+6*4) == 248
assert s.expand(3*x**2+2*x-5*x**2) == -2*x**2+2*x
assert s.solve(s.Eq(10+2*x,26),x) == [8]
assert 180-65 == 115
assert tuple(s.Matrix([-2,3])+s.Matrix([4,-1])) == (2,2)
assert 12+8 == 20 and 3*12+5*8 == 76
assert (2*1+1 == 3) and (3*3-2 == 7)
assert sum([8,9,8,7])/4 == 8 and sum([6,7,6,5])/4 == 6
assert s.sqrt((s.Rational(8,3))**2+4) == s.Rational(10,3)
assert s.sqrt((s.Rational(4,3))**2+1) == s.Rational(5,3)
assert s.simplify(1/(x-1)+1-2/(x-1)).subs(x,2) == 0
assert 180-50-60 == 70
assert s.simplify(2/(s.sqrt(3)+1)-(s.sqrt(3)-1)) == 0
assert s.Rational((1-2)**2+(3-2)**2,5) == s.Rational(2,5)
assert 3-1 == 2
assert (10*6+10*4+6*4)*2 == 248
assert sum([2,3]) == 5 and 2*3 == 6
assert s.simplify(s.pi*3*5+ s.pi*3**2-24*s.pi) == 0
assert ((3+(-1))/2,(5+(-1))/2) == (1,2)
assert s.simplify((s.Rational(3,2))**2-s.Rational(9,4)) == 0
assert s.simplify(s.sin(s.pi/3)-s.sqrt(3)/2) == 0
assert 36.86 < float(180*s.atan(s.Rational(3,4))/s.pi) < 36.88
assert s.solve_univariate_inequality(2*x**2-3*x-2<0,x, relational=False) == s.Interval.open(s.Rational(-1,2),2)
assert s.simplify(s.sqrt(3)*s.sin(x)+s.cos(x)-2*s.sin(x+s.pi/6)) == 0
assert s.Rational(3,2)**2-2 == s.Rational(1,4)
assert s.Rational(5,4)**2-2 == s.Rational(-7,16)
assert s.Rational(1)+s.Rational(4,5)*(3-2) == s.Rational(9,5)
assert s.Rational(3,3)*(4+16+s.sqrt(4*16)) == 28
assert s.simplify((1+s.I)*(s.sqrt(3)+s.I)-((s.sqrt(3)-1)+(s.sqrt(3)+1)*s.I)) == 0
assert s.simplify(s.Abs((1+s.I)*(s.sqrt(3)+s.I))-2*s.sqrt(2)) == 0
assert s.Rational(1,2)+s.Rational(1,3)-s.Rational(1,6) == s.Rational(2,3)
assert s.ceiling(s.Rational(75,100)*8) == 6
assert s.simplify(s.sqrt(2)/2 - 1/s.sqrt(2)) == 0
assert s.expand((x-2)**2 + (s.Symbol('y')+3)**2-25) == x**2+s.Symbol('y')**2-4*x+6*s.Symbol('y')-12
assert s.Matrix([1,2,3])+2*s.Matrix([2,-1,0]) == s.Matrix([5,0,3])
assert abs(5-2) == 3
assert s.sqrt(25-9) == 4
assert s.sqrt(9+16) == 5
assert s.simplify(s.cos(s.pi/4)-1/s.sqrt(2)) == 0
assert sum(2*(-2)**j for j in range(4)) == -10
assert s.expand(x*x-(x-1)**2) == 2*x-1
assert s.diff((x*x+1)**3,x) == 6*x*(x*x+1)**2
assert s.simplify(s.diff(2**x,x)-2**x*s.log(2)) == 0
assert s.diff(x**3-3*x,x) == 3*x*x-3
assert 10*9*8*7 == 5040 and 9*9*8*7 == 4536
assert s.binomial(5,3)*2**2 == 40
assert s.Rational(0)*s.Rational(3,10)+s.Rational(1)*s.Rational(6,10)+s.Rational(2)*s.Rational(1,10) == s.Rational(4,5)
assert s.Rational(1)*s.Rational(6,10)+4*s.Rational(1,10)-s.Rational(4,5)**2 == s.Rational(9,25)
assert s.Rational(2)*s.Rational(2,5)*s.Rational(3,5)*s.Rational(3,4) == s.Rational(9,25)
assert sum(s.binomial(5,k) for k in range(6)) == 32
print('97 selected arithmetic and algebra examples independently checked; not a complete mathematical audit.')
