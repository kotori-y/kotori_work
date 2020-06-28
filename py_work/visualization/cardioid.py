# -*- encoding: utf-8 -*-
'''
Created on 2020/06/28 14:47:40

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
'''


import matplotlib.pyplot as plt
import numpy as np


def drawCardioid(a=1):
    f, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    
    theta = np.linspace(0, 360, 1000, endpoint=True)
    theta = np.radians(theta) #angle to radian 
    rho = a * (1 - np.sin(theta))

    ax.plot(theta, rho)

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    plt.show()
    return f



if '__main__' == __name__:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')

    def init():
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(-1, 1)
        return ln,

    def update(frame):
        xdata.append(frame)
        ydata.append(np.sin(frame))
        ln.set_data(xdata, ydata)
        return ln,

    ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                        init_func=init, blit=True)

    fig.savefig('sdsfs.gif')
    
    plt.show()