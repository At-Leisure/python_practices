import random

def RBG_circle(theta):
    """ -180 < theta < 180 """
    theta %= 360
    R = G = B = 0
    if theta == 0:# R
        R = 255
    if theta == 120:# G
        G = 255
    if theta == 240:# B
        B = 255
    if 0 < theta < 120:# R->G
        R = (120-theta)/120 *255
        G = (theta - 0)/120 *255
    if 120 < theta < 240:# R->G
        G = (theta-120)/120 *255
        B = (240-theta)/120 *255
    if 240 < theta < 360:# R->G
        B = (theta-240)/120 *255
        R = (360-theta)/120 *255
    return (R,G,B)

def RBG_random(para=None):
    return (random.random()*255,random.random()*255,random.random()*255)