import gmpy2
import numbers

class EllipticCurve:
    def __init__(self, p, a, b):
        if not isinstance(p, numbers.Integral):
            raise ValueError("Modulo must be integral.")
        if not isinstance(a, numbers.Integral):
            raise ValueError("Modulo must be integral.")
        if not isinstance(b, numbers.Integral):
            raise ValueError("Modulo must be integral.")

        if p < 2:
            raise ValueError("Modulo most be greater or equal to 2.")
        if not gmpy2.is_prime(p):
            raise ValueError("Only prime modulos are supported.")
        if p == 2:
            raise ValueError("Curve cannot have a characteristic of 2.")
        if p == 3:
            raise ValueError("Curve cannot have a characteristic of 3.")

        if -16 * ((4 * a**3) + (27 * b**2)) == 0:
            raise ValueError("Invalid a and/or b. Discriminant cannot be"
                             " zero.")

        self._p = p
        self._a = a
        self._b = b

        self._points = set([None])

        # Generate all possible tuples
        for x in range(self._p):
            for y in self._solve(x):
                self._points.add((x, y))

    def generate(self, start):
        current = start

        while current is not None:
            yield current
            current = self.add(current, start)

        yield current

    def add(self, p1, p2):
        # First point is identity, return p2 (even if p2 is identity)
        if p1 is None:
            return p2
        # Second point is identity, return p1 (even if p1 is identity)
        elif p2 is None:
            return p1

        if p1 not in self._points:
            raise ValueError("Point 1 must exist in the curve.")
        if p2 not in self._points:
            raise ValueError("Point 2 must exist in the curve.")

        try:
            if p1 == p2:
                slope = ((3 * p1[0]**2) + self._a) * gmpy2.invert(2 * p1[1],
                                                                  self._p)
            else:
                slope = (p2[1] - p1[1]) * gmpy2.invert(p2[0] - p1[0], self._p)
        except ZeroDivisionError:
            return None

        intersect = p1[1] - (slope * p1[0])

        x3 = (slope**2 - p1[0] - p2[0]) % self._p
        y3 = -((slope * x3) + intersect) % self._p

        return (int(x3), int(y3))

    def multiply(self, start, p1, k):
        point = p1
        for _ in range(k):
            point = self.add(point, start)

    def get_points(self):
        return self._points.copy()

    def _solve(self, x):
        y_squared = (pow(x, 3, self._p) + (self._a * x) + self._b) % self._p

        return EllipticCurve._quadratic_residue(y_squared, self._p)

    @staticmethod
    def _quadratic_residue(a, p):
        if not gmpy2.is_prime(p):
            raise ValueError("p must be prime for Euler's criterion to work.")

        points = []

        # By Euler's Criterion, we return an empty list if no solutions exist.
        if pow(a, (p - 1) // 2, p) == -1:
            return points

        # Iteratively check every point from 0 to p - 1 if its square equals
        # a mod p
        for r in range(p):
            if pow(r, 2, p) == a:
                points.append(r)

                # Once we have 2 points, we are done
                if len(points) == 2:
                    break

        return points
