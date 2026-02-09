"""Fortune's sweep line algorithm for Voronoi diagram construction.

This module implements Fortune's algorithm for constructing Voronoi diagrams
from a set of points (sites). This is a simplified but functional implementation.
"""

import logging
import math
import sys
from typing import Dict, List, Optional, Set, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


Point = Tuple[float, float]
Edge = Tuple[Point, Point]


class VoronoiDiagram:
    """Voronoi diagram construction using Fortune's algorithm (simplified)."""

    def __init__(self, sites: List[Point]) -> None:
        """Initialize Voronoi diagram with sites.

        Args:
            sites: List of site points.
        """
        self.sites = sites
        self.edges: List[Edge] = []
        self.vertices: List[Point] = []

    def _distance_squared(self, p1: Point, p2: Point) -> float:
        """Compute squared distance between two points.

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

    def _circumcenter(self, p1: Point, p2: Point, p3: Point) -> Optional[Point]:
        """Compute circumcenter of three points.

        Args:
            p1: First point.
            p2: Second point.
            p3: Third point.

        Returns:
            Circumcenter point, or None if points are collinear.
        """
        ax, ay = p1
        bx, by = p2
        cx, cy = p3

        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        if abs(d) < 1e-9:
            return None

        ux = (
            (ax * ax + ay * ay) * (by - cy)
            + (bx * bx + by * by) * (cy - ay)
            + (cx * cx + cy * cy) * (ay - by)
        ) / d

        uy = (
            (ax * ax + ay * ay) * (cx - bx)
            + (bx * bx + by * by) * (ax - cx)
            + (cx * cx + cy * cy) * (bx - ax)
        ) / d

        return (ux, uy)

    def _perpendicular_bisector(
        self, p1: Point, p2: Point
    ) -> Tuple[float, float, float]:
        """Compute perpendicular bisector line (ax + by + c = 0).

        Args:
            p1: First point.
            p2: Second point.

        Returns:
            Tuple (a, b, c) representing line equation.
        """
        mid_x = (p1[0] + p2[0]) / 2.0
        mid_y = (p1[1] + p2[1]) / 2.0

        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        a = dx
        b = dy
        c = -(a * mid_x + b * mid_y)

        norm = math.sqrt(a * a + b * b)
        if norm > 1e-9:
            a /= norm
            b /= norm
            c /= norm

        return (a, b, c)

    def _line_intersection(
        self, line1: Tuple[float, float, float], line2: Tuple[float, float, float]
    ) -> Optional[Point]:
        """Find intersection of two lines.

        Args:
            line1: First line (a, b, c).
            line2: Second line (a, b, c).

        Returns:
            Intersection point, or None if lines are parallel.
        """
        a1, b1, c1 = line1
        a2, b2, c2 = line2

        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9:
            return None

        x = (b1 * c2 - b2 * c1) / det
        y = (a2 * c1 - a1 * c2) / det

        return (x, y)

    def construct_simple(self) -> List[Edge]:
        """Construct Voronoi diagram using simplified method.

        For each pair of sites, compute perpendicular bisector.
        For each triple of sites, compute circumcenter (Voronoi vertex).
        Connect vertices to form edges.

        Returns:
            List of edges in the Voronoi diagram.
        """
        if len(self.sites) < 2:
            return []

        if len(self.sites) == 2:
            p1, p2 = self.sites[0], self.sites[1]
            mid_x = (p1[0] + p2[0]) / 2.0
            mid_y = (p1[1] + p2[1]) / 2.0

            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            if abs(dx) < 1e-9:
                edge1 = ((mid_x, mid_y - 1000), (mid_x, mid_y + 1000))
            else:
                slope = -dx / dy if abs(dy) > 1e-9 else float("inf")
                if abs(slope) < 1e-9:
                    edge1 = ((mid_x - 1000, mid_y), (mid_x + 1000, mid_y))
                else:
                    x1 = mid_x - 1000
                    y1 = mid_y + slope * 1000
                    x2 = mid_x + 1000
                    y2 = mid_y - slope * 1000
                    edge1 = ((x1, y1), (x2, y2))

            return [edge1]

        vertices: List[Point] = []
        vertex_to_sites: Dict[Point, List[Point]] = {}

        for i in range(len(self.sites)):
            for j in range(i + 1, len(self.sites)):
                for k in range(j + 1, len(self.sites)):
                    center = self._circumcenter(
                        self.sites[i], self.sites[j], self.sites[k]
                    )
                    if center is not None:
                        dist_to_i = self._distance_squared(center, self.sites[i])
                        is_valid = True
                        for l in range(len(self.sites)):
                            if l in (i, j, k):
                                continue
                            dist_to_l = self._distance_squared(
                                center, self.sites[l]
                            )
                            if dist_to_l < dist_to_i - 1e-6:
                                is_valid = False
                                break

                        if is_valid:
                            existing_vertex = None
                            for v in vertices:
                                if self._distance_squared(v, center) < 1e-6:
                                    existing_vertex = v
                                    break

                            if existing_vertex is None:
                                vertices.append(center)
                                vertex_to_sites[center] = [
                                    self.sites[i],
                                    self.sites[j],
                                    self.sites[k],
                                ]
                            else:
                                sites_list = vertex_to_sites[existing_vertex]
                                for site in [self.sites[i], self.sites[j], self.sites[k]]:
                                    if site not in sites_list:
                                        sites_list.append(site)

        self.vertices = vertices

        edges: List[Edge] = []

        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                v1, v2 = vertices[i], vertices[j]

                v1_sites = vertex_to_sites.get(v1, [])
                v2_sites = vertex_to_sites.get(v2, [])

                common_sites = [s for s in v1_sites if s in v2_sites]
                if len(common_sites) >= 2:
                    edges.append((v1, v2))

        self.edges = edges
        return edges

    def construct(self) -> List[Edge]:
        """Construct Voronoi diagram.

        This is a wrapper that calls the simplified construction method.
        A full Fortune's algorithm implementation would be more complex.

        Returns:
            List of edges in the Voronoi diagram.
        """
        return self.construct_simple()

    def get_voronoi_cells(self) -> Dict[Point, List[Point]]:
        """Get Voronoi cells for each site.

        Returns:
            Dictionary mapping sites to their Voronoi cell vertices.
        """
        cells: Dict[Point, List[Point]] = {site: [] for site in self.sites}

        for vertex in self.vertices:
            distances = [
                (self._distance_squared(site, vertex), site)
                for site in self.sites
            ]
            distances.sort()

            if len(distances) >= 2:
                min_dist = distances[0][0]
                for dist, site in distances:
                    if abs(dist - min_dist) < 1e-6:
                        if vertex not in cells[site]:
                            cells[site].append(vertex)

        return cells

    def get_cell_for_point(self, point: Point) -> Optional[Point]:
        """Get the Voronoi cell (site) that contains a given point.

        Args:
            point: Point to find cell for.

        Returns:
            Site point of the containing cell, or None if not found.
        """
        if not self.sites:
            return None

        min_dist = float("inf")
        closest_site = None

        for site in self.sites:
            dist = self._distance_squared(point, site)
            if dist < min_dist:
                min_dist = dist
                closest_site = site

        return closest_site


def main() -> None:
    """Main function to run the Voronoi diagram CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Fortune's algorithm for Voronoi diagram construction"
    )
    parser.add_argument(
        "--sites",
        type=str,
        required=True,
        help="Sites in format 'x1,y1;x2,y2;...'",
    )
    parser.add_argument(
        "--cells",
        action="store_true",
        help="Show Voronoi cells",
    )
    parser.add_argument(
        "--test-point",
        type=str,
        help="Test point to find cell for (format: x,y)",
    )

    args = parser.parse_args()

    try:
        site_strings = args.sites.split(";")
        sites: List[Point] = []
        for ss in site_strings:
            coords = ss.split(",")
            if len(coords) != 2:
                raise ValueError("Each site must have 2 coordinates")
            sites.append(
                (float(coords[0].strip()), float(coords[1].strip()))
            )

        print(f"Input sites: {sites}")
        print(f"Number of sites: {len(sites)}")

        vd = VoronoiDiagram(sites)
        edges = vd.construct()

        print(f"\nVoronoi Diagram:")
        print(f"Number of vertices: {len(vd.vertices)}")
        print(f"Number of edges: {len(edges)}")
        for i, edge in enumerate(edges):
            p1, p2 = edge
            print(f"  Edge {i+1}: {p1} -> {p2}")

        if args.cells:
            cells = vd.get_voronoi_cells()
            print(f"\nVoronoi Cells:")
            for site, vertices in cells.items():
                print(f"  Site {site}: {len(vertices)} vertices")
                for vertex in vertices:
                    print(f"    {vertex}")

        if args.test_point:
            coords = args.test_point.split(",")
            if len(coords) != 2:
                raise ValueError("Test point must have 2 coordinates")
            test_point = (
                float(coords[0].strip()),
                float(coords[1].strip()),
            )
            cell_site = vd.get_cell_for_point(test_point)
            print(f"\nTest point {test_point} is in cell of site: {cell_site}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
