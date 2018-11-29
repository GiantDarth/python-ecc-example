import sys
import random
import argparse

from ecc import EllipticCurve

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Generates information about an elliptic curve and
a picks a random point to demonstrate.""")\

    parser.add_argument("modulo", type=int,
                        help="The modulo of the curve. It must be prime and"
                            " greater than 3.")
    parser.add_argument("A", type=int, help="The A parameter of the curve.")
    parser.add_argument("B", type=int, help="The B parameter of the curve.")
    parser.add_argument("-x", default=None, type=int,
                        help="An optional x coordinate for the starting point."
                             " If provided, than you must provide the y"
                             " coordinate as well. The point has to exist on"
                             " the curve.")
    parser.add_argument("-y", default=None, type=int,
                        help="An optional y coordinate for the starting point."
                             " If provided, than you must provide the x"
                             " coordinate as well. The point has to exist on"
                             " the curve.")

    args = parser.parse_args()

    try:
        curve = EllipticCurve(args.modulo, args.A, args.B)
    except ValueError as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)

    if args.x is None and args.y is None:
        rand_start = random.choice(list(curve.get_points()))
    elif args.x is None or args.x is None:
        print("Both (x, y) must be provided to make sense!", file=sys.stderr)
        sys.exit(1)
    else:
        rand_start = (args.x, args.y)

    for index, point in enumerate(curve.generate(rand_start), 1):
        print("{}P: {}".format(index, point))

    print()

    for _ in range(5):
        points = random.choices(list(curve.get_points()), k=2)
        print("{} + {} = {}".format(points[0], points[1],
                                    curve.add(points[0], points[1])))

    print()

    for start in curve.get_points():
        print("Start: {}, Order: {}".format(start,
                                            len(list(curve.generate(start)))))

    print()
    print("Order of the Group:", len(curve.get_points()))
    print()