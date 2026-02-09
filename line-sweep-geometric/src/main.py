"""Line sweep algorithm for geometric intersection and closest pair finding.

This module implements line sweep algorithms for solving geometric problems
including line segment intersections, rectangle intersections, and finding
the closest pair of points.
"""

import logging
import math
import sys
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


Point = Tuple[float, float]
Segment = Tuple[Point, Point]
Rectangle = Tuple[Point, Point]


class EventType(Enum):
    """Event types for line sweep algorithm."""

    LEFT = "left"
    RIGHT = "right"
    START = "start"
    END = "end"


class LineSweep:
    """Line sweep algorithm for geometric problems."""

    def __init__(self) -> None:
        """Initialize line sweep calculator."""
        pass

    def _cross_product(self, o: Point, a: Point, b: Point) -> float:
        """Compute 2D cross product (OA × OB).

        Args:
            o: Origin point.
            a: First point.
            b: Second point.

        Returns:
            Cross product value.
        """
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def _orientation(self, p: Point, q: Point, r: Point) -> int:
        """Find orientation of ordered triplet (p, q, r).

        Args:
            p: First point.
            q: Second point.
            r: Third point.

        Returns:
            0 if collinear, 1 if clockwise, 2 if counter-clockwise.
        """
        val = self._cross_product(p, q, r)
        if abs(val) < 1e-9:
            return 0
        return 1 if val > 0 else 2

    def _on_segment(self, p: Point, q: Point, r: Point) -> bool:
        """Check if point r lies on segment pq.

        Args:
            p: First endpoint of segment.
            q: Second endpoint of segment.
            r: Point to check.

        Returns:
            True if r lies on segment pq.
        """
        return (
            r[0] <= max(p[0], q[0])
            and r[0] >= min(p[0], q[0])
            and r[1] <= max(p[1], q[1])
            and r[1] >= min(p[1], q[1])
        )

    def segments_intersect(
        self, seg1: Segment, seg2: Segment
    ) -> Optional[Point]:
        """Check if two line segments intersect and return intersection point.

        Args:
            seg1: First line segment ((x1, y1), (x2, y2)).
            seg2: Second line segment ((x3, y3), (x4, y4)).

        Returns:
            Intersection point if segments intersect, None otherwise.
        """
        p1, p2 = seg1
        p3, p4 = seg2

        o1 = self._orientation(p1, p2, p3)
        o2 = self._orientation(p1, p2, p4)
        o3 = self._orientation(p3, p4, p1)
        o4 = self._orientation(p3, p4, p2)

        if o1 != o2 and o3 != o4:
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3
            x4, y4 = p4

            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(denom) < 1e-9:
                return None

            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

            if 0 <= t <= 1 and 0 <= u <= 1:
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                return (x, y)

        if o1 == 0 and self._on_segment(p1, p2, p3):
            return p3
        if o2 == 0 and self._on_segment(p1, p2, p4):
            return p4
        if o3 == 0 and self._on_segment(p3, p4, p1):
            return p1
        if o4 == 0 and self._on_segment(p3, p4, p2):
            return p2

        return None

    def find_segment_intersections(
        self, segments: List[Segment]
    ) -> List[Tuple[Segment, Segment, Point]]:
        """Find all intersections between line segments using line sweep.

        Args:
            segments: List of line segments.

        Returns:
            List of tuples (seg1, seg2, intersection_point).
        """
        if len(segments) < 2:
            return []

        events: List[Tuple[float, EventType, int, Segment]] = []

        for i, seg in enumerate(segments):
            p1, p2 = seg
            if p1[0] > p2[0] or (p1[0] == p2[0] and p1[1] > p2[1]):
                p1, p2 = p2, p1

            events.append((p1[0], EventType.START, i, (p1, p2)))
            events.append((p2[0], EventType.END, i, (p1, p2)))

        events.sort(key=lambda x: (x[0], 0 if x[1] == EventType.START else 1))

        active_segments: Dict[int, Segment] = {}
        intersections: List[Tuple[Segment, Segment, Point]] = []

        for event in events:
            x, event_type, seg_idx, seg = event

            if event_type == EventType.START:
                for active_idx, active_seg in active_segments.items():
                    intersection = self.segments_intersect(seg, active_seg)
                    if intersection is not None:
                        intersections.append((seg, active_seg, intersection))
                active_segments[seg_idx] = seg

            elif event_type == EventType.END:
                if seg_idx in active_segments:
                    del active_segments[seg_idx]

        return intersections

    def rectangles_intersect(self, rect1: Rectangle, rect2: Rectangle) -> bool:
        """Check if two rectangles intersect.

        Args:
            rect1: First rectangle ((x1, y1), (x2, y2)) where (x1,y1) is
                   bottom-left and (x2,y2) is top-right.
            rect2: Second rectangle.

        Returns:
            True if rectangles intersect, False otherwise.
        """
        (x1, y1), (x2, y2) = rect1
        (x3, y3), (x4, y4) = rect2

        return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

    def find_rectangle_intersections(
        self, rectangles: List[Rectangle]
    ) -> List[Tuple[Rectangle, Rectangle]]:
        """Find all intersecting rectangles using line sweep.

        Args:
            rectangles: List of rectangles.

        Returns:
            List of tuples of intersecting rectangles.
        """
        if len(rectangles) < 2:
            return []

        events: List[Tuple[float, EventType, int, Rectangle]] = []

        for i, rect in enumerate(rectangles):
            (x1, y1), (x2, y2) = rect
            events.append((x1, EventType.LEFT, i, rect))
            events.append((x2, EventType.RIGHT, i, rect))

        events.sort(key=lambda x: (x[0], 0 if x[1] == EventType.LEFT else 1))

        active_rectangles: Dict[int, Rectangle] = {}
        intersections: List[Tuple[Rectangle, Rectangle]] = []

        for event in events:
            x, event_type, rect_idx, rect = event

            if event_type == EventType.LEFT:
                for active_idx, active_rect in active_rectangles.items():
                    if self.rectangles_intersect(rect, active_rect):
                        intersections.append((rect, active_rect))
                active_rectangles[rect_idx] = rect

            elif event_type == EventType.RIGHT:
                if rect_idx in active_rectangles:
                    del active_rectangles[rect_idx]

        return intersections

    def _distance_squared(self, p1: Point, p2: Point) -> float:
        """Compute squared Euclidean distance between two points.

        Args:
            p1: First point.
            p2: Second point.

        Returns:
            Squared distance.
        """
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return dx * dx + dy * dy

    def _distance(self, p1: Point, p2: Point) -> float:
        """Compute Euclidean distance between two points.

        Args:
            p1: First point.
            p2: Second point.

        Returns:
            Distance.
        """
        return math.sqrt(self._distance_squared(p1, p2))

    def closest_pair_naive(self, points: List[Point]) -> Tuple[Point, Point, float]:
        """Find closest pair of points using naive O(n²) algorithm.

        Args:
            points: List of points.

        Returns:
            Tuple (point1, point2, distance).

        Raises:
            ValueError: If points list has less than 2 points.
        """
        if len(points) < 2:
            raise ValueError("Need at least 2 points")

        min_dist = float("inf")
        closest_pair = (points[0], points[1])

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dist = self._distance_squared(points[i], points[j])
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (points[i], points[j])

        return (*closest_pair, math.sqrt(min_dist))

    def closest_pair_sweep(self, points: List[Point]) -> Tuple[Point, Point, float]:
        """Find closest pair of points using line sweep algorithm.

        Args:
            points: List of points.

        Returns:
            Tuple (point1, point2, distance).

        Raises:
            ValueError: If points list has less than 2 points.
        """
        if len(points) < 2:
            raise ValueError("Need at least 2 points")

        if len(points) == 2:
            return (points[0], points[1], self._distance(points[0], points[1]))

        sorted_points = sorted(points, key=lambda p: (p[0], p[1]))

        min_dist = float("inf")
        closest_pair = (sorted_points[0], sorted_points[1])

        active_points: List[Point] = [sorted_points[0]]

        for i in range(1, len(sorted_points)):
            current = sorted_points[i]

            active_points = [
                p
                for p in active_points
                if abs(current[0] - p[0]) < min_dist
            ]

            active_points_sorted = sorted(active_points, key=lambda p: p[1])

            for j in range(len(active_points_sorted)):
                p = active_points_sorted[j]
                if abs(current[1] - p[1]) >= min_dist:
                    break

                dist = self._distance_squared(current, p)
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (current, p)

            active_points.append(current)

        return (*closest_pair, math.sqrt(min_dist))

    def closest_pair_divide_conquer(
        self, points: List[Point]
    ) -> Tuple[Point, Point, float]:
        """Find closest pair using divide and conquer algorithm.

        Args:
            points: List of points.

        Returns:
            Tuple (point1, point2, distance).

        Raises:
            ValueError: If points list has less than 2 points.
        """
        if len(points) < 2:
            raise ValueError("Need at least 2 points")

        if len(points) == 2:
            return (points[0], points[1], self._distance(points[0], points[1]))

        if len(points) <= 3:
            return self.closest_pair_naive(points)

        sorted_points = sorted(points, key=lambda p: p[0])
        mid = len(sorted_points) // 2
        mid_point = sorted_points[mid]

        left_points = sorted_points[:mid]
        right_points = sorted_points[mid:]

        left_result = self.closest_pair_divide_conquer(left_points)
        right_result = self.closest_pair_divide_conquer(right_points)
        left_pair, left_dist = (left_result[0], left_result[1]), left_result[2]
        right_pair, right_dist = (right_result[0], right_result[1]), right_result[2]

        min_dist = min(left_dist, right_dist)
        closest_pair = left_pair if left_dist < right_dist else right_pair

        strip = [
            p
            for p in sorted_points
            if abs(p[0] - mid_point[0]) < min_dist
        ]
        strip_sorted = sorted(strip, key=lambda p: p[1])

        for i in range(len(strip_sorted)):
            for j in range(i + 1, len(strip_sorted)):
                if abs(strip_sorted[j][1] - strip_sorted[i][1]) >= min_dist:
                    break
                dist = self._distance(strip_sorted[i], strip_sorted[j])
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (strip_sorted[i], strip_sorted[j])

        return (*closest_pair, min_dist)

    def find_all_closest_pairs(
        self, points: List[Point]
    ) -> List[Tuple[Point, Point, float]]:
        """Find all pairs of points with minimum distance.

        Args:
            points: List of points.

        Returns:
            List of tuples (point1, point2, distance) for all closest pairs.
        """
        if len(points) < 2:
            return []

        _, _, min_dist = self.closest_pair_sweep(points)

        all_pairs: List[Tuple[Point, Point, float]] = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dist = self._distance(points[i], points[j])
                if abs(dist - min_dist) < 1e-9:
                    all_pairs.append((points[i], points[j], dist))

        return all_pairs


def main() -> None:
    """Main function to run the line sweep CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Line sweep algorithm for geometric problems"
    )
    parser.add_argument(
        "--segments",
        type=str,
        help="Line segments in format 'x1,y1,x2,y2;x3,y3,x4,y4;...'",
    )
    parser.add_argument(
        "--rectangles",
        type=str,
        help="Rectangles in format 'x1,y1,x2,y2;x3,y3,x4,y4;...' (bottom-left, top-right)",
    )
    parser.add_argument(
        "--points",
        type=str,
        help="Points in format 'x1,y1;x2,y2;...'",
    )
    parser.add_argument(
        "--closest-pair",
        type=str,
        choices=["naive", "sweep", "divide"],
        default="sweep",
        help="Algorithm for closest pair (default: sweep)",
    )
    parser.add_argument(
        "--all-closest",
        action="store_true",
        help="Find all closest pairs",
    )

    args = parser.parse_args()

    try:
        ls = LineSweep()

        if args.segments:
            try:
                segment_strings = args.segments.split(";")
                segments: List[Segment] = []
                for ss in segment_strings:
                    coords = ss.split(",")
                    if len(coords) != 4:
                        raise ValueError("Each segment must have 4 coordinates")
                    segments.append(
                        (
                            (float(coords[0].strip()), float(coords[1].strip())),
                            (float(coords[2].strip()), float(coords[3].strip())),
                        )
                    )
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid segments format: {e}")
                sys.exit(1)

            print(f"Input segments: {segments}")
            intersections = ls.find_segment_intersections(segments)
            print(f"Number of intersections: {len(intersections)}")
            for seg1, seg2, point in intersections:
                print(f"  {seg1} ∩ {seg2} = {point}")

        elif args.rectangles:
            try:
                rect_strings = args.rectangles.split(";")
                rectangles: List[Rectangle] = []
                for rs in rect_strings:
                    coords = rs.split(",")
                    if len(coords) != 4:
                        raise ValueError("Each rectangle must have 4 coordinates")
                    rectangles.append(
                        (
                            (float(coords[0].strip()), float(coords[1].strip())),
                            (float(coords[2].strip()), float(coords[3].strip())),
                        )
                    )
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid rectangles format: {e}")
                sys.exit(1)

            print(f"Input rectangles: {rectangles}")
            intersections = ls.find_rectangle_intersections(rectangles)
            print(f"Number of intersections: {len(intersections)}")
            for rect1, rect2 in intersections:
                print(f"  {rect1} ∩ {rect2}")

        elif args.points:
            try:
                point_strings = args.points.split(";")
                points: List[Point] = []
                for ps in point_strings:
                    coords = ps.split(",")
                    if len(coords) != 2:
                        raise ValueError("Each point must have 2 coordinates")
                    points.append(
                        (float(coords[0].strip()), float(coords[1].strip()))
                    )
            except (ValueError, IndexError) as e:
                logger.error(f"Invalid points format: {e}")
                sys.exit(1)

            print(f"Input points: {points}")

            if args.all_closest:
                pairs = ls.find_all_closest_pairs(points)
                print(f"All closest pairs (distance: {pairs[0][2] if pairs else 0}):")
                for p1, p2, dist in pairs:
                    print(f"  {p1} - {p2}: {dist:.4f}")
            else:
                if args.closest_pair == "naive":
                    p1, p2, dist = ls.closest_pair_naive(points)
                elif args.closest_pair == "sweep":
                    p1, p2, dist = ls.closest_pair_sweep(points)
                elif args.closest_pair == "divide":
                    p1, p2, dist = ls.closest_pair_divide_conquer(points)

                print(f"Closest pair ({args.closest_pair}):")
                print(f"  Point 1: {p1}")
                print(f"  Point 2: {p2}")
                print(f"  Distance: {dist:.4f}")

        else:
            print("Line Sweep Algorithm for Geometric Problems")
            print("Use --help to see available options")
            print("\nExamples:")
            print("  python src/main.py --segments '0,0,2,2;1,1,3,0'")
            print("  python src/main.py --rectangles '0,0,2,2;1,1,3,3'")
            print("  python src/main.py --points '0,0;1,1;2,2;3,3' --closest-pair sweep")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
