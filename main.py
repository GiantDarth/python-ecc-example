import sys
import random
import argparse
from pathlib import Path

from eulerlib.numtheory import Divisors

from ecc import EllipticCurve
from plot import plot_curve

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Generates information about an elliptic curve and
a picks a random point to demonstrate.""",
        epilog="""
Copyright (c) 2018 Christopher Robert Philabaum <cp723@nau.edu>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

    parser.add_argument("modulo", type=int,
                        help="The modulo of the curve. It must be prime and"
                            " greater than 3.")
    parser.add_argument("A", type=int, help="The A parameter of the curve.")
    parser.add_argument("B", type=int, help="The B parameter of the curve.")
    parser.add_argument("-s", "--start", default=None, type=int, nargs=2,
                        help="An optional x, y coordinate for the starting"
                             " point. The point has to exist on"
                             " the curve.")
    parser.add_argument("-p", "--path", default=None, type=str,
                        help="An optional path to save the plot as a .png. If"
                             " not provided, then no file will be saved.")

    args = parser.parse_args()

    try:
        curve = EllipticCurve(args.modulo, args.A, args.B)
    except ValueError as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)

    points = list(curve.get_points())

    if args.start is None:
        start = random.choice(points)
    else:
        start = tuple(args.start)
    
    plot_path = None
    if args.path is not None:
        plot_path = Path(args.path)

    generated_points = list(curve.generate(start))
    for index, point in enumerate(generated_points, 1):
        print("{}P: {}".format(index, point))

    print()

    print("Example (Addition):")
    for _ in range(5):
        add_points = [random.choice(generated_points) for _ in range(2)]
        add_points_indices = [
            generated_points.index(point) + 1 for point in add_points
        ]

        result = curve.add(add_points[0], add_points[1])
        result_pos = generated_points.index(result) + 1

        predicted_point_pos = (sum(add_points_indices)
            % len(generated_points))
        # We want to refer to 0P as (#E)P
        if predicted_point_pos == 0:
            predicted_point_pos = len(generated_points)
        # Make sure to have the prediction position to be 0-based.
        predicted_point = generated_points[predicted_point_pos - 1]

        print("{}P {} + {}P {} =".format(
            add_points_indices[0], add_points[0],
            add_points_indices[1], add_points[1]
        ))
        print("\tPredicted: {}P {}".format(predicted_point_pos,
                                            predicted_point))
        print("\tActual: {}P {}".format(result_pos, result))

    print()

    primitive_elements = []

    for s in curve.get_points():
        print("Start: {}, Order: {}".format(s,
                                            len(list(curve.generate(s)))))
        if len(list(curve.generate(s))) == len(points):
            primitive_elements.append(s)

    print()
    print("Order of the Group:", len(points))
    print("# of Generators:")
    print("\tPredicted: \u03d5({}) = {}".format(
        len(points), int(Divisors().phi(len(points)))))
    print("\tActual:", len(primitive_elements))
    print()

    if plot_path is not None:
        print("Saving plot to '{}'...".format(plot_path))
        plot_curve(curve, plot_path)
        print()
