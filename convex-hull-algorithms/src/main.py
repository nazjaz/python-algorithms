"""Convex hull algorithms implementation.

This module implements Graham scan and Andrew's monotone chain algorithms
for 2D convex hull computation, along with 3D convex hull extension.
"""

import logging
import math
import sys
from typing import Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


Point2D = Tuple[float, float]
Point3D = Tuple[float, float, float]


class ConvexHull:
    """Convex hull computation using various algorithms."""

    def __init__(self) -> None:
        """Initialize convex hull calculator."""
        pass

    def _cross_product_2d(self, o: Point2D, a: Point2D, b: Point2D) -> float:
        """Compute 2D cross product (OA × OB).

        Args:
            o: Origin point.
            a: First point.
            b: Second point.

        Returns:
            Cross product value. Positive if counter-clockwise, negative if clockwise.
        """
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def _cross_product_3d(
        self, a: Point3D, b: Point3D, c: Point3D
    ) -> Tuple[float, float, float]:
        """Compute 3D cross product (AB × AC).

        Args:
            a: First point.
            b: Second point.
            c: Third point.

        Returns:
            3D cross product vector.
        """
        ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        ac = (c[0] - a[0], c[1] - a[1], c[2] - a[2])

        return (
            ab[1] * ac[2] - ab[2] * ac[1],
            ab[2] * ac[0] - ab[0] * ac[2],
            ab[0] * ac[1] - ab[1] * ac[0],
        )

    def _dot_product_3d(self, a: Point3D, b: Point3D) -> float:
        """Compute 3D dot product.

        Args:
            a: First vector (as point).
            b: Second vector (as point).

        Returns:
            Dot product value.
        """
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def _distance_2d(self, a: Point2D, b: Point2D) -> float:
        """Compute Euclidean distance between two 2D points.

        Args:
            a: First point.
            b: Second point.

        Returns:
            Distance between points.
        """
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return math.sqrt(dx * dx + dy * dy)

    def _distance_3d(self, a: Point3D, b: Point3D) -> float:
        """Compute Euclidean distance between two 3D points.

        Args:
            a: First point.
            b: Second point.

        Returns:
            Distance between points.
        """
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        dz = a[2] - b[2]
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def _find_bottom_left_2d(self, points: List[Point2D]) -> int:
        """Find bottom-left point (lowest y, then leftmost x).

        Args:
            points: List of 2D points.

        Returns:
            Index of bottom-left point.

        Raises:
            ValueError: If points list is empty.
        """
        if not points:
            raise ValueError("Points list cannot be empty")

        min_idx = 0
        for i in range(1, len(points)):
            if points[i][1] < points[min_idx][1] or (
                points[i][1] == points[min_idx][1]
                and points[i][0] < points[min_idx][0]
            ):
                min_idx = i

        return min_idx

    def graham_scan_2d(self, points: List[Point2D]) -> List[Point2D]:
        """Compute 2D convex hull using Graham scan algorithm.

        Args:
            points: List of 2D points.

        Returns:
            List of points forming the convex hull in counter-clockwise order.

        Raises:
            ValueError: If points list is empty or has less than 3 points.
        """
        if len(points) < 3:
            if len(points) <= 1:
                return points.copy()
            if len(points) == 2:
                return points.copy()

        points = points.copy()
        bottom_idx = self._find_bottom_left_2d(points)
        points[0], points[bottom_idx] = points[bottom_idx], points[0]

        pivot = points[0]

        def polar_angle(p: Point2D) -> Tuple[float, float]:
            dx = p[0] - pivot[0]
            dy = p[1] - pivot[1]
            angle = math.atan2(dy, dx)
            dist = math.sqrt(dx * dx + dy * dy)
            return (angle, dist)

        sorted_points = sorted(points[1:], key=polar_angle)

        hull = [pivot, sorted_points[0]]

        for i in range(1, len(sorted_points)):
            while (
                len(hull) > 1
                and self._cross_product_2d(
                    hull[-2], hull[-1], sorted_points[i]
                )
                <= 0
            ):
                hull.pop()
            hull.append(sorted_points[i])

        return hull

    def andrews_monotone_chain_2d(
        self, points: List[Point2D]
    ) -> List[Point2D]:
        """Compute 2D convex hull using Andrew's monotone chain algorithm.

        Args:
            points: List of 2D points.

        Returns:
            List of points forming the convex hull in counter-clockwise order.

        Raises:
            ValueError: If points list is empty.
        """
        if len(points) <= 1:
            return points.copy()

        if len(points) == 2:
            return points.copy()

        points = sorted(points)

        def build_hull(half_points: List[Point2D]) -> List[Point2D]:
            hull = []
            for point in half_points:
                while (
                    len(hull) >= 2
                    and self._cross_product_2d(
                        hull[-2], hull[-1], point
                    )
                    <= 0
                ):
                    hull.pop()
                hull.append(point)
            return hull

        lower = build_hull(points)
        upper = build_hull(reversed(points))

        return lower[:-1] + upper[:-1]

    def gift_wrapping_3d(self, points: List[Point3D]) -> List[Tuple[int, int, int]]:
        """Compute 3D convex hull using gift wrapping algorithm.

        Args:
            points: List of 3D points.

        Returns:
            List of triangular faces (indices of points forming triangles).

        Raises:
            ValueError: If points list has less than 4 points.
        """
        if len(points) < 4:
            if len(points) <= 2:
                return []
            if len(points) == 3:
                return [(0, 1, 2)]

        n = len(points)
        faces: List[Tuple[int, int, int]] = []

        def normalize_face(face: Tuple[int, int, int]) -> Tuple[int, int, int]:
            a, b, c = face
            permutations = [
                (a, b, c),
                (b, c, a),
                (c, a, b),
            ]
            return min(permutations)

        def face_exists(face: Tuple[int, int, int]) -> bool:
            normalized = normalize_face(face)
            for f in faces:
                if normalize_face(f) == normalized:
                    return True
            return False

        def find_initial_face() -> Optional[Tuple[int, int, int]]:
            for i in range(n):
                for j in range(i + 1, n):
                    for k in range(j + 1, n):
                        normal = self._cross_product_3d(
                            points[i], points[j], points[k]
                        )
                        norm = math.sqrt(
                            normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2
                        )
                        if norm < 1e-9:
                            continue

                        all_on_same_side = True
                        sign = 0

                        for l in range(n):
                            if l in (i, j, k):
                                continue
                            vec = (
                                points[l][0] - points[i][0],
                                points[l][1] - points[i][1],
                                points[l][2] - points[i][2],
                            )
                            dot = self._dot_product_3d(normal, vec)

                            if abs(dot) > 1e-9:
                                if sign == 0:
                                    sign = 1 if dot > 0 else -1
                                elif (dot > 0 and sign < 0) or (dot < 0 and sign > 0):
                                    all_on_same_side = False
                                    break

                        if all_on_same_side:
                            return (i, j, k)
            return None

        initial_face = find_initial_face()
        if initial_face is None:
            return []

        faces.append(initial_face)
        edge_to_faces: Dict[Tuple[int, int], List[Tuple[int, int, int]]] = {}

        def add_edge(edge: Tuple[int, int], face: Tuple[int, int, int]) -> None:
            a, b = edge
            normalized_edge = (min(a, b), max(a, b))
            if normalized_edge not in edge_to_faces:
                edge_to_faces[normalized_edge] = []
            edge_to_faces[normalized_edge].append(face)

        for i in range(3):
            j = (i + 1) % 3
            edge = (initial_face[i], initial_face[j])
            add_edge(edge, initial_face)

        changed = True
        max_iterations = n * n
        iterations = 0

        while changed and iterations < max_iterations:
            iterations += 1
            changed = False

            for edge, face_list in list(edge_to_faces.items()):
                if len(face_list) >= 2:
                    continue

                a, b = edge
                best_point = None
                best_distance = -1

                for c in range(n):
                    if c == a or c == b:
                        continue

                    test_face = (a, b, c)
                    if face_exists(test_face):
                        continue

                    normal = self._cross_product_3d(
                        points[a], points[b], points[c]
                    )
                    norm = math.sqrt(
                        normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2
                    )

                    if norm < 1e-9:
                        continue

                    is_visible = True
                    for d in range(n):
                        if d in (a, b, c):
                            continue
                        vec = (
                            points[d][0] - points[a][0],
                            points[d][1] - points[a][1],
                            points[d][2] - points[a][2],
                        )
                        dot = self._dot_product_3d(normal, vec)
                        if dot > 1e-9:
                            is_visible = False
                            break

                    if is_visible and norm > best_distance:
                        best_distance = norm
                        best_point = c

                if best_point is not None:
                    new_face = (a, b, best_point)
                    if not face_exists(new_face):
                        faces.append(new_face)
                        changed = True

                        for i in range(3):
                            j = (i + 1) % 3
                            edge_new = (new_face[i], new_face[j])
                            add_edge(edge_new, new_face)

        return faces

    def convex_hull_2d(
        self, points: List[Point2D], algorithm: str = "graham"
    ) -> List[Point2D]:
        """Compute 2D convex hull using specified algorithm.

        Args:
            points: List of 2D points.
            algorithm: Algorithm to use ("graham" or "andrews"). Default: "graham".

        Returns:
            List of points forming the convex hull.

        Raises:
            ValueError: If algorithm name is invalid.
        """
        if algorithm.lower() == "graham":
            return self.graham_scan_2d(points)
        elif algorithm.lower() == "andrews":
            return self.andrews_monotone_chain_2d(points)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def convex_hull_3d(self, points: List[Point3D]) -> List[Tuple[int, int, int]]:
        """Compute 3D convex hull using gift wrapping algorithm.

        Args:
            points: List of 3D points.

        Returns:
            List of triangular faces (indices of points forming triangles).
        """
        return self.gift_wrapping_3d(points)

    def hull_area_2d(self, hull_points: List[Point2D]) -> float:
        """Compute area of 2D convex hull.

        Args:
            hull_points: Points forming the convex hull in order.

        Returns:
            Area of the convex hull polygon.
        """
        if len(hull_points) < 3:
            return 0.0

        area = 0.0
        n = len(hull_points)

        for i in range(n):
            j = (i + 1) % n
            area += hull_points[i][0] * hull_points[j][1]
            area -= hull_points[j][0] * hull_points[i][1]

        return abs(area) / 2.0

    def hull_perimeter_2d(self, hull_points: List[Point2D]) -> float:
        """Compute perimeter of 2D convex hull.

        Args:
            hull_points: Points forming the convex hull in order.

        Returns:
            Perimeter of the convex hull polygon.
        """
        if len(hull_points) < 2:
            return 0.0

        if len(hull_points) == 2:
            return self._distance_2d(hull_points[0], hull_points[1])

        perimeter = 0.0
        n = len(hull_points)

        for i in range(n):
            j = (i + 1) % n
            perimeter += self._distance_2d(hull_points[i], hull_points[j])

        return perimeter

    def hull_volume_3d(
        self, points: List[Point3D], faces: List[Tuple[int, int, int]]
    ) -> float:
        """Compute volume of 3D convex hull.

        Args:
            points: List of 3D points.
            faces: List of triangular faces (indices).

        Returns:
            Volume of the 3D convex hull.
        """
        if len(faces) == 0:
            return 0.0

        volume = 0.0
        origin = points[0] if points else (0.0, 0.0, 0.0)

        for face in faces:
            a, b, c = points[face[0]], points[face[1]], points[face[2]]

            normal = self._cross_product_3d(a, b, c)
            dot = self._dot_product_3d(normal, a)

            volume += dot / 6.0

        return abs(volume)

    def is_point_inside_2d(
        self, point: Point2D, hull_points: List[Point2D]
    ) -> bool:
        """Check if a point is inside 2D convex hull.

        Args:
            point: Point to check.
            hull_points: Points forming the convex hull in order.

        Returns:
            True if point is inside or on the hull, False otherwise.
        """
        if len(hull_points) < 3:
            return False

        n = len(hull_points)
        for i in range(n):
            j = (i + 1) % n
            cross = self._cross_product_2d(hull_points[i], hull_points[j], point)
            if cross < 0:
                return False

        return True

    def hull_surface_area_3d(
        self, points: List[Point3D], faces: List[Tuple[int, int, int]]
    ) -> float:
        """Compute surface area of 3D convex hull.

        Args:
            points: List of 3D points.
            faces: List of triangular faces (indices).

        Returns:
            Surface area of the 3D convex hull.
        """
        surface_area = 0.0

        for face in faces:
            a, b, c = points[face[0]], points[face[1]], points[face[2]]

            ab = (
                b[0] - a[0],
                b[1] - a[1],
                b[2] - a[2],
            )
            ac = (
                c[0] - a[0],
                c[1] - a[1],
                c[2] - a[2],
            )

            normal = self._cross_product_3d(a, b, c)
            area = 0.5 * math.sqrt(
                normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2
            )

            surface_area += area

        return surface_area


def main() -> None:
    """Main function to run the convex hull CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Convex hull algorithms (Graham scan, Andrew's, 3D)"
    )
    parser.add_argument(
        "--points-2d",
        type=str,
        help="2D points in format 'x1,y1;x2,y2;...'",
    )
    parser.add_argument(
        "--points-3d",
        type=str,
        help="3D points in format 'x1,y1,z1;x2,y2,z2;...'",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        choices=["graham", "andrews"],
        default="graham",
        help="Algorithm for 2D convex hull (default: graham)",
    )
    parser.add_argument(
        "--area",
        action="store_true",
        help="Compute area of 2D convex hull",
    )
    parser.add_argument(
        "--perimeter",
        action="store_true",
        help="Compute perimeter of 2D convex hull",
    )
    parser.add_argument(
        "--volume",
        action="store_true",
        help="Compute volume of 3D convex hull",
    )
    parser.add_argument(
        "--surface-area",
        action="store_true",
        help="Compute surface area of 3D convex hull",
    )
    parser.add_argument(
        "--check-point",
        type=str,
        help="Check if point is inside 2D hull (format: x,y)",
    )

    args = parser.parse_args()

    try:
        ch = ConvexHull()

        if args.points_2d:
            try:
                point_strings = args.points_2d.split(";")
                points_2d: List[Point2D] = []
                for ps in point_strings:
                    coords = ps.split(",")
                    if len(coords) != 2:
                        raise ValueError("Each point must have 2 coordinates")
                    points_2d.append(
                        (float(coords[0].strip()), float(coords[1].strip()))
                    )
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid 2D points format: {e}")
                sys.exit(1)

            print(f"Input points (2D): {points_2d}")
            print(f"Algorithm: {args.algorithm}")

            hull = ch.convex_hull_2d(points_2d, algorithm=args.algorithm)
            print(f"Convex hull points: {hull}")

            if args.area:
                area = ch.hull_area_2d(hull)
                print(f"Area: {area:.2f}")

            if args.perimeter:
                perimeter = ch.hull_perimeter_2d(hull)
                print(f"Perimeter: {perimeter:.2f}")

            if args.check_point:
                try:
                    coords = args.check_point.split(",")
                    if len(coords) != 2:
                        raise ValueError("Point must have 2 coordinates")
                    point = (
                        float(coords[0].strip()),
                        float(coords[1].strip()),
                    )
                    is_inside = ch.is_point_inside_2d(point, hull)
                    print(f"Point {point} is {'inside' if is_inside else 'outside'} the hull")
                except (ValueError, IndexError) as e:
                    logger.error(f"Invalid point format: {e}")
                    sys.exit(1)

        elif args.points_3d:
            try:
                point_strings = args.points_3d.split(";")
                points_3d: List[Point3D] = []
                for ps in point_strings:
                    coords = ps.split(",")
                    if len(coords) != 3:
                        raise ValueError("Each point must have 3 coordinates")
                    points_3d.append(
                        (
                            float(coords[0].strip()),
                            float(coords[1].strip()),
                            float(coords[2].strip()),
                        )
                    )
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid 3D points format: {e}")
                sys.exit(1)

            print(f"Input points (3D): {points_3d}")

            faces = ch.convex_hull_3d(points_3d)
            print(f"Convex hull faces: {faces}")
            print(f"Number of faces: {len(faces)}")

            if args.volume:
                volume = ch.hull_volume_3d(points_3d, faces)
                print(f"Volume: {volume:.2f}")

            if args.surface_area:
                surface_area = ch.hull_surface_area_3d(points_3d, faces)
                print(f"Surface area: {surface_area:.2f}")

        else:
            print("Convex Hull Algorithms")
            print("Use --help to see available options")
            print("\nExamples:")
            print("  python src/main.py --points-2d '0,0;1,1;2,0;1,0.5' --algorithm graham")
            print("  python src/main.py --points-2d '0,0;1,1;2,0' --area --perimeter")
            print("  python src/main.py --points-3d '0,0,0;1,0,0;0,1,0;0,0,1' --volume")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
