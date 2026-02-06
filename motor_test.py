import robot

from time import sleep

r = robot.Robot()

r.enable_12v = True

import math

cpos = [0,0]
#The current position of the robot on a unit grid

cdir = [0,1]
#The current direction our robot is facing, stored as a basis vector with a length of 1 unit

tag_id = {
    100:[-2.5,3],
    101:[-1.5,3],
    102:[-0.5,3],
    103:[0.5,3],
    104:[1.5,3],
    105:[2.5,3],
    106:[3,2.5],
    107:[3,1.5],
    108:[3,0.5],
    109:[3,-0.5],
    110:[3,-1.5],
    111:[3,-2.5],
    112:[2.5,-3],
    113:[1.5,-3],
    114:[0.5,-3],
    115:[-0.5,-3],
    116:[-1.5,-3],
    117:[-2.5,-3],
    118:[-3,-2.5],
    119:[-3,-1.5],
    120:[-3,-0.5],
    121:[-3,0.5],
    122:[-3,1.5],
    123:[-3,2.5]
}


tag_map = {
    
    "up" : [0,-1],
    "down" : [0,1],
    "right" : [-1,0],
    "left" : [1,0],
}



orientation_map = {
    0 : [1,1],
    1 : [1,-1],
    2 : [-1,-1],
    3 : [-1,1],
    }


def correct_pos():
    # Use min/max for faster clamping - avoids multiple conditionals
    cpos[0] = max(-3, min(3, cpos[0]))
    cpos[1] = max(-3, min(3, cpos[1]))
    
    # Optimized epsilon check - use abs() and single comparison
    if abs(cpos[0]) < 0.000001:
        cpos[0] = 0
    if abs(cpos[1]) < 0.000001:
        cpos[1] = 0
    

def rotate_vector(vector, angle_degrees):
    # Inline negation to avoid extra assignment
    angle_radians = math.radians(-angle_degrees)
    
    # Pre-calculate sin/cos once instead of calling twice
    cos_a = math.cos(angle_radians)
    sin_a = math.sin(angle_radians)
    
    x_rot = vector[0] * cos_a - vector[1] * sin_a
    y_rot = vector[0] * sin_a + vector[1] * cos_a

    return [x_rot, y_rot]




def update_dir(angle):
    #Change the direction the robot is facing using the rotate_vector function
    global cdir
    # Use else to avoid redundant check - only one branch executes
    cdir = rotate_vector(cdir, angle)
        

    
def update_pos(dist):
    global cpos
    global cdir
    #It will update the position of our robot on a unit grid using the direction we are facing and the distance the robot moves
    # Eliminate intermediate list creation - update in place
    cpos[0] += cdir[0] * dist
    cpos[1] += cdir[1] * dist

        
def vectorcon(dist,angle):
    global orientation_map
    angle %= 360
    orientation = angle // 90
    angle %= 90
    # Cache orientation multipliers to avoid multiple dictionary lookups
    orient = orientation_map[orientation]
    if orientation % 2 != 0:
        angle = 90 - angle
    # Pre-calculate radian conversion once
    angle_rad = math.radians(angle)
    # Calculate and apply orientation in one step
    return [math.cos(angle_rad) * dist * orient[0], math.sin(angle_rad) * dist * orient[1]]

def update_ALL(dist,bearing,rotation,tag):
    global cdir
    global cpos
    global tag_id
    # Optimize tag_type lookup - use dictionary for O(1) lookup instead of if-elif chain
    # This assumes tag coordinates are exactly -3 or 3
    tag = tag_id[tag]
    if tag[0] == -3:
        tag_type = "left"
    elif tag[0] == 3:
        tag_type = "right"
    elif tag[1] == -3:
        tag_type = "down"
    elif tag[1] == 3:
        tag_type = "up"
    
    if rotation < 0:
        rotation += 360
    tag_dir = tag_map[tag_type]
    tag_dir = rotate_vector(tag_dir, rotation)
    # Calculate vector_guide once and reuse
    vg_x = tag_dir[0] * dist
    vg_y = tag_dir[1] * dist
    cpos[0] = tag[0] + vg_x
    cpos[1] = tag[1] + vg_y
    # Optimize: avoid division then negation - just negate the normalized direction
    vector_guide = [-tag_dir[0], -tag_dir[1]]
    if bearing < 0:
        bearing += 360
    
    cdir = rotate_vector(vector_guide, -bearing)

def work_to_coords(dest):
    # Calculate differences once
    dx = dest[0] - cpos[0]
    dy = dest[1] - cpos[1]
    length = math.hypot(dx, dy)  # Inline dist_between to avoid function call overhead
    
    # Avoid division by zero
    if length == 0:
        return [0, 0]
    
    # Normalize vector
    inv_length = 1.0 / length
    vx = dx * inv_length
    vy = dy * inv_length
    
    # Calculate dot product and determinant (fixed: det should be cross product)
    dot = vx * cdir[0] + vy * cdir[1]
    det = vx * cdir[1] - vy * cdir[0]  # Fixed: proper cross product for 2D
    
    # Inline negation
    angle = -math.degrees(math.atan2(det, dot))
    return [length, angle]
    
    
def dist_between(pos1,pos2):
    # Already optimal - math.hypot is fast and handles edge cases
    # Could inline if only called once, but keeping for reusability
    return math.hypot(pos1[0]-pos2[0], pos1[1]-pos2[1])


def move(dist, speed):
    # Motor 0 is right
    # Motor 1 is left
    if dist > 0:
        r.motors[0] = 495 * (speed / 100)
        r.motors[1] = 500 * (speed / 100)
    elif dist < 0:
        r.motors[0] = -495 * (speed / 100)
        r.motors[1] = -500 * (speed / 100)
    t = (43 / speed) * abs(dist) 
    print(f"Time to sleep: {t} For {abs(dist)} metres")
    sleep(t)
    r.motors[0] = 0
    r.motors[1] = 0
    update_pos(dist)


def turn(deg, speed):
    if deg > 0:
        r.motors[0] = -495 * (speed / 100)
        r.motors[1] = 500 * (speed / 100)
    else:
        r.motors[0] = 495 * (speed / 100)
        r.motors[1] = -500 * (speed / 100)
    sleep(abs((0.3)/90*deg))
    r.motors[0] = 0
    r.motors[1] = 0
    update_dir(deg)

cpos = [-1,2]
cdir = [1,0]
move(1, 40)
sleep(0.5)
turn(90, 40)
sleep(0.5)
move(3, 40)
sleep(0.5)
turn(-45, 40)
sleep(0.5)
move(1.4, 40)
sleep(0.5)
turn(-45, 40)
sleep(0.5)
move(-2, 40)
sleep(0.5)
move(2, 40)
sleep(0.5)

print(round(cpos[0], 1), round(cpos[1], 1))
print(round(cdir[0], 1), round(cdir[1], 1))
