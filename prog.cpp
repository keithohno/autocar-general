
#include <iostream>
#include <list>

using namespace std;

// Pathfinding current strategy
// Input: 2D points where cones are, distance to left bound, distance to right bound
// Process:
//  Make a Voronoi diagram
//  Plan a path along the Voronoi

// TODO: winged edges
// TODO: delaunay
// TODO: voronoi
// TODO: pathfind from voronoi

class Point
{
public:
    int x;
    int y;

    Point(int x1, int y1)
    {
        x = x1;
        y = y1;
    }
};

/**
 * Find the next point to go to.
 * 
 * @param cones list of 2D points corresponding to cones (robot at origin)
 * @param left_bound space on the left
 * @param right_bound space on the right
 */
Point pathfind(list<Point> cones, int left_bound, int right_bound)
{
    // first combine points for cones and bounds
    // then get delaunay/voronoi
    // then pathfind along voronoi (choose fastest route that meets robot size allowance)
    return Point(0, 0);
}

list<Point> combine(list<Point> cones, int left_bound, int right_bound)
{
    list<Point> new_points;
    for (const auto &point : cones)
    {
        new_points.push_back(Point(p.x, p.y));
        new_points.push_back(Point(-left_bound, p.y));
        new_points.push_back(Point(right_bound, p.y));
    }
    return new_points;
}

int main()
{
    cout << "Hello\n";
}