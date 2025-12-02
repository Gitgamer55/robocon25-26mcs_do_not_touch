import math


cpos = [0,0]
#The current position of the robot on a unit grid

cdir = [0,1]
#The current direction our robot is facing, stored as a basis vector with a length of 1 unit

cdir_angle = 90 
#The angle of the cdir vector from the x-axis

home_coords = [-3,-3]
#The position of our home base

tag_map = {
    
    "up" : [0,-1],
    "down" : [0,1],
    "right" : [1,0],
    "left" : [-1,0],
}



orientation_map = {
    1 : [1,1],
    2 : [1,-1],
    3 : [-1,-1],
    4 : [-1,1],
    }


def correct_pos():
    if cpos[0] > 3:
        cpos[0] = 3
    elif cpos[0] < -3:
        cpos[0] = -3
    elif cpos[1] > 3:
        cpos[1] = 3
    elif cpos[-1] < -3:
        cpos[1] = -3
    
    if cpos[0] < 0.000001:
        cpos[0] = 0
    if cpos[1] < 0.000001:
        cpos[1] = 0
    

def rotate_vector(vector, angle_degrees):
    x = vector[0]
    y = vector[1]
    angle_radians = math.radians(angle_degrees)
    
    #Use the rotation matrix
    
    x_rot = x * math.cos(angle_radians) - y * math.sin(angle_radians)
    y_rot = x * math.sin(angle_radians) + y * math.cos(angle_radians)

    return [x_rot, y_rot]

def update_dir_generic(angle,forward):
    #Change the direction the robot is facing using the rotate_vector function
    global cdir
    global cdir_angle
    if forward:
        cdir = rotate_vector(cdir,angle)
        cdir_angle += angle
    if not forward:
        cdir = rotate_vector(cdir,(360-angle))
        cdir_angle -= angle
        
    if cdir_angle < 0:
        cdir_angle += 360
    elif cdir_angle > 359:
        cdir_angle %= 360

    
def update_pos_generic(dist):
    global cpos
    global cdir
    #It will update the position of our robot on a unit grid using the direction we are facing and the distance the robot moves
    npos = [cdir[0] * dist , cdir[1] * dist]
    cpos = [cpos[0] + npos[0] , cpos[1] + npos[1]]

        
def vectorcon(dist,angle):
    """
    It takes the following parametres:
        -The distance of the line.
        -The angle of the line from the x axis
        -The quarter of its surrounding its on.(Explained below)
        
                                |						-The function converts a line and angle (polar vector) into a cartesian 
                        4       |		1				vector that faces the designated corner of the arena.
                                |
                                |
                ________________|________________
                                |
                                |
                        3       |		2
                                |
    """
    angle %= 360
    if 90 < angle < 180:
        orientation = 4
    elif 180 < angle < 270:
        orientation = 3
    elif 270 < angle < 360:
        orientation = 2
    else:
        orientation = 1
    angle %= 90
    f = orientation_map[orientation]
    if orientation == 1:
        vector = [(dist * math.sin(angle)),(dist * math.cos(angle))]
    else:
        vector = [(dist * math.cos(angle) * f[0]),(dist * math.sin(angle) * f[1])]
    return vector

def update_ALL(dist,bearing,rotation,tag):
    global cdir
    global cdir_angle
    global cpos
    
    if tag[0] == -3:
        tag_type = "right"
    elif tag[0] == 3:
        tag_type = "left"
    elif tag[1] == -3:
        tag_type = "down"
    elif tag[1] == 3:
        tag_type = "up"
    
    if rotation < 0:
        rotation += 360
    tag_dir = tag_map[tag_type]
    tag_dir = rotate_vector(tag_dir,rotation)
    vector_guide = [tag_dir[0] * dist , tag_dir[1] * dist]
    cpos = [cpos[0] + vector_guide[0] , cpos[1] + vector_guide[1]]
    cdir_angle = (bearing + 90 - rotation) % 360
    cdir = vectorcon(1,cdir_angle)

def angle_coords(Pos1, Pos2, Dir):
    #This section is ChatGPT I will make it easier to read at some point (;
    """
    Pos1: (x1, y1)  - starting point
    Pos2: (x2, y2)  - target point
    Dir:  (dx, dy)  - current direction vector (centered at Pos1)

    Returns:
        angle (float): signed angle in radians to rotate Dir so it aligns
                       with the vector from Pos1 to Pos2.
    """
    x1, y1 = Pos1
    x2, y2 = Pos2
    dx_dir, dy_dir = Dir

    # Vector from Pos1 to Pos2 (target direction)
    vx = x2 - x1
    vy = y2 - y1

    # Check for degenerate case: Pos1 == Pos2
    if vx == 0 and vy == 0:
        raise ValueError("Pos1 and Pos2 are the same point; direction is undefined.")

    # Normalise target vector
    mag_v = math.hypot(vx, vy)
    vx /= mag_v
    vy /= mag_v

    # Normalise Dir (in case it's not exactly length 1)
    mag_dir = math.hypot(dx_dir, dy_dir)
    if mag_dir == 0:
        raise ValueError("Dir vector has zero length.")
    dx_dir /= mag_dir
    dy_dir /= mag_dir

    # Dot product and "2D cross product" (determinant)
    dot = dx_dir * vx + dy_dir * vy
    det = dx_dir * vy - dy_dir * vx

    # atan2(det, dot) gives signed angle from Dir -> target
    angle = math.atan2(det, dot)

    return math.degrees(angle)

update_ALL(5,60,52,[3,2])
update_dir_generic(angle_coords(cpos,[0,0],cdir),True)
update_pos_generic(math.sqrt(cpos[0] ** 2 + cpos[1] ** 2))
correct_pos()
print(f"Current position: {cpos}. Current direction: {cdir}")
