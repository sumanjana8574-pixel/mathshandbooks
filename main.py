import math, cmath
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line, Ellipse
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex('#04040F')

# ── Neon Galaxy Palette ──────────────────────────
BG        = get_color_from_hex('#04040F')
BG2       = get_color_from_hex('#080820')
CARD      = get_color_from_hex('#0D0D2B')
CARD2     = get_color_from_hex('#111130')
NEON_BLUE = get_color_from_hex('#00D4FF')
NEON_PURP = get_color_from_hex('#BF5FFF')
NEON_PINK = get_color_from_hex('#FF2D78')
NEON_GRN  = get_color_from_hex('#00FF9C')
NEON_YEL  = get_color_from_hex('#FFE033')
TEXT      = get_color_from_hex('#E8EAFF')
SUBTEXT   = get_color_from_hex('#6B6B99')
RESULT_BG = get_color_from_hex('#0A0A22')

# Chapter icons and neon colors
CH_META = {
    'ch1':  ('∑',  NEON_BLUE,  '#00D4FF'),
    'ch2':  ('∠',  NEON_PURP,  '#BF5FFF'),
    'ch3':  ('⬡',  NEON_GRN  if False else get_color_from_hex('#00FF9C'),  '#00FF9C'),
    'ch4':  ('∫',  NEON_PINK,  '#FF2D78'),
    'ch5':  ('∞',  NEON_YEL,   '#FFE033'),
    'ch6':  ('⊞',  NEON_BLUE,  '#00D4FF'),
    'ch7':  ('→',  NEON_PURP,  '#BF5FFF'),
    'ch8':  ('σ',  NEON_GRN  if False else get_color_from_hex('#00FF9C'),  '#00FF9C'),
    'ch9':  ('ℂ',  NEON_PINK,  '#FF2D78'),
    'ch10': ('!',  NEON_YEL,   '#FFE033'),
    'ch11': ('λ',  NEON_BLUE,  '#00D4FF'),
    'ch12': ('★',  NEON_PURP,  '#BF5FFF'),
}

def sf(v, d=0.0):
    try: return float(v)
    except: return d
def si(v, d=0):
    try: return int(v)
    except: return d
def fact(n): return math.factorial(int(n))
def C(n,r):
    n,r=int(n),int(r)
    return 0 if r<0 or r>n else fact(n)//(fact(r)*fact(n-r))

# ── Neon Card Widget ─────────────────────────────
class NeonCard(BoxLayout):
    def __init__(self, neon_color=None, radius=18, **kwargs):
        super().__init__(**kwargs)
        self.neon_color = neon_color or NEON_BLUE
        self.radius = radius
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            # Glow outer
            r,g,b,_ = self.neon_color
            Color(r, g, b, 0.08)
            RoundedRectangle(pos=(self.x-4, self.y-4),
                             size=(self.width+8, self.height+8),
                             radius=[self.radius+4]*4)
            # Card background
            Color(*get_color_from_hex('#0D0D2B'))
            RoundedRectangle(pos=self.pos, size=self.size,
                             radius=[self.radius]*4)
            # Neon border
            Color(r, g, b, 0.7)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height,
                                    self.radius), width=1.2)

class NeonButton(Button):
    def __init__(self, neon_color=None, **kwargs):
        self.neon_color = neon_color or NEON_BLUE
        kwargs.setdefault('background_normal', '')
        kwargs.setdefault('background_color', [0,0,0,0])
        kwargs.setdefault('color', TEXT)
        kwargs.setdefault('font_size', dp(14))
        kwargs.setdefault('bold', True)
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            r,g,b,_ = self.neon_color
            Color(r, g, b, 0.15)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)]*4)
            Color(r, g, b, 0.8)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(12)), width=1.4)

    def on_press(self):
        anim = Animation(opacity=0.6, duration=0.08) + Animation(opacity=1.0, duration=0.08)
        anim.start(self)

class GlowLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault('color', TEXT)
        kwargs.setdefault('markup', True)
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'middle')
        super().__init__(**kwargs)
        self.bind(size=lambda *a: setattr(self, 'text_size', (self.width, None)))

def mlbl(text, size=14, color=TEXT, halign='left', height=32):
    l = GlowLabel(text=text, font_size=dp(size), color=color,
                  halign=halign, size_hint_y=None, height=dp(height))
    return l

def minp(hint, val='', neon=None):
    nc = neon or NEON_BLUE
    r,g,b,_ = nc
    ti = TextInput(
        hint_text=hint, text=str(val), multiline=False,
        background_color=(0,0,0,0),
        foreground_color=TEXT,
        hint_text_color=list(SUBTEXT),
        cursor_color=list(nc),
        font_size=dp(14),
        size_hint_y=None, height=dp(44),
        padding=[dp(12), dp(10)]
    )
    with ti.canvas.before:
        Color(r, g, b, 0.12)
        RoundedRectangle(pos=ti.pos, size=ti.size, radius=[dp(10)]*4)
        Color(r, g, b, 0.5)
        Line(rounded_rectangle=(ti.x, ti.y, ti.width, ti.height, dp(10)), width=1.0)
    def redraw(*a):
        ti.canvas.before.clear()
        with ti.canvas.before:
            Color(r, g, b, 0.12)
            RoundedRectangle(pos=ti.pos, size=ti.size, radius=[dp(10)]*4)
            Color(r, g, b, 0.5)
            Line(rounded_rectangle=(ti.x, ti.y, ti.width, ti.height, dp(10)), width=1.0)
    ti.bind(pos=redraw, size=redraw)
    return ti

# ── Stars Background ─────────────────────────────
class StarsBG(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import random
        self.stars = [(random.random(), random.random(), random.random()*1.5+0.5,
                       random.choice([NEON_BLUE, NEON_PURP, TEXT])) for _ in range(60)]
        self.bind(pos=self._draw, size=self._draw)
        Clock.schedule_interval(self._twinkle, 2.0)

    def _draw(self, *a):
        self.canvas.clear()
        with self.canvas:
            for sx, sy, sz, col in self.stars:
                r,g,b,_ = col
                Color(r, g, b, 0.4)
                x = self.x + sx * self.width
                y = self.y + sy * self.height
                Ellipse(pos=(x, y), size=(dp(sz), dp(sz)))

    def _twinkle(self, dt):
        import random
        self.stars = [(sx, sy, random.random()*1.5+0.5, col)
                      for sx, sy, sz, col in self.stars]
        self._draw()

# ── Topic Screen ─────────────────────────────────
class TopicScreen(Screen):
    def __init__(self, title, back, fields, fn, neon_color=None, **kw):
        super().__init__(**kw)
        self.back = back
        self.fields = fields
        self.fn = fn
        self.inputs = {}
        nc = neon_color or NEON_BLUE
        r,g,b,_ = nc

        root = FloatLayout()
        stars = StarsBG(size_hint=(1,1), pos_hint={'x':0,'y':0})
        root.add_widget(stars)

        main = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8),
                         size_hint=(1,1))

        # Header
        hdr = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        bb = NeonButton(text='←', neon_color=nc, size_hint_x=None, width=dp(46),
                        font_size=dp(20))
        bb.bind(on_release=lambda *a: setattr(self.manager, 'current', self.back))

        title_lbl = mlbl(f'[b]{title}[/b]', 16, nc, 'left', 52)
        hdr.add_widget(bb)
        hdr.add_widget(title_lbl)
        main.add_widget(hdr)

        sv = ScrollView()
        inner = BoxLayout(orientation='vertical', spacing=dp(10),
                          size_hint_y=None, padding=[0, dp(4)])
        inner.bind(minimum_height=inner.setter('height'))

        for lbl, default in fields:
            inner.add_widget(mlbl(f'  {lbl}', 12, list(SUBTEXT), height=24))
            ti = minp(lbl, default, nc)
            self.inputs[lbl] = ti
            inner.add_widget(ti)

        inner.add_widget(Widget(size_hint_y=None, height=dp(8)))

        calc_btn = NeonButton(text='▶   CALCULATE', neon_color=nc,
                              size_hint_y=None, height=dp(54), font_size=dp(15))
        calc_btn.bind(on_release=self.calc)
        inner.add_widget(calc_btn)

        inner.add_widget(Widget(size_hint_y=None, height=dp(8)))

        # Result card
        res_card = NeonCard(neon_color=nc, orientation='vertical',
                            padding=dp(12), spacing=dp(6),
                            size_hint_y=None, height=dp(280))
        res_header = mlbl('  RESULT', 11, list(nc), height=22)
        res_card.add_widget(res_header)

        self.out = Label(
            text='Enter values and press Calculate…',
            font_size=dp(13), color=list(SUBTEXT),
            halign='left', valign='top', markup=True,
            size_hint_y=None, height=dp(240)
        )
        self.out.bind(size=lambda *a: setattr(self.out, 'text_size', (self.out.width, None)))
        res_card.add_widget(self.out)
        inner.add_widget(res_card)

        sv.add_widget(inner)
        main.add_widget(sv)
        root.add_widget(main)
        self.add_widget(root)

    def calc(self, *a):
        v = {l: self.inputs[l].text for l, _ in self.fields}
        try:
            result = self.fn(v)
            self.out.color = list(TEXT)
            lines = result.split('\n')
            colored = []
            for line in lines:
                if '=' in line:
                    parts = line.split('=', 1)
                    colored.append(f'[color=#6B6B99]{parts[0]}=[/color][color=#00FF9C][b]{parts[1]}[/b][/color]')
                else:
                    colored.append(f'[color=#BF5FFF]{line}[/color]')
            self.out.text = '\n'.join(colored)
        except Exception as e:
            self.out.color = list(NEON_PINK)
            self.out.text = f'[color=#FF2D78]⚠ Error: {e}[/color]'

# ── Chapter Screen ───────────────────────────────
class ChapterScreen(Screen):
    def __init__(self, title, topics, ch_key='ch1', **kw):
        super().__init__(**kw)
        icon, nc, nc_hex = CH_META.get(ch_key, ('∑', NEON_BLUE, '#00D4FF'))
        r,g,b,_ = nc

        root = FloatLayout()
        stars = StarsBG(size_hint=(1,1), pos_hint={'x':0,'y':0})
        root.add_widget(stars)

        main = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(10),
                         size_hint=(1,1))

        hdr = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        bb = NeonButton(text='←', neon_color=nc, size_hint_x=None, width=dp(46),
                        font_size=dp(20))
        bb.bind(on_release=lambda *a: setattr(self.manager, 'current', 'home'))

        icon_lbl = Label(text=icon, font_size=dp(28), color=list(nc),
                         size_hint_x=None, width=dp(40), bold=True)
        title_lbl = mlbl(f'[b]{title}[/b]', 15, nc, 'left', 60)
        hdr.add_widget(bb)
        hdr.add_widget(icon_lbl)
        hdr.add_widget(title_lbl)
        main.add_widget(hdr)

        sv = ScrollView()
        g = BoxLayout(orientation='vertical', spacing=dp(10),
                      size_hint_y=None, padding=[0, dp(4)])
        g.bind(minimum_height=g.setter('height'))

        if not topics:
            card = NeonCard(neon_color=nc, size_hint_y=None, height=dp(80),
                            padding=dp(16))
            card.add_widget(mlbl('[i]Coming soon…[/i]', 14, list(SUBTEXT), height=40))
            g.add_widget(card)
        else:
            for key, label in topics:
                btn = NeonButton(text=f'  {icon}  {label}', neon_color=nc,
                                 size_hint_y=None, height=dp(56),
                                 halign='left', font_size=dp(14))
                btn.bind(on_release=lambda b, k=key: setattr(self.manager, 'current', k))
                g.add_widget(btn)

        sv.add_widget(g)
        main.add_widget(sv)
        root.add_widget(main)
        self.add_widget(root)

# ── Home Screen ──────────────────────────────────
class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        root = FloatLayout()
        stars = StarsBG(size_hint=(1,1), pos_hint={'x':0,'y':0})
        root.add_widget(stars)

        main = BoxLayout(orientation='vertical', padding=dp(14), spacing=dp(10),
                         size_hint=(1,1))

        # Title section
        title_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(90),
                              padding=[0, dp(8)])
        t1 = Label(text='[b]✦ MATHS HANDBOOK ✦[/b]', font_size=dp(22),
                   color=list(NEON_BLUE), markup=True,
                   size_hint_y=None, height=dp(40), halign='center')
        t1.bind(size=lambda *a: setattr(t1, 'text_size', (t1.width, None)))
        t2 = Label(text='500+ Formulas  ·  12 Chapters  ·  Neon Edition',
                   font_size=dp(12), color=list(SUBTEXT), markup=True,
                   size_hint_y=None, height=dp(26), halign='center')
        t2.bind(size=lambda *a: setattr(t2, 'text_size', (t2.width, None)))
        title_box.add_widget(t1)
        title_box.add_widget(t2)
        main.add_widget(title_box)

        sv = ScrollView()
        g = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, padding=[0, dp(4)])
        g.bind(minimum_height=g.setter('height'))

        chapters = [
            ('ch1',  'Ch 1\nAlgebra'),
            ('ch2',  'Ch 2\nTrigonometry'),
            ('ch3',  'Ch 3\nGeometry'),
            ('ch4',  'Ch 4\nCalculus'),
            ('ch5',  'Ch 5\nSequences'),
            ('ch6',  'Ch 6\nMatrices'),
            ('ch7',  'Ch 7\nVectors'),
            ('ch8',  'Ch 8\nStatistics'),
            ('ch9',  'Ch 9\nComplex Nos'),
            ('ch10', 'Ch 10\nCombinatorics'),
            ('ch11', 'Ch 11\nEngineering'),
            ('ch12', 'Ch 12\nExam Special'),
        ]

        neon_cycle = [NEON_BLUE, NEON_PURP, get_color_from_hex('#00FF9C'),
                      NEON_PINK, NEON_YEL, NEON_BLUE]

        for i, (sc, lbl) in enumerate(chapters):
            icon, nc, nc_hex = CH_META.get(sc, ('∑', NEON_BLUE, '#00D4FF'))
            r,g2,b,_ = nc

            card = NeonCard(neon_color=nc, orientation='vertical',
                            padding=dp(10), spacing=dp(4),
                            size_hint_y=None, height=dp(90))

            icon_lbl = Label(text=icon, font_size=dp(26), color=list(nc),
                             bold=True, size_hint_y=None, height=dp(34),
                             halign='center')
            icon_lbl.bind(size=lambda *a, l=icon_lbl: setattr(l,'text_size',(l.width,None)))

            name_lbl = Label(text=f'[b]{lbl}[/b]', font_size=dp(12),
                             color=list(TEXT), markup=True,
                             size_hint_y=None, height=dp(36),
                             halign='center')
            name_lbl.bind(size=lambda *a, l=name_lbl: setattr(l,'text_size',(l.width,None)))

            card.add_widget(icon_lbl)
            card.add_widget(name_lbl)

            # Make card tappable
            btn = Button(background_normal='', background_color=[0,0,0,0],
                         size_hint=(1,1), pos_hint={'x':0,'y':0})
            btn.bind(on_release=lambda b, s=sc: setattr(self.manager,'current',s))

            fl = FloatLayout(size_hint_y=None, height=dp(90))
            fl.add_widget(card)
            fl.add_widget(btn)
            g.add_widget(fl)

        sv.add_widget(g)
        main.add_widget(sv)
        root.add_widget(main)
        self.add_widget(root)

# ── Compute Functions ─────────────────────────────
def f_indices(v):
    a=sf(v['Base a'],2); m=sf(v['Exponent m'],3); n=sf(v['Exponent n'],4)
    return (f'aᵐ × aⁿ = a^(m+n) = {a**(m+n):.6g}\n'
            f'aᵐ ÷ aⁿ = a^(m-n) = {a**(m-n):.6g}\n'
            f'(aᵐ)ⁿ  = a^(mn)  = {a**(m*n):.6g}\n'
            f'a⁻ⁿ    = 1/aⁿ    = {a**(-n):.6g}\n'
            f'a^(1/n) = ⁿ√a    = {a**(1/n):.6g}')
def f_log(v):
    a=sf(v['Base a'],10); m=sf(v['m'],100); n=sf(v['n'],1000)
    if a<=0 or a==1 or m<=0 or n<=0: raise ValueError('Need a>0, a≠1, m>0, n>0')
    log=lambda b,x:math.log(x)/math.log(b)
    return (f'logₐ(mn)  = {log(a,m*n):.6g}\n'
            f'logₐ(m/n) = {log(a,m/n):.6g}\n'
            f'logₐ(mⁿ)  = {n*log(a,m):.6g}\n'
            f'ln({m:.4g})   = {math.log(m):.6g}')
def f_quad(v):
    a=sf(v['a'],1); b=sf(v['b'],-5); c=sf(v['c'],6)
    if a==0: raise ValueError('a ≠ 0')
    D=b**2-4*a*c
    res=[f'Equation : {a}x² + {b}x + {c} = 0', f'Discriminant D = {D:.6g}']
    if D>0:
        x1=(-b+math.sqrt(D))/(2*a); x2=(-b-math.sqrt(D))/(2*a)
        res+=[f'Root x₁ = {x1:.6g}', f'Root x₂ = {x2:.6g}']
    elif D==0:
        res+=[f'Equal roots x = {-b/(2*a):.6g}']
    else:
        re=-b/(2*a); im=math.sqrt(-D)/(2*a)
        res+=[f'Complex roots = {re:.4g} ± {im:.4g}i']
    res+=[f'Sum of roots = {-b/a:.6g}', f'Product of roots = {c/a:.6g}',
          f'Vertex = ({-b/(2*a):.4g}, {c-b**2/(4*a):.4g})']
    return '\n'.join(res)
def f_trig(v):
    d=sf(v['Angle (deg)'],45); r=math.radians(d)
    s=math.sin(r); c=math.cos(r); t=math.tan(r) if abs(c)>1e-9 else float('inf')
    return (f'sin({d}°) = {s:.6g}\ncos({d}°) = {c:.6g}\ntan({d}°) = {t:.6g}\n'
            f'csc({d}°) = {1/s:.6g}\nsec({d}°) = {1/c:.6g}\ncot({d}°) = {1/t:.6g}\n'
            f'sin²+cos² = {s**2+c**2:.6g} ✓')
def f_compound(v):
    A=sf(v['Angle A (deg)'],30); B=sf(v['Angle B (deg)'],45)
    a=math.radians(A); b=math.radians(B)
    return (f'sin(A+B) = {math.sin(a+b):.6g}\nsin(A-B) = {math.sin(a-b):.6g}\n'
            f'cos(A+B) = {math.cos(a+b):.6g}\ncos(A-B) = {math.cos(a-b):.6g}\n'
            f'sin(2A)  = {math.sin(2*a):.6g}\ncos(2A)  = {math.cos(2*a):.6g}')
def f_area(v):
    sh=v['Shape(circle/rect/triangle/sphere/cylinder)'].strip().lower()
    a=sf(v['Value1(r/length/base)'],5); b=sf(v['Value2(h/width)'],3)
    if sh=='circle': return f'Area = πr² = {math.pi*a**2:.6g}\nCircumference = 2πr = {2*math.pi*a:.6g}'
    if sh=='rect': return f'Area = {a*b:.6g}\nPerimeter = {2*(a+b):.6g}\nDiagonal = {math.sqrt(a**2+b**2):.6g}'
    if sh=='triangle': return f'Area = ½bh = {0.5*a*b:.6g}'
    if sh=='sphere': return f'Volume = (4/3)πr³ = {4/3*math.pi*a**3:.6g}\nSurface = 4πr² = {4*math.pi*a**2:.6g}'
    if sh=='cylinder': return f'Volume = πr²h = {math.pi*a**2*b:.6g}\nLateral SA = 2πrh = {2*math.pi*a*b:.6g}'
    raise ValueError('Use: circle / rect / triangle / sphere / cylinder')
def f_deriv(v):
    n=sf(v['n (for xⁿ)'],3); x=sf(v['x value'],2)
    return (f'f(x) = x^{n}\nf\'(x) = {n}x^{n-1}\nf\'({x}) = {n*x**(n-1):.6g}\n\n'
            f'Basic Rules:\nd/dx(xⁿ) = nxⁿ⁻¹\nd/dx(sin x) = cos x\n'
            f'd/dx(cos x) = -sin x\nd/dx(eˣ) = eˣ\nd/dx(ln x) = 1/x')
def f_integral(v):
    a=sf(v['Lower limit'],0); b=sf(v['Upper limit'],1); n=sf(v['n (for xⁿ)'],2)
    val=(b**(n+1)-a**(n+1))/(n+1) if n!=-1 else math.log(abs(b))-math.log(abs(a))
    return (f'∫[{a},{b}] x^{n} dx = {val:.6g}\n\n'
            f'∫xⁿ dx = xⁿ⁺¹/(n+1) + C\n∫sin x dx = -cos x + C\n'
            f'∫cos x dx = sin x + C\n∫eˣ dx = eˣ + C\n∫(1/x) dx = ln|x| + C')
def f_ap(v):
    a=sf(v['First term a'],1); d=sf(v['Common diff d'],2); n=si(v['Terms n'],10)
    nth=a+(n-1)*d; Sn=n/2*(2*a+(n-1)*d)
    return (f'nth term = {nth:.6g}\nSum Sₙ   = {Sn:.6g}\n'
            f'First 5  : '+', '.join(f'{a+i*d:.4g}' for i in range(5)))
def f_gp(v):
    a=sf(v['First term a'],1); r=sf(v['Ratio r'],2); n=si(v['Terms n'],8)
    nth=a*r**(n-1); Sn=a*(r**n-1)/(r-1) if r!=1 else a*n
    res=f'nth term = {nth:.6g}\nSum Sₙ   = {Sn:.6g}'
    if abs(r)<1: res+=f'\nS∞       = {a/(1-r):.6g}'
    return res+'\nFirst 5  : '+', '.join(f'{a*r**i:.4g}' for i in range(5))
def f_stats(v):
    data=[float(x) for x in v['Numbers (space-separated)'].split()]
    n=len(data); mean=sum(data)/n; ds=sorted(data)
    med=ds[n//2] if n%2 else (ds[n//2-1]+ds[n//2])/2
    var=sum((x-mean)**2 for x in data)/n
    return (f'Count n    = {n}\nMean       = {mean:.6g}\nMedian     = {med:.6g}\n'
            f'Variance   = {var:.6g}\nStd Dev    = {math.sqrt(var):.6g}\n'
            f'Min        = {min(data):.6g}\nMax        = {max(data):.6g}')
def f_prob(v):
    n=si(v['Total outcomes n'],52); r=si(v['Favourable r'],4)
    p=r/n if n>0 else 0
    return (f'P(E)         = {r}/{n} = {p:.6g}\nP(E\')        = {1-p:.6g}\n'
            f'Odds for     = {r} : {n-r}\nOdds against = {n-r} : {r}\n'
            f'P(A∪B) = P(A)+P(B)-P(A∩B)\nP(A∩B) = P(A)·P(B|A)')
def f_complex(v):
    a=sf(v['Re(z₁)'],3); b=sf(v['Im(z₁)'],4)
    c=sf(v['Re(z₂)'],1); d=sf(v['Im(z₂)'],2)
    z1=complex(a,b); z2=complex(c,d)
    return (f'z₁ + z₂ = {z1+z2}\nz₁ - z₂ = {z1-z2}\n'
            f'z₁ × z₂ = {z1*z2}\nz₁ / z₂ = {z1/z2:.4g}\n'
            f'|z₁|    = {abs(z1):.6g}\narg(z₁) = {math.degrees(math.atan2(b,a)):.4g}°\n'
            f'conj(z₁)= {a} - {b}i')
def f_pc(v):
    n=si(v['n'],10); r=si(v['r'],3)
    return (f'P(n,r) = {fact(n)//fact(n-r)}\nC(n,r) = {C(n,r)}\n'
            f'n!     = {fact(n)}\nr!     = {fact(r)}')
def f_laplace(v):
    s=sf(v['s value'],2); w=sf(v['ω'],2)
    return (f'L{{1}}         = 1/s           = {1/s:.6g}\n'
            f'L{{t}}         = 1/s²          = {1/s**2:.6g}\n'
            f'L{{sin(ωt)}}   = ω/(s²+ω²)    = {w/(s**2+w**2):.6g}\n'
            f'L{{cos(ωt)}}   = s/(s²+ω²)    = {s/(s**2+w**2):.6g}\n'
            f'L{{eᵃᵗ}}       = 1/(s-a)  [s≠a]')
def f_sici(v):
    P=sf(v['Principal P'],10000); R=sf(v['Rate R%'],8); T=sf(v['Time T(yrs)'],3)
    SI=P*R*T/100; CI=P*((1+R/100)**T-1)
    return (f'Simple Interest   = {SI:.6g}\nCompound Interest = {CI:.6g}\n'
            f'CI - SI           = {CI-SI:.6g}\nAmount (SI)       = {P+SI:.6g}\n'
            f'Amount (CI)       = {P+CI:.6g}\nRule of 72        ≈ {72/R:.4g} yrs to double')
def f_const(v):
    phi=(1+math.sqrt(5))/2; a,b=1,1; fibs=[]
    for _ in range(8): fibs.append(a); a,b=b,a+b
    return (f'π   = {math.pi:.12f}\ne   = {math.e:.12f}\n'
            f'√2  = {math.sqrt(2):.12f}\n√3  = {math.sqrt(3):.12f}\n'
            f'φ   = {phi:.12f}\nln2 = {math.log(2):.12f}\n'
            f'Fibonacci: {fibs}')

TOPICS = {
  'indices': ('Laws of Indices',   'ch1',  [('Base a',2),('Exponent m',3),('Exponent n',4)],    f_indices),
  'log':     ('Logarithm Laws',    'ch1',  [('Base a',10),('m',100),('n',1000)],                f_log),
  'quad':    ('Quadratic Equation','ch1',  [('a',1),('b',-5),('c',6)],                          f_quad),
  'trig':    ('Trig Ratios',       'ch2',  [('Angle (deg)',45)],                                 f_trig),
  'compound':('Compound Angles',   'ch2',  [('Angle A (deg)',30),('Angle B (deg)',45)],          f_compound),
  'area':    ('Area & Volume',     'ch3',  [('Shape(circle/rect/triangle/sphere/cylinder)','circle'),
                                            ('Value1(r/length/base)',5),('Value2(h/width)',3)],  f_area),
  'deriv':   ('Differentiation',   'ch4',  [('n (for xⁿ)',3),('x value',2)],                    f_deriv),
  'integ':   ('Integration',       'ch4',  [('Lower limit',0),('Upper limit',1),('n (for xⁿ)',2)], f_integral),
  'ap':      ('Arithmetic Prog.',  'ch5',  [('First term a',1),('Common diff d',2),('Terms n',10)], f_ap),
  'gp':      ('Geometric Prog.',   'ch5',  [('First term a',1),('Ratio r',2),('Terms n',8)],    f_gp),
  'stats':   ('Statistics',        'ch8',  [('Numbers (space-separated)','2 4 6 8 10')],        f_stats),
  'prob':    ('Probability',       'ch8',  [('Total outcomes n',52),('Favourable r',4)],        f_prob),
  'complex': ('Complex Numbers',   'ch9',  [('Re(z₁)',3),('Im(z₁)',4),('Re(z₂)',1),('Im(z₂)',2)], f_complex),
  'pc':      ('Permutations & Combinations','ch10',[('n',10),('r',3)],                          f_pc),
  'laplace': ('Laplace Transforms','ch11', [('s value',2),('ω',2)],                             f_laplace),
  'sici':    ('SI & CI',           'ch12', [('Principal P',10000),('Rate R%',8),('Time T(yrs)',3)], f_sici),
  'const':   ('Important Constants','ch12',[],                                                   f_const),
}
CHAPTERS = {
  'ch1': ('Ch1: Algebra',         [('indices','Laws of Indices'),('log','Logarithm Laws'),('quad','Quadratic Equation')]),
  'ch2': ('Ch2: Trigonometry',    [('trig','Basic Trig Ratios'),('compound','Compound Angles')]),
  'ch3': ('Ch3: Geometry',        [('area','Area & Volume')]),
  'ch4': ('Ch4: Calculus',        [('deriv','Differentiation'),('integ','Integration')]),
  'ch5': ('Ch5: Sequences',       [('ap','Arithmetic Progression'),('gp','Geometric Progression')]),
  'ch6': ('Ch6: Matrices',        []),
  'ch7': ('Ch7: Vectors',         []),
  'ch8': ('Ch8: Statistics',      [('stats','Statistics'),('prob','Probability')]),
  'ch9': ('Ch9: Complex Numbers', [('complex','Complex Numbers')]),
  'ch10':('Ch10: Combinatorics',  [('pc','Permutations & Combinations')]),
  'ch11':('Ch11: Engineering',    [('laplace','Laplace Transforms')]),
  'ch12':('Ch12: Exam Special',   [('sici','SI & CI'),('const','Important Constants')]),
}

class MathsApp(App):
    def build(self):
        self.title = 'Maths Handbook'
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(HomeScreen(name='home'))
        for ch, (title, topics) in CHAPTERS.items():
            sm.add_widget(ChapterScreen(title, topics, ch_key=ch, name=ch))
        for key, (title, back, fields, fn) in TOPICS.items():
            ch_key = back
            _, nc, _ = CH_META.get(ch_key, ('∑', NEON_BLUE, '#00D4FF'))
            sm.add_widget(TopicScreen(title, back, fields, fn, neon_color=nc, name=key))
        return sm

if __name__ == '__main__':
    MathsApp().run()
