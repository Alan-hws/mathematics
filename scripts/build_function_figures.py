#!/usr/bin/env python3
"""Generate the static, data-based coordinate illustrations for function notes."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / 'assets' / 'figures'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans', 'svg.fonttype':'none', 'axes.unicode_minus':False})

def axes(xlim, ylim):
    fig, ax = plt.subplots(figsize=(7.4, 4.6), constrained_layout=True)
    ax.set(xlim=xlim, ylim=ylim, xlabel='x', ylabel='y')
    ax.set_axisbelow(True)
    ax.grid(True, color='#e5ebe5', linewidth=.8)
    ax.axhline(0, color='#46594e', linewidth=1)
    ax.axvline(0, color='#46594e', linewidth=1)
    for spine in ax.spines.values(): spine.set_visible(False)
    return fig, ax

def save(fig, name):
    fig.savefig(OUT/name, format='svg', metadata={'Date':None})
    plt.close(fig)

fig, ax = axes((-4.5, 4.5), (-3.5, 4.5))
ax.set_xticks(range(-4,5)); ax.set_yticks(range(-3,5)); ax.set_aspect('equal')
ax.scatter([-2,2],[3,2],c=['#27705a','#cb7950'],s=50,zorder=4)
ax.annotate('P (-2, 3)',(-2,3),xytext=(-3.9,3.45),arrowprops={'arrowstyle':'-', 'color':'#27705a'})
ax.annotate("P' (2, 2)",(2,2),xytext=(2.25,2.6),arrowprops={'arrowstyle':'-', 'color':'#cb7950'})
ax.annotate('',xy=(2,2),xytext=(-2,3),arrowprops={'arrowstyle':'->','color':'#cb7950','lw':1.8})
ax.text(-.4,2.85,'(+4, -1)',color='#a35431')
save(fig,'coordinate-translation.svg')

fig, ax=axes((-1,5),(-5,7)); x=np.linspace(-1,5,300)
ax.plot(x,2*x-4,color='#27705a',linewidth=2.6,label='y = 2x - 4')
ax.scatter([0,1,2],[-4,-2,0],color='#27705a',zorder=3)
ax.plot([0,1,1],[-4,-4,-2],color='#cb7950',linestyle='--',linewidth=1.8)
ax.annotate('rise = 2',(.99,-3),xytext=(1.2,-3.5),color='#a35431')
ax.text(.3,-4.65,'run = 1',color='#a35431')
ax.annotate('(2, 0)',(2,0),xytext=(2.25,.7));ax.legend(frameon=False,loc='upper left')
save(fig,'linear-slope.svg')

fig, ax=axes((-6,6),(-6,6))
for x in (np.linspace(-6,-1,250),np.linspace(1,6,250)):
    ax.plot(x,6/x,color='#27705a',linewidth=2.6)
ax.scatter([2,-2],[3,-3],color='#cb7950',zorder=3)
ax.annotate('(2, 3)',(2,3),xytext=(2.4,3.6));ax.annotate('(-2, -3)',(-2,-3),xytext=(-5,-3.7))
ax.text(2.9,4.5,'y = 6/x',color='#27705a');ax.text(.3,-5.6,'x = 0: undefined',color='#7a887d',fontsize=10)
save(fig,'inverse-proportion.svg')

fig, ax=axes((-1,5),(-2,5));x=np.linspace(-.5,4.5,400)
ax.plot(x,x*x-4*x+3,color='#27705a',linewidth=2.6,label='y = (x - 2)^2 - 1')
ax.axvline(2,color='#9cad9c',linestyle='--',linewidth=1.5)
ax.scatter([1,2,3],[0,-1,0],color='#cb7950',zorder=3)
ax.annotate('(1, 0)',(1,0),xytext=(.1,.65));ax.annotate('(3, 0)',(3,0),xytext=(3.2,.65));ax.annotate('vertex (2, -1)',(2,-1),xytext=(2.3,-1.65));ax.legend(frameon=False,loc='upper right')
save(fig,'quadratic-vertex.svg')
