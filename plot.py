from pathlib import Path

import matplotlib

from ecc import EllipticCurve

def plot_curve(curve: EllipticCurve, path: Path):
    matplotlib.use('AGG')
    import matplotlib.pyplot as plt

    # Plot the points of the curve unconnected by splitting the x's and y's as
    # separate arrays, and ignoring the None point
    # Points are empty circles in red
    plt.scatter(
        *zip(*[point for point in curve.get_points() if point is not None]),
        s=60, facecolors='none', edgecolors='r')
    
    formatted_a = ''
    if curve._a != 0:
        formatted_a += ' + {}x'.format('' if curve._a == 1 else curve._a)
    
    formatted_b = ''
    if curve._b != 0:
        formatted_b += ' + {}'.format(curve._b)

    # Title in the form of y^2 equivalent to x^3 + Ax + B 
    plt.title("Elliptic Curve: y\u00b2 \u2261 x\u00b3{}{} (mod {})"
        .format(formatted_a, formatted_b, curve._p)
    )
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.savefig(str(path), bbox_inches='tight')
    plt.close()
