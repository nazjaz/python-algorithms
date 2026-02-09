"""Delaunay triangulation with incremental insertion and edge flipping.

This module implements Delaunay triangulation using incremental insertion
and Lawson's edge flipping algorithm to maintain the empty circle property.
"""

import logging
import math
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


Point = Tuple[float, float]
Triangle = Tuple[int, int, int]
Edge = Tuple[int, int]


@dataclass
class TriangleData:
    """Triangle data structure."""

    vertices: Triangle
    neighbors: List[Optional[int]] = field(default_factory=lambda: [None, None, None])
    circumcenter: Optional[Point] = None
    circumradius_sq: float = 0.0

    def __bool__(self) -> bool:
        """Check if triangle is valid (not None)."""
        return True


class DelaunayTriangulation:
    """Delaunay triangulation using incremental insertion and edge flipping."""

    def __init__(self, points: List[Point]) -> None:
        """Initialize Delaunay triangulation with points.

        Args:
            points: List of points to triangulate.
        """
        self.points = points
        self.triangles: List[Optional[TriangleData]] = []
        self.edge_to_triangles: Dict[Edge, List[int]] = {}

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

    def _point_in_circumcircle(
        self, point: Point, triangle: TriangleData
    ) -> bool:
        """Check if point is inside triangle's circumcircle.

        Args:
            point: Point to check.
            triangle: Triangle to check against.

        Returns:
            True if point is inside circumcircle.
        """
        if triangle.circumcenter is None:
            return False

        dist_sq = self._distance_squared(point, triangle.circumcenter)
        return dist_sq < triangle.circumradius_sq - 1e-9

    def _update_triangle_circumcircle(self, tri_idx: int) -> None:
        """Update circumcircle for a triangle.

        Args:
            tri_idx: Triangle index.
        """
        triangle = self.triangles[tri_idx]
        v0, v1, v2 = triangle.vertices

        center = self._circumcenter(
            self.points[v0], self.points[v1], self.points[v2]
        )
        if center is not None:
            triangle.circumcenter = center
            triangle.circumradius_sq = self._distance_squared(
                center, self.points[v0]
            )

    def _point_in_triangle(self, point: Point, triangle: TriangleData) -> bool:
        """Check if point is inside triangle using barycentric coordinates.

        Args:
            point: Point to check.
            triangle: Triangle to check against.

        Returns:
            True if point is inside triangle.
        """
        v0, v1, v2 = triangle.vertices
        p0, p1, p2 = (
            self.points[v0],
            self.points[v1],
            self.points[v2],
        )

        def sign(p1: Point, p2: Point, p3: Point) -> float:
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (
                p1[1] - p3[1]
            )

        d1 = sign(point, p0, p1)
        d2 = sign(point, p1, p2)
        d3 = sign(point, p2, p0)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def _find_triangle_containing(self, point: Point) -> Optional[int]:
        """Find triangle containing a point.

        Args:
            point: Point to locate.

        Returns:
            Triangle index, or None if not found.
        """
        for i, triangle in enumerate(self.triangles):
            if self._point_in_triangle(point, triangle):
                return i
        return None

    def _get_edge(self, v1: int, v2: int) -> Edge:
        """Get normalized edge (smaller index first).

        Args:
            v1: First vertex index.
            v2: Second vertex index.

        Returns:
            Normalized edge.
        """
        return (min(v1, v2), max(v1, v2))

    def _add_edge_to_triangle(self, edge: Edge, tri_idx: int) -> None:
        """Add edge to triangle mapping.

        Args:
            edge: Edge.
            tri_idx: Triangle index.
        """
        if edge not in self.edge_to_triangles:
            self.edge_to_triangles[edge] = []
        if tri_idx not in self.edge_to_triangles[edge]:
            self.edge_to_triangles[edge].append(tri_idx)

    def _remove_edge_from_triangle(self, edge: Edge, tri_idx: int) -> None:
        """Remove edge from triangle mapping.

        Args:
            edge: Edge.
            tri_idx: Triangle index.
        """
        if edge in self.edge_to_triangles:
            if tri_idx in self.edge_to_triangles[edge]:
                self.edge_to_triangles[edge].remove(tri_idx)
            if not self.edge_to_triangles[edge]:
                del self.edge_to_triangles[edge]

    def _add_triangle(self, v0: int, v1: int, v2: int) -> int:
        """Add a triangle to the triangulation.

        Args:
            v0: First vertex index.
            v1: Second vertex index.
            v2: Third vertex index.

        Returns:
            Triangle index.
        """
        tri = TriangleData(vertices=(v0, v1, v2))
        tri_idx = len(self.triangles)
        self.triangles.append(tri)

        self._update_triangle_circumcircle(tri_idx)

        edge0 = self._get_edge(v1, v2)
        edge1 = self._get_edge(v2, v0)
        edge2 = self._get_edge(v0, v1)

        self._add_edge_to_triangle(edge0, tri_idx)
        self._add_edge_to_triangle(edge1, tri_idx)
        self._add_edge_to_triangle(edge2, tri_idx)

        return tri_idx

    def _remove_triangle(self, tri_idx: int) -> None:
        """Remove a triangle from the triangulation.

        Args:
            tri_idx: Triangle index.
        """
        if tri_idx >= len(self.triangles):
            return

        triangle = self.triangles[tri_idx]
        v0, v1, v2 = triangle.vertices

        edge0 = self._get_edge(v1, v2)
        edge1 = self._get_edge(v2, v0)
        edge2 = self._get_edge(v0, v1)

        self._remove_edge_from_triangle(edge0, tri_idx)
        self._remove_edge_from_triangle(edge1, tri_idx)
        self._remove_edge_from_triangle(edge2, tri_idx)

        self.triangles[tri_idx] = None

    def _flip_edge(self, edge: Edge) -> bool:
        """Flip an edge if it violates Delaunay property.

        Args:
            edge: Edge to potentially flip.

        Returns:
            True if edge was flipped.
        """
        if edge not in self.edge_to_triangles:
            return False

        triangles = self.edge_to_triangles[edge]
        if len(triangles) != 2:
            return False

        tri1_idx, tri2_idx = triangles[0], triangles[1]
        tri1 = self.triangles[tri1_idx]
        tri2 = self.triangles[tri2_idx]

        v1, v2 = edge
        tri1_verts = list(tri1.vertices)
        tri2_verts = list(tri2.vertices)

        v3 = None
        for v in tri1_verts:
            if v != v1 and v != v2:
                v3 = v
                break

        v4 = None
        for v in tri2_verts:
            if v != v1 and v != v2:
                v4 = v
                break

        if v3 is None or v4 is None:
            return False

        if self._point_in_circumcircle(self.points[v4], tri1):
            self._remove_triangle(tri1_idx)
            self._remove_triangle(tri2_idx)

            new_tri1_idx = self._add_triangle(v1, v3, v4)
            new_tri2_idx = self._add_triangle(v2, v3, v4)

            self.triangles[new_tri1_idx].neighbors[0] = new_tri2_idx
            self.triangles[new_tri2_idx].neighbors[0] = new_tri1_idx

            new_edge = self._get_edge(v3, v4)
            if new_edge in self.edge_to_triangles:
                for neighbor_idx in self.edge_to_triangles[new_edge]:
                    if neighbor_idx != new_tri1_idx and neighbor_idx != new_tri2_idx:
                        if self.triangles[neighbor_idx].neighbors[0] is None:
                            self.triangles[neighbor_idx].neighbors[0] = new_tri1_idx
                        elif self.triangles[neighbor_idx].neighbors[1] is None:
                            self.triangles[neighbor_idx].neighbors[1] = new_tri1_idx
                        else:
                            self.triangles[neighbor_idx].neighbors[2] = new_tri1_idx

            return True

        return False

    def _legalize_edges(self, point_idx: int, bad_triangles: List[int]) -> None:
        """Legalize edges after point insertion using edge flipping.

        Args:
            point_idx: Index of inserted point.
            bad_triangles: List of triangle indices to check.
        """
        edges_to_check: List[Edge] = []
        checked_edges: Set[Edge] = set()

        for tri_idx in bad_triangles:
            if tri_idx >= len(self.triangles):
                continue
            triangle = self.triangles[tri_idx]
            v0, v1, v2 = triangle.vertices

            if point_idx in (v0, v1, v2):
                edge1 = self._get_edge(v0, v1)
                edge2 = self._get_edge(v1, v2)
                edge3 = self._get_edge(v2, v0)

                for edge in [edge1, edge2, edge3]:
                    if point_idx not in edge and edge not in checked_edges:
                        edges_to_check.append(edge)
                        checked_edges.add(edge)

        while edges_to_check:
            edge = edges_to_check.pop(0)
            if self._flip_edge(edge):
                if edge in self.edge_to_triangles:
                    for tri_idx in self.edge_to_triangles[edge]:
                        if tri_idx < len(self.triangles):
                            v0, v1, v2 = self.triangles[tri_idx].vertices
                            new_edge1 = self._get_edge(v0, v1)
                            new_edge2 = self._get_edge(v1, v2)
                            new_edge3 = self._get_edge(v2, v0)

                            for new_edge in [new_edge1, new_edge2, new_edge3]:
                                if (
                                    new_edge != edge
                                    and new_edge not in checked_edges
                                    and new_edge in self.edge_to_triangles
                                    and len(self.edge_to_triangles[new_edge]) == 2
                                ):
                                    edges_to_check.append(new_edge)
                                    checked_edges.add(new_edge)

    def construct(self) -> List[Triangle]:
        """Construct Delaunay triangulation using incremental insertion.

        Returns:
            List of triangles (vertex indices).
        """
        if len(self.points) < 3:
            return []

        if len(self.points) == 3:
            self._add_triangle(0, 1, 2)
            return self.get_triangles()

        sorted_indices = sorted(
            range(len(self.points)), key=lambda i: self.points[i][0]
        )

        first_three = sorted_indices[:3]
        self._add_triangle(first_three[0], first_three[1], first_three[2])

        for i in range(3, len(sorted_indices)):
            point_idx = sorted_indices[i]
            point = self.points[point_idx]

            bad_triangles: List[int] = []
            for tri_idx, triangle in enumerate(self.triangles):
                if triangle is not None and self._point_in_circumcircle(point, triangle):
                    bad_triangles.append(tri_idx)

            polygon_edges: List[Edge] = []
            edge_counts: Dict[Edge, int] = {}

            for tri_idx in bad_triangles:
                if tri_idx >= len(self.triangles):
                    continue
                triangle = self.triangles[tri_idx]
                v0, v1, v2 = triangle.vertices

                edge1 = self._get_edge(v0, v1)
                edge2 = self._get_edge(v1, v2)
                edge3 = self._get_edge(v2, v0)

                for edge in [edge1, edge2, edge3]:
                    edge_counts[edge] = edge_counts.get(edge, 0) + 1

            for edge, count in edge_counts.items():
                if count == 1:
                    polygon_edges.append(edge)

            for tri_idx in reversed(sorted(bad_triangles)):
                if tri_idx < len(self.triangles) and self.triangles[tri_idx] is not None:
                    self._remove_triangle(tri_idx)

            for edge in polygon_edges:
                v1, v2 = edge
                new_tri_idx = self._add_triangle(point_idx, v1, v2)

            edges_to_legalize = []
            for tri_idx in range(len(self.triangles)):
                triangle = self.triangles[tri_idx]
                if point_idx in triangle.vertices:
                    v0, v1, v2 = triangle.vertices
                    edges_to_legalize.append(self._get_edge(v0, v1))
                    edges_to_legalize.append(self._get_edge(v1, v2))
                    edges_to_legalize.append(self._get_edge(v2, v0))

            checked_edges: Set[Edge] = set()
            while edges_to_legalize:
                edge = edges_to_legalize.pop(0)
                if edge in checked_edges:
                    continue
                checked_edges.add(edge)

                if point_idx in edge:
                    continue

                if self._flip_edge(edge):
                    if edge in self.edge_to_triangles:
                        for tri_idx in self.edge_to_triangles[edge]:
                            if tri_idx < len(self.triangles):
                                triangle = self.triangles[tri_idx]
                                if point_idx in triangle.vertices:
                                    v0, v1, v2 = triangle.vertices
                                    new_edge1 = self._get_edge(v0, v1)
                                    new_edge2 = self._get_edge(v1, v2)
                                    new_edge3 = self._get_edge(v2, v0)

                                    for new_edge in [new_edge1, new_edge2, new_edge3]:
                                        if (
                                            new_edge != edge
                                            and new_edge not in checked_edges
                                            and point_idx not in new_edge
                                        ):
                                            edges_to_legalize.append(new_edge)

        return [
            tri.vertices
            for tri in self.triangles
            if tri is not None
        ]

    def get_edges(self) -> List[Edge]:
        """Get all edges in the triangulation.

        Returns:
            List of edges (vertex index pairs).
        """
        edges: List[Edge] = []
        seen: Set[Edge] = set()

        for triangle in self.triangles:
            if triangle is None:
                continue
            v0, v1, v2 = triangle.vertices
            edge1 = self._get_edge(v0, v1)
            edge2 = self._get_edge(v1, v2)
            edge3 = self._get_edge(v2, v0)

            for edge in [edge1, edge2, edge3]:
                if edge not in seen:
                    edges.append(edge)
                    seen.add(edge)

        return edges

    def get_triangles(self) -> List[Triangle]:
        """Get all triangles in the triangulation.

        Returns:
            List of triangles (vertex index triples).
        """
        return [
            tri.vertices
            for tri in self.triangles
            if tri is not None
        ]


def main() -> None:
    """Main function to run the Delaunay triangulation CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Delaunay triangulation with incremental insertion and edge flipping"
    )
    parser.add_argument(
        "--points",
        type=str,
        required=True,
        help="Points in format 'x1,y1;x2,y2;...'",
    )
    parser.add_argument(
        "--edges",
        action="store_true",
        help="Show edges",
    )

    args = parser.parse_args()

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

        print(f"Input points: {points}")
        print(f"Number of points: {len(points)}")

        dt = DelaunayTriangulation(points)
        triangles = dt.construct()

        print(f"\nDelaunay Triangulation:")
        print(f"Number of triangles: {len(triangles)}")
        for i, triangle in enumerate(triangles):
            v0, v1, v2 = triangle
            print(f"  Triangle {i+1}: ({v0}, {v1}, {v2}) -> "
                  f"{points[v0]}, {points[v1]}, {points[v2]}")

        if args.edges:
            edges = dt.get_edges()
            print(f"\nEdges: {len(edges)}")
            for i, edge in enumerate(edges):
                v1, v2 = edge
                print(f"  Edge {i+1}: ({v1}, {v2}) -> {points[v1]}, {points[v2]}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
