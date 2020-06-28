# -*- encoding: utf-8 -*-
'''
Created on 2020/06/28 16:46:12

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
'''


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def oppaiX(t=0):
    x_1 = (1.5 * np.exp((0.12*np.sin(t)-0.5) * (y + 0.16 * np.sin(t))
                        ** 2)) / (1 + np.exp(-20 * (5 * y + np.sin(t))))
    x_2 = ((1.5 + 0.8 * (y + 0.2*np.sin(t)) ** 3) *
           (1 + np.exp(20 * (5 * y + np.sin(t)))) ** -1)
    x_3 = (1+np.exp(-(100*(y+1)+16*np.sin(t))))
    x_4 = (0.2 * (np.exp(-(y + 1) ** 2) + 1)) / \
        (1 + np.exp(100 * (y + 1) + 16*np.sin(t)))
    x_5 = (0.1 / np.exp(2 * (10 * y + 1.2*(2+np.sin(t))*np.sin(t)) ** 4))
    X = x_1 + (x_2 / x_3) + x_4 + x_5
    return X


def animate(frame):
    ln.set_xdata(oppaiX(frame))
    return ln,


def init():
    ln.set_xdata(oppaiX(0.1))
    return ln,


if '__main__' == __name__:

    fig, ax = plt.subplots(figsize=(10, 9))
    plt.axes().set_aspect('equal', 'datalim')
    y = np.arange(-3, 3.01, 0.01)
    ln, = plt.plot(oppaiX(t=0.1), y)

    frames = np.linspace(0.1, 10, 100)
    ani = animation.FuncAnimation(fig=fig, func=animate, frames=np.hstack((frames, frames[::-1])),
                                  init_func=init, interval=20, blit=True)
    
    plt.show()
    # ani.save('Oppai.mp4')