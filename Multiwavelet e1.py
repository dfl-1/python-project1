import matplotlib.pyplot as plt
import numpy as np
import math as mt

if __name__ == '__main__':
    f = [x for x in range(100)]
    ce = [f[i] for i in range(0, 100, 2)]
    co = [f[i] for i in range(1, 100, 2)]
    c0 = np.array([ce, co]) 
    l = int(mt.log(len(ce), 2))

    p0 = np.array([[0.5, 0.5], [-7**0.5/4, -7**0.5/4]])/2
    p1 = np.array([[1, 0], [0, 0.5]])/2
    p2 = np.array([[0.5, -0.5], [7**0.5/4, -7**0.5/4]])/2
    P = [p0, p1, p2]

    q0 = np.array([[-0.5, -0.5], [1/4, 1/4]])/2
    q1 = np.array([[1, 0], [0, 7**0.5/2]])/2
    q2 = np.array([[-0.5, 0.5], [-1/4, 1/4]])/2
    Q = [q0, q1, q2]

    coeffs = []
    c = c0
    for i in range(l):
        d = np.dot(q0, c) + np.dot(q1, c) + np.dot(q2, c)
        c = np.dot(p0, c)+np.dot(p1, c)+np.dot(p2, c)
        coeffs.insert(0, d)
    coeffs.insert(0, c)

    c = coeffs[0]
    for i in range(1, len(coeffs)):
        d = coeffs[i]
        c = np.dot(np.transpose(p0), c)+np.dot(np.transpose(p1), c)+np.dot(np.transpose(p2), c) + \
            np.dot(np.transpose(q0), d)+np.dot(np.transpose(q1), d)+np.dot(np.transpose(q2), d)
    print(c)
    print(c0)




