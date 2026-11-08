"""Original questions, solutions and reproducible mathematical verification specifications."""
from curriculum import bi
import hashlib, random

QUESTIONS=[]

def M(id,u,skill,ko,en,options,sk,se,oracle=None,calc=False,figure=None,table=None):
    """Author the correct option first; deterministic shuffling prevents key patterns."""
    choices=[]
    for option in options:
        if isinstance(option,tuple):
            choices.append({'text':bi(*option),'value':None})
        else:
            choices.append({'value':str(option)})
    order=list(range(4)); random.Random(int(hashlib.sha256(id.encode()).hexdigest()[:12],16)).shuffle(order)
    item={'id':id,'unit':u,'skill':skill,'type':'MCQ','calculator':calc,'prompt':bi(ko,en),
          'choices':[choices[i] for i in order],'answer':order.index(0),'solution':bi(sk,se),
          'oracle':oracle,'figure':figure,'table':table}
    QUESTIONS.append(item);return item

def part(ko,en,ak,ae,points,criteria_ko,criteria_en,oracle=None,value=None):
    return {'prompt':bi(ko,en),'solution':bi(ak,ae),'points':points,
            'criteria':bi(criteria_ko,criteria_en),'oracle':oracle,'value':value}

def F(id,u,skill,ko,en,parts,calc=False,figure=None,table=None):
    item={'id':id,'unit':u,'skill':skill,'type':'FRQ','calculator':calc,'prompt':bi(ko,en),
          'parts':parts,'figure':figure,'table':table}
    QUESTIONS.append(item);return item

# Prerequisite diagnostic. No calculus is needed here.
M('D01',0,'Algebra',r'$x^2-5x+6=0$의 큰 해는?',r'What is the larger root of $x^2-5x+6=0$?', ['3','2','5','6'],r'$(x-2)(x-3)=0$이므로 큰 해는 $3$이다.',r'Factoring gives roots $2$ and $3$, so the larger is $3$.','max(solve(x**2-5*x+6,x))')
M('D02',0,'Rational expressions',r'$x\ne4$에서 $(x^2-16)/(x-4)$와 같은 식은?',r'For $x\ne4$, simplify $(x^2-16)/(x-4)$.',['x+4','x-4','x**2+4','4'],r'분자를 $(x-4)(x+4)$로 인수분해하고 약분한다. 제한 $x\ne4$는 유지한다.',r'Factor and cancel the common factor while retaining $x\ne4$.','cancel((x**2-16)/(x-4))')
M('D03',0,'Radian trigonometry',r'$\sin(\pi/6)$의 값은?',r'Find $\sin(\pi/6)$.',['1/2','sqrt(3)/2','1','0'],r'라디안의 특수각 값으로 $1/2$이다.',r'The standard radian value is $1/2$.','sin(pi/6)')
M('D04',0,'Exponentials and logs',r'$\ln(e^3)$의 값은?',r'Find $\ln(e^3)$.',['3','exp(3)','1','0'],r'로그와 지수는 역함수이므로 $3$이다.',r'Natural log and exponential are inverse functions.','log(exp(3))')
M('D05',0,'Composition',r'$f(x)=x^2+1$, $g(x)=2x-3$일 때 $f(g(2))$는?',r'If $f(x)=x^2+1$ and $g(x)=2x-3$, find $f(g(2))$.',['2','7','10','1'],r'$g(2)=1$을 먼저 구하면 $f(1)=2$이다.',r'First $g(2)=1$, then $f(1)=2$.','(2*2-3)**2+1')
M('D06',0,'Slope',r'$(1,3)$과 $(5,11)$을 지나는 직선의 기울기는?',r'Find the slope through $(1,3)$ and $(5,11)$.',['2','1/2','8','4'],r'$(11-3)/(5-1)=2$이다.',r'Use change in output divided by change in input.','Rational(11-3,5-1)')
M('D07',0,'Functions and domain',r'$\ln(x-2)$의 실수 정의역은?',r'What is the real domain of $\ln(x-2)$?',[(' $x>2$',' $x>2$'),(r'$x\ge2$',r'$x\ge2$'),('$x<2$','$x<2$'),('모든 실수','All real numbers')],r'로그의 입력이 양수여야 하므로 $x-2>0$이다.',r'The logarithm argument must be positive: $x-2>0$.')
M('D08',0,'Inverse functions',r'$f(x)=3x+5$일 때 $f^{-1}(11)$은?',r'For $f(x)=3x+5$, find $f^{-1}(11)$.',['2','38','16/3','1/11'],r'$3x+5=11$을 풀면 $x=2$이다.',r'Solve $3x+5=11$.','solve(3*x+5-11,x)[0]')
M('D09',0,'Powers',r'$x>0$에서 $x^{3/2}/x^{1/2}$는?',r'For $x>0$, simplify $x^{3/2}/x^{1/2}$.',['x','x**2','sqrt(x)','1'],r'지수를 빼면 $x^{3/2-1/2}=x$이다.',r'Subtract the exponents.','x**(Rational(3,2)-Rational(1,2))')
M('D10',0,'Trigonometric identities',r'$\sin^2x+\cos^2x$는?',r'What is $\sin^2x+\cos^2x$?',['1','0','sin(2*x)','2'],r'피타고라스 항등식이다.',r'Use the Pythagorean identity.','trigsimp(sin(x)**2+cos(x)**2)')
M('D11',0,'Quadratic vertex',r'$x^2-6x+11$의 최솟값은?',r'Find the minimum of $x^2-6x+11$.',['2','3','11','-6'],r'$(x-3)^2+2$로 쓰면 최솟값은 $2$이다.',r'Complete the square: $(x-3)^2+2$.','(x**2-6*x+11).subs(x,3)')
M('D12',0,'Absolute value',r'$|x-2|=5$의 두 해의 합은?',r'Find the sum of the two solutions of $|x-2|=5$.',['4','10','7','-3'],r'해는 $7,-3$이므로 합은 $4$이다.',r'The solutions are $7$ and $-3$.','(2+5)+(2-5)')

# Unit 1
M('U1-M01',1,'Algebraic limit',r'$\lim_{x\to3}(x^2-9)/(x-3)$는?',r'Evaluate $\lim_{x\to3}(x^2-9)/(x-3)$.',['6','0','3','9'],r'주변에서 $x+3$과 같으므로 극한은 $6$이다.',r'For nearby inputs simplify to $x+3$, whose limit is $6$.','limit((x**2-9)/(x-3),x,3)')
M('U1-M02',1,'One-sided limits',r'$x<0$에서 $f(x)=2+x$, $x\ge0$에서 $f(x)=5-x$이다. $x=0$에서 양쪽 극한은?',r'Let $f(x)=2+x$ for $x<0$ and $f(x)=5-x$ for $x\ge0$. What is the two-sided limit at $0$?',[('존재하지 않는다','Does not exist'),('$2$','$2$'),('$5$','$5$'),('$7/2$','$7/2$')],r'왼쪽 극한은 $2$, 오른쪽 극한은 $5$이므로 일치하지 않는다.',r'The left and right limits are $2$ and $5$, so they disagree.')
M('U1-M03',1,'Continuity parameter',r'$x<2$에서 $f(x)=kx+1$, $x\ge2$에서 $f(x)=x^2+5$이다. 연속이 되게 하는 $k$는?',r'For $x<2$, $f(x)=kx+1$; for $x\ge2$, $f(x)=x^2+5$. Which $k$ makes $f$ continuous?',['4','2','5','9'],r'$2k+1=9$를 풀어 $k=4$이다.',r'Match the limiting values: $2k+1=9$.','solve(2*x+1-9,x)[0]')
M('U1-M04',1,'Squeeze theorem',r'$\lim_{x\to0}x^2\sin(1/x)$는?',r'Evaluate $\lim_{x\to0}x^2\sin(1/x)$.',['0','1','-1','2'],r'$-x^2\le x^2\sin(1/x)\le x^2$이고 양 경계가 $0$으로 가므로 조임정리로 $0$이다.',r'Squeeze the function between $-x^2$ and $x^2$, both tending to zero.','limit(x**2*sin(1/x),x,0)')
M('U1-M05',1,'Limits at infinity',r'$\lim_{x\to\infty}(3x^2-x)/(2x^2+7)$는?',r'Evaluate $\lim_{x\to\infty}(3x^2-x)/(2x^2+7)$.',['3/2','0','3','2/3'],r'분자와 분모를 $x^2$으로 나눈 뒤 극한을 취한다.',r'Divide numerator and denominator by $x^2$.','limit((3*x**2-x)/(2*x**2+7),x,oo)')
M('U1-M06',1,'Intermediate value theorem',r'$f$가 $[0,4]$에서 연속이고 $f(0)=-2$, $f(4)=6$이다. 반드시 참인 것은?',r'A continuous $f$ on $[0,4]$ satisfies $f(0)=-2$ and $f(4)=6$. Which must be true?',[(r'$f(c)=1$인 $c\in(0,4)$가 있다',r'There is $c\in(0,4)$ with $f(c)=1$'),('영점은 정확히 하나이다','There is exactly one zero'),('$f$는 증가한다','$f$ is increasing'),('$f(2)=2$','$f(2)=2$')],r'$1$은 $-2$와 $6$ 사이에 있으므로 중간값정리를 적용한다. 유일성이나 증가는 보장되지 않는다.',r'Apply the intermediate value theorem to the value $1$. Uniqueness and monotonicity do not follow.')

# Unit 2
M('U2-M01',2,'Derivative definition',r'$\lim_{h\to0}((2+h)^3-8)/h$는?',r'Evaluate $\lim_{h\to0}((2+h)^3-8)/h$.',['12','8','6','4'],r'$f(x)=x^3$의 $f\prime(2)=3(2)^2=12$이다.',r'This is the derivative of $x^3$ at $2$.','limit(((2+h)**3-8)/h,h,0)')
M('U2-M02',2,'Product rule',r'$f(x)=x^2\sin x$일 때 $f\prime(\pi/2)$는?',r'If $f(x)=x^2\sin x$, find $f\prime(\pi/2)$.',['pi','pi**2/4','0','2'],r'$f\prime=2x\sin x+x^2\cos x$에 $\pi/2$를 대입한다.',r'Apply the product rule, then substitute.','diff(x**2*sin(x),x).subs(x,pi/2)')
M('U2-M03',2,'Quotient rule',r'$f(x)=(x^2+1)/(x+1)$일 때 $f\prime(1)$은?',r'For $f(x)=(x^2+1)/(x+1)$, find $f\prime(1)$.',['1/2','1','0','2'],r'$f\prime(1)=(2\cdot1\cdot2-2)/4=1/2$이다.',r'The quotient rule gives $(4-2)/4=1/2$.','diff((x**2+1)/(x+1),x).subs(x,1)')
M('U2-M04',2,'Trigonometric derivative',r'$f(x)=\tan x$일 때 $f\prime(\pi/4)$는?',r'For $f(x)=\tan x$, find $f\prime(\pi/4)$.',['2','1','sqrt(2)','0'],r'$f\prime=\sec^2x$이므로 $2$이다.',r'The derivative is secant squared.','diff(tan(x),x).subs(x,pi/4)')
M('U2-M05',2,'Differentiability',r'$f(x)=|x-2|$의 $x=2$에서의 성질은?',r'Which describes $f(x)=|x-2|$ at $x=2$?',[('연속이지만 미분가능하지 않다','Continuous but not differentiable'),('연속이고 미분가능하다','Continuous and differentiable'),('불연속이다','Discontinuous'),('미분계수는 $0$이다','Its derivative is $0$')],r'함숫값과 극한은 $0$으로 일치하지만 좌우 기울기는 $-1,1$로 다르다.',r'The function and limit agree, but its one-sided slopes are $-1$ and $1$.')
M('U2-M06',2,'Derivative estimate',r'표의 $x=1.8,2,2.2$에서 $f(x)=4.1,4.8,5.7$이다. 양옆 점을 쓰는 $f\prime(2)$의 추정값은?',r'The values of $f$ at $x=1.8,2,2.2$ are $4.1,4.8,5.7$. Estimate $f\prime(2)$ using the outer two points.',['4','8','0.8','2'],r'$(5.7-4.1)/(2.2-1.8)=4$이다. 표로 얻은 추정값이다.',r'The centered secant estimate is $(5.7-4.1)/0.4=4$.','(Rational(57,10)-Rational(41,10))/(Rational(22,10)-Rational(18,10))')

# Unit 3
M('U3-M01',3,'Chain rule',r'$f(x)=(2x^3+1)^4$일 때 $f\prime(1)$은?',r'If $f(x)=(2x^3+1)^4$, find $f\prime(1)$.',['648','108','216','72'],r'$f\prime=4(2x^3+1)^3(6x^2)$이므로 $648$이다.',r'Include the inner derivative $6x^2$.','diff((2*x**3+1)**4,x).subs(x,1)')
M('U3-M02',3,'Implicit derivative',r'$x^2+xy+y^2=7$에서 점 $(1,2)$의 $dy/dx$는?',r'On $x^2+xy+y^2=7$, find $dy/dx$ at $(1,2)$.',['-4/5','-1/2','-5/4','4/5'],r'$2x+y+(x+2y)y\prime=0$이므로 기울기는 $-(2x+y)/(x+2y)=-4/5$이다.',r'Implicit differentiation gives $y\prime=-(2x+y)/(x+2y)$.','(-(2*x+y)/(x+2*y)).subs({x:1,y:2})')
M('U3-M03',3,'Inverse derivative',r'$f(3)=8$, $f\prime(3)=4$이고 $f$의 국소 역함수 $g$가 있다. $g\prime(8)$은?',r'If $f(3)=8$, $f\prime(3)=4$, and $g$ is its local inverse, find $g\prime(8)$.',['1/4','4','1/8','3'],r'$g(8)=3$이므로 $g\prime(8)=1/f\prime(3)=1/4$이다.',r'Use the reciprocal derivative at the corresponding input $3$.','1/Integer(4)')
M('U3-M04',3,'Inverse trigonometric derivative',r'$f(x)=\arctan(3x)$일 때 $f\prime(0)$은?',r'For $f(x)=\arctan(3x)$, find $f\prime(0)$.',['3','1','1/3','0'],r'$f\prime=3/(1+9x^2)$에 $0$을 대입한다.',r'Use the arctangent derivative with a chain factor.','diff(atan(3*x),x).subs(x,0)')
M('U3-M05',3,'Second derivative',r'$f(x)=\sin(2x)$일 때 $f^{\prime\prime}(\pi/4)$는?',r'For $f(x)=\sin(2x)$, find $f^{\prime\prime}(\pi/4)$.',['-4','-2','0','4'],r'$f^{\prime\prime}=-4\sin(2x)$이다.',r'Differentiate twice, including a chain factor each time.','diff(sin(2*x),x,2).subs(x,pi/4)')
M('U3-M06',3,'Inverse exponential',r'$g$가 $f(x)=\ln x$의 역함수이다. $g\prime(\ln5)$는?',r'Let $g$ be the inverse of $f(x)=\ln x$. Find $g\prime(\ln5)$.',['5','1/5','log(5)','1'],r'$g(x)=e^x$이므로 $g\prime(\ln5)=5$이다.',r'The inverse is exponential, whose derivative equals itself.','diff(exp(x),x).subs(x,log(5))')

# Unit 4
M('U4-M01',4,'Speeding up',r'한 입자의 속도가 $v(t)=3t^2-12t+9$이다. $t=3/2$에서 입자는?',r'A particle has velocity $v(t)=3t^2-12t+9$. At $t=3/2$ it is:',[('음의 방향으로 움직이며 빨라진다','Moving in the negative direction and speeding up'),('음의 방향으로 움직이며 느려진다','Moving in the negative direction and slowing down'),('양의 방향으로 움직이며 빨라진다','Moving in the positive direction and speeding up'),('정지해 있다','At rest')],r'$v=-9/4$, $a=6t-12=-3$이다. 둘 다 음수이므로 음의 방향으로 움직이며 속력이 증가한다.',r'Both $v=-9/4$ and $a=-3$ are negative, so motion is negative and speed increases.')
M('U4-M02',4,'Related rates',r'구의 반지름이 $3$ cm일 때 $dr/dt=2$ cm/s이다. $dV/dt$는 몇 cm$^3$/s인가?',r'When a sphere has radius $3$ cm, $dr/dt=2$ cm/s. Find $dV/dt$ in cm$^3$/s.',['72*pi','24*pi','18*pi','36*pi'],r'$4\pi r^2r\prime=4\pi\cdot9\cdot2=72\pi$이다.',r'Differentiate volume with respect to time.','diff(Rational(4,3)*pi*x**3,x).subs(x,3)*2')
M('U4-M03',4,'Linearization',r'$x=16$에서의 선형근사로 $\sqrt{16.2}$를 추정하면?',r'Use linearization at $x=16$ to estimate $\sqrt{16.2}$.',['161/40','81/20','4','41/10'],r'$4+(1/8)(0.2)=4.025=161/40$이다.',r'Use the base value $4$ and derivative $1/8$.','sqrt(16)+diff(sqrt(x),x).subs(x,16)*Rational(1,5)')
M('U4-M04',4,'L Hospital rule',r'$\lim_{x\to0}(e^{2x}-1)/x$는?',r'Evaluate $\lim_{x\to0}(e^{2x}-1)/x$.',['2','1','0','4'],r'$0/0$형이다. 분자와 분모를 각각 미분한 비의 극한은 $2e^0=2$이다.',r'The $0/0$ form allows L Hospital rule; the ratio of derivatives tends to $2$.','limit((exp(2*x)-1)/x,x,0)')
M('U4-M05',4,'Derivative units',r'$W(t)$가 탱크의 물의 양(L), $t$가 시간(h)이다. $W\prime(3)=-4$의 의미는?',r'$W(t)$ is water volume in liters and $t$ is hours. Interpret $W\prime(3)=-4$.',[('$3$시간일 때 물의 양이 시간당 $4$ L의 비율로 감소한다','At hour $3$, water volume decreases at $4$ liters per hour'),('$3$시간일 때 물이 $4$ L이다','There are $4$ liters at hour $3$'),('첫 $3$시간 동안 물이 $4$ L 줄었다','Volume fell by $4$ liters over the first $3$ hours'),('감소율이 시간당 $4$ L씩 더 커진다','The rate itself decreases by $4$ liters per hour each hour')],r'미분계수는 그 순간의 변화율이며 단위는 L/h이다.',r'A first derivative gives the instantaneous volume rate, in liters per hour.')
M('U4-M06',4,'Ladder rate',r'길이 $10$ m 사다리의 바닥이 벽에서 $6$ m 떨어져 있고 바깥으로 $2$ m/s로 움직인다. 윗부분의 높이 변화율은?',r'A $10$ m ladder has its foot $6$ m from a wall, moving outward at $2$ m/s. Find the top height rate in m/s.',['-3/2','3/2','-8/3','-2'],r'$y=8$이고 $2xx\prime+2yy\prime=0$에서 $y\prime=-(6/8)2=-3/2$이다.',r'Use $x^2+y^2=100$, so $y\prime=-xx\prime/y$.','-6*2/sqrt(100-36)')

# Unit 5
M('U5-M01',5,'Mean value theorem',r'$f(x)=x^2$의 $[1,5]$에서 평균값정리의 $c$는?',r'For $f(x)=x^2$ on $[1,5]$, find the mean-value-theorem point $c$.',['3','2','4','6'],r'평균변화율은 $(25-1)/4=6$이고 $2c=6$이므로 $c=3$이다.',r'Set $2c$ equal to the average rate $6$.','((5**2-1**2)/Integer(5-1))/2')
M('U5-M02',5,'Absolute extrema',r'$f(x)=x^3-3x$의 $[-2,2]$에서 절대최댓값은?',r'Find the absolute maximum value of $f(x)=x^3-3x$ on $[-2,2]$.',['2','-2','0','6'],r'임계수 $-1,1$과 양 끝점에서의 값을 비교하면 최대는 $2$이다.',r'Compare values at critical numbers and both endpoints.','max([(x**3-3*x).subs(x,a) for a in [-2,-1,1,2]])')
M('U5-M03',5,'Stationary inflection',r'$f(x)=x^3$의 $x=0$에 대한 설명으로 옳은 것은?',r'Which describes $x=0$ for $f(x)=x^3$?',[('변곡점이며 극대나 극소는 아니다','An inflection point but no local extremum'),('극대점이다','A local maximum'),('극소점이다','A local minimum'),('임계수가 아니다','Not a critical number')],r'$f\prime=3x^2$는 양쪽에서 양수이고 $f^{\prime\prime}=6x$는 부호가 바뀐다.',r'The first derivative stays positive on both sides, while the second derivative changes sign.')
M('U5-M04',5,'Derivative signs',r'$f\prime(x)=(x-1)(x-3)$일 때 $f$가 증가하는 구간은?',r'If $f\prime(x)=(x-1)(x-3)$, where is $f$ increasing?',[(r' $(-\infty,1)$과 $(3,\infty)$',r' $(-\infty,1)$ and $(3,\infty)$'),('$(1,3)$','$(1,3)$'),('모든 실수','All real numbers'),(r'$(-\infty,3)$',r'$(-\infty,3)$')],r'$f\prime>0$인 바깥 두 구간에서 증가한다.',r'The derivative is positive outside the two roots.')
M('U5-M05',5,'Concavity change',r'$f^{\prime\prime}(x)=6x-12$이고 $f$가 모든 실수에서 두 번 미분가능하다. 변곡점의 $x$좌표는?',r'If $f^{\prime\prime}(x)=6x-12$ everywhere, find the inflection input.',['2','0','6','12'],r'$x=2$에서 둘째 도함수가 음수에서 양수로 바뀐다.',r'The second derivative changes from negative to positive at $2$.','solve(6*x-12,x)[0]')
M('U5-M06',5,'Optimization',r'둘레가 $40$ m인 직사각형의 가능한 최대넓이는 몇 m$^2$인가?',r'What is the maximum area in m$^2$ of a rectangle with perimeter $40$ m?',['100','200','400','80'],r'$A=x(20-x)$의 꼭짓점 $x=10$에서 넓이는 $100$이다.',r'Maximize $A=x(20-x)$ on $0<x<20$.','(x*(20-x)).subs(x,10)')

# Unit 6
M('U6-M01',6,'Definite integral',r'$\int_0^2(3x^2+1)\,dx$는?',r'Evaluate $\int_0^2(3x^2+1)\,dx$.',['10','8','6','14'],r'원시함수 $x^3+x$의 양 끝 차는 $10$이다.',r'Evaluate $x^3+x$ at the endpoints.','integrate(3*x**2+1,(x,0,2))')
M('U6-M02',6,'FTC and chain rule',r'$F(x)=\int_0^{x^2}\sqrt{1+t}\,dt$일 때 $F\prime(2)$는?',r'If $F(x)=\int_0^{x^2}\sqrt{1+t}\,dt$, find $F\prime(2)$.',['4*sqrt(5)','sqrt(5)','4*sqrt(3)','2*sqrt(5)'],r'$F\prime(x)=2x\sqrt{1+x^2}$에 $x=2$를 대입한다.',r'Apply the fundamental theorem and the chain rule.','(2*x*sqrt(1+x**2)).subs(x,2)')
M('U6-M03',6,'Unequal trapezoids',r'표의 $t=0,1,3$에서 $r(t)=2,4,8$이다. 두 사다리꼴로 $\int_0^3r(t)\,dt$를 추정하면?',r'At $t=0,1,3$, the values of $r(t)$ are $2,4,8$. Estimate $\int_0^3r(t)\,dt$ with two trapezoids.',['15','12','18','14'],r'$1(2+4)/2+2(4+8)/2=15$이다.',r'Use each interval width separately.','1*Rational(2+4,2)+2*Rational(4+8,2)')
M('U6-M04',6,'Substitution',r'$\int_0^1 6x(1+3x^2)^2\,dx$는?',r'Evaluate $\int_0^1 6x(1+3x^2)^2\,dx$.',['21','63','16','7'],r'$u=1+3x^2$에서 $\int_1^4u^2\,du=21$이다.',r'Use substitution with new bounds $1$ and $4$.','integrate(6*x*(1+3*x**2)**2,(x,0,1))')
M('U6-M05',6,'Algebra before integration',r'$x>0$에서 $(x^2+1)/x$의 한 원시함수는?',r'For $x>0$, which is an antiderivative of $(x^2+1)/x$?',['x**2/2+log(x)','2*x-1/x**2','x**2+log(x)','log(x**2+1)'],r'식을 $x+1/x$로 나누어 적분한다.',r'Divide first, then integrate $x+1/x$.','integrate((x**2+1)/x,x)')
M('U6-M06',6,'Graphical accumulation',r'그림은 선분으로 연결된 $f$의 그래프이다. $F(x)=\int_0^x f(t)\,dt$일 때 $F(3)$은?',r'The graph of $f$ consists of line segments. If $F(x)=\int_0^x f(t)\,dt$, find $F(3)$.',['3','2','4','6'],r'밑변 $3$, 높이 $2$인 삼각형의 넓이로 $3$이다.',r'The positive triangle has base $3$ and height $2$.','Rational(3*2,2)',figure='accumulation')

# Unit 7
M('U7-M01',7,'Exponential initial value',r'$y\prime=3y$, $y(0)=2$일 때 $y(\ln2)$는?',r'If $y\prime=3y$ and $y(0)=2$, find $y(\ln2)$.',['16','8','6','4'],r'$y=2e^{3x}$이므로 $y(\ln2)=16$이다.',r'The initial-value solution is $2e^{3x}$.','(2*exp(3*x)).subs(x,log(2))')
M('U7-M02',7,'Slope field',r'$y\prime=x-y$가 주는 점 $(1,3)$의 기울기는?',r'For $y\prime=x-y$, what is the slope at $(1,3)$?',['-2','2','4','-4'],r'$1-3=-2$이다.',r'Substitute the coordinates into the rate expression.','(x-y).subs({x:1,y:3})')
M('U7-M03',7,'Separation branch',r'$y\prime=x/y$, $y(0)=2$인 해의 $y(1)$은?',r'For $y\prime=x/y$ with $y(0)=2$, find $y(1)$.',['sqrt(5)','5','sqrt(3)','-sqrt(5)'],r'$y^2=x^2+4$이고 초기조건에 따라 양의 가지를 고른다.',r'Separation gives $y^2=x^2+4$; the initial value selects the positive branch.','sqrt(1**2+4)')
M('U7-M04',7,'Equilibrium',r'$y\prime=-2(y-7)$의 평형해는?',r'Find the equilibrium solution of $y\prime=-2(y-7)$.',['7','0','2','-7'],r'변화율이 $0$이 되는 상수해는 $y=7$이다.',r'Set the right-hand side to zero.','solve(-2*(y-7),y)[0]')
M('U7-M05',7,'Solution verification',r'$y=Ce^{-2x}$가 모든 상수 $C$에 대해 만족하는 방정식은?',r'Which equation is satisfied by $y=Ce^{-2x}$ for every constant $C$?',[(r'$y\prime=-2y$',r'$y\prime=-2y$'),(r'$y\prime=2y$',r'$y\prime=2y$'),(r'$y\prime=-2x$',r'$y\prime=-2x$'),(r'$y\prime=y^2$',r'$y\prime=y^2$')],r'미분하면 $y\prime=-2Ce^{-2x}=-2y$이다.',r'Differentiate and rewrite in terms of $y$.')
M('U7-M06',7,'Cooling model',r'$T\prime=-\tfrac12(T-20)$, $T(0)=60$이면 $T(2)$는?',r'If $T\prime=-\tfrac12(T-20)$ and $T(0)=60$, find $T(2)$.',['20+40/exp(1)','60/exp(1)','20+60/exp(1)','40/exp(1)'],r'$T=20+40e^{-t/2}$에 $t=2$를 대입한다.',r'The excess temperature decays exponentially.','(20+40*exp(-t/2)).subs(t,2)')

# Unit 8
M('U8-M01',8,'Average value',r'$f(x)=x^2$의 $[0,3]$에서 평균값은?',r'Find the average value of $f(x)=x^2$ on $[0,3]$.',['3','9','9/2','6'],r'$\frac13\int_0^3x^2\,dx=3$이다.',r'Divide the integral by the interval length.','integrate(x**2,(x,0,3))/3')
M('U8-M02',8,'Total distance',r'$v(t)=t-1$ m/s인 입자가 $0\le t\le3$에서 이동한 총 거리는 몇 m인가?',r'A particle has $v(t)=t-1$ m/s for $0\le t\le3$. Find total distance in meters.',['5/2','3/2','2','3'],r'$t=1$에서 나누면 두 삼각형의 넓이는 $1/2$와 $2$이다.',r'Split at the velocity zero and add the two positive areas.','-integrate(t-1,(t,0,1))+integrate(t-1,(t,1,3))')
M('U8-M03',8,'Area between curves',r'$y=x$와 $y=x^2$ 사이 $0\le x\le1$의 넓이는?',r'Find the area between $y=x$ and $y=x^2$ on $0\le x\le1$.',['1/6','1/3','1/2','2/3'],r'$\int_0^1(x-x^2)\,dx=1/6$이다.',r'Integrate top minus bottom.','integrate(x-x**2,(x,0,1))',figure='area')
M('U8-M04',8,'Disk volume',r'$y=\sqrt x$, $x$축 및 $x=4$가 둘러싼 영역을 $x$축 둘레로 회전한 부피는?',r'Rotate the region bounded by $y=\sqrt x$, the $x$-axis, and $x=4$ about the $x$-axis. Find the volume.',['8*pi','16*pi','4*pi','32*pi/3'],r'$V=\pi\int_0^4x\,dx=8\pi$이다.',r'Square the radius $\sqrt x$ in the disk formula.','pi*integrate(x,(x,0,4))')
M('U8-M05',8,'Square cross sections',r'$y=x$와 $y=x^2$ 사이 영역을 밑면으로 하고 $x$축에 수직인 단면이 정사각형이다. 부피는?',r'A solid has base between $y=x$ and $y=x^2$. Cross sections perpendicular to the $x$-axis are squares. Find its volume.',['1/30','1/6','1/15','pi/30'],r'단면의 변은 $x-x^2$이므로 $\int_0^1(x-x^2)^2\,dx=1/30$이다.',r'Integrate the square of the vertical base length.','integrate((x-x**2)**2,(x,0,1))')
M('U8-M06',8,'Horizontal slices',r'$x=y^2$와 $x=2y$가 둘러싼 넓이는?',r'Find the area enclosed by $x=y^2$ and $x=2y$.',['4/3','2/3','8/3','4'],r'교점은 $y=0,2$이고 넓이는 $\int_0^2(2y-y^2)\,dy=4/3$이다.',r'Use right minus left with horizontal slices.','integrate(2*y-y**2,(y,0,2))')
