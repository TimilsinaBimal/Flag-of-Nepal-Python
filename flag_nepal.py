import pygame
import math


# Screen Dimensions
HEIGHT = 600
WIDTH = 800

# Screen Colors
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLUE = (0, 56, 147)

# Starting Points
initial_x = 240
initial_y = 510
distance_AB = 324

PI = math.pi


def prepare_screen():
    """
    Create the initial screen.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    pygame.display.set_caption("Flag of Nepal")
    icon = pygame.image.load('flag.png')
    pygame.display.set_icon(icon)
    return screen


def distance(A: tuple, B: tuple):
    """
    Calculates the distance between two points.
    """
    return math.sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)


def line(p1, p2):
    """Returns the coefficients of x , y and constant of given line."""
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def intersection(L1, L2):
    """Calculate the intersection point of given two lines using Cramer's Rule."""
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return int(x), int(y)
    else:
        return False


def distance_line_point(line, point):
    """Calculate the distance between a line and a point."""
    numerator = abs(line[0] * point[0] + line[1] * point[1] - line[2])
    denominator = math.sqrt(math.pow(line[0], 2) + math.pow(line[1], 2))
    return numerator / denominator


def get_intercetions(x0, y0, r0, x1, y1, r1):
    """Calculate the intersection points of two circles."""
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d = math.sqrt((x1-x0)**2 + (y1-y0)**2)

    # non intersecting
    if d > r0 + r1:
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0**2-r1**2+d**2)/(2*d)
        h = math.sqrt(r0**2-a**2)
        x2 = x0+a*(x1-x0)/d
        y2 = y0+a*(y1-y0)/d
        x3 = x2+h*(y1-y0)/d
        y3 = y2-h*(x1-x0)/d
        x4 = x2-h*(y1-y0)/d
        y4 = y2+h*(x1-x0)/d

        return (x3, y3), (x4, y4)


# Finding all required Points

A = (initial_x, initial_y)
B = (initial_x + distance_AB, initial_y)
C = (initial_x, initial_y - (distance_AB * 1.33))
D = (initial_x, initial_y - distance_AB)
temp_dist = distance_AB / math.sqrt(2)
E = (B[0] - temp_dist, initial_y - temp_dist)
F = (initial_x, E[1])
G = (B[0], F[1])
H = (initial_x + 0.25 * distance_AB, initial_y)
I = intersection(line(H, (H[0], H[1] - 1.5 * distance_AB)), line(C, G))
J = (C[0], C[1] + 0.5 * distance(C, F))
K = intersection(line(J, (J[0] + distance_AB, J[1])), line(C, G))
L = intersection(line(J, K), line(H, I))
M = intersection(line(J, G), line(H, I))
N = (M[0], M[1] + distance_line_point(line(B, D), M))
O = intersection(line(A, C), line(M, (M[0] - distance_AB, M[1])))
unknown_point = intersection(line(C, G), line(M, (M[0] + distance_AB, M[1])))
LM = math.sqrt((int(distance(L, N)))**2 -
               distance_line_point(line(O, unknown_point), L))
P = (M[0] - LM, M[1])
Q = (M[0] + LM, M[1])
R, S = get_intercetions(L[0], L[1], distance(L, N),
                        N[0], N[1], distance(M, N))
T = intersection(line(R, S), line(I, H))
U = (A[0], A[1] - distance(F, A)/2)
V = intersection(line(B, D), line(U, (U[0] + distance_AB, U[1])))
W = intersection(line(U, V), line(H, I))


def base_length(radius, angle):
    """Calculate the base length of triangle present in sun and moon."""
    return math.sqrt(2 * math.pow(radius, 2) -
                     2 * math.pow(radius, 2) * math.cos(angle))


def rotation(point1, point2, angle):
    """Rotate the point1 around point2 with given angle."""
    x, y = point1[0], point1[1]
    a, b = point2[0], point2[1]
    return (math.cos(angle) * (x - a) - math.sin(angle) * (y - b) + a, math.sin(angle) * (x - a) + math.cos(angle) * (y - b) + b)


def draw_triangles_round(n, height, startpoint, base_length, angle):
    """Draw the Triangles around Sun and Moon to look them Like Sun and Moon"""
    for i in range(n):
        endpoint = (startpoint[0], startpoint[1] - base_length)
        outer_point = (startpoint[0] + height,
                       startpoint[1] - base_length/2)
        rotated_end_point = rotation(endpoint, startpoint, -(i * (angle)))
        rotated_outer_point = rotation(
            outer_point, startpoint, -(i * (angle)))
        initial_poly = pygame.draw.polygon(
            screen, WHITE, (startpoint, rotated_end_point, rotated_outer_point))
        startpoint = rotated_end_point


def draw_skeleton():
    """Draw flag only using Lines"""
    AB = pygame.draw.line(screen, RED, A, B)
    AC = pygame.draw.line(screen, RED, A, C)
    BD = pygame.draw.line(screen, RED, B, D)
    FG = pygame.draw.line(screen, RED, F, G)
    CG = pygame.draw.line(screen, RED, C, G)
    HI = pygame.draw.line(screen, RED, H, I)
    JK = pygame.draw.line(screen, RED, J, K)
    JG = pygame.draw.line(screen, RED, J, G)
    Ounknown_point = pygame.draw.line(screen, RED, O, unknown_point)
    UV = pygame.draw.line(screen, RED, U, V)


def draw_moon(start_x, start_y, end_x, end_y):
    """Draws the Arc Part of Moon Filled with White Color"""
    for x in range(start_x, end_x+1):
        for y in range(start_y, end_y+1):
            if distance(M, (x, y)) <= MQ and distance(L, (x, y)) > LN:
                screen.set_at((x, y), WHITE)


# Calculate Radius
MN = int(distance(M, N))
LN = int(distance(L, N))
LN = int(distance(L, N))
MQ = int(distance(M, Q))
MN = int(distance(M, N))
TM = int(distance(T, M))
TS = int(distance(T, S))
TN = distance(T, N)

# Calculate Points for Border
outer_A = (A[0] - TN, A[1] + TN)
outer_C = (C[0] - TN, C[1] - 2 * TN)
outer_G = (G[0] + 3 * TN, G[1] + TN)
outer_E = (E[0] + 2 * TN, E[1] + TN)
outer_B = (B[0] + 2 * TN, B[1] + TN)


# Initialize Display
screen = prepare_screen()

# Draw Blue Border
pygame.draw.polygon(
    screen, BLUE, (outer_A, outer_C, outer_G, outer_E, outer_B, outer_A))

# Draw Red Shape Polygon Main Flag
inner_shape = pygame.draw.polygon(screen, RED, (A, C, G, E, B, A))
# inner_shape = pygame.draw.polygon(screen, RED, (A, C, G, E, B))
# Draw Sun and Moon Circles
pygame.draw.circle(screen, WHITE, T, TM, 0)
pygame.draw.circle(screen, WHITE, W, int(distance(M, N))+2, 0)


# Draw Triangles Around SUn
base_length_sun = base_length(MN, math.radians(30))
startpoint_sun = (W[0] + MN, W[1] + base_length_sun/2)
draw_triangles_round(12, (LN - MN),
                     startpoint_sun, base_length_sun, PI/6)

# Draw Triangles Around Moon
angle = math.radians(360/18)
base_length_moon = base_length(TM, angle)
startpoint_moon = (T[0] + TM - 0.52, T[1] + base_length_moon/2 + 1)
draw_triangles_round(11, (TS - TM), startpoint_moon,
                     base_length_moon, angle)

# Draw Moon
draw_moon((M[0] - MQ), (M[1] - LN), (M[0] + MQ), (M[0] + MQ))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
