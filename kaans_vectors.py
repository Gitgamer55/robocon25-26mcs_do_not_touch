import math
import robot
from time import *


'''
Copyrighted by the UPRC (Ultra - Power Richard Company). Any plagerism from AI 
is a direct violation to the UPRC's Copyright Laws which
can be viewed in the "plagerism violations" section on the main website
'''

'''
UPDATE:

- ALL MOTORS ARE NEGATIVE. You do not want to accidentally go backwards.
- MAIN HAS BEEN IMPLEMENTED
- CONCERNS
    - Can we scan tags effectively?
'''

team = "blue"
c = (1 / 0.75) / 1.18

r = robot.Robot()
r.enable_12v = True

r.gpio[2].mode = robot.OUTPUT
r.gpio[1].mode = robot.OUTPUT

cpos = [0,0]
#The current position of the robot on a unit grid

cdir = [0,1]
#The current direction our robot is facing, stored as a basis vector with a length of 1 unit

tag_id = {}
tag_blue = {
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

tag_red = {
    100:tag_blue[118],
    101:tag_blue[119],
    102:tag_blue[120],
    103:tag_blue[121],
    104:tag_blue[122],
    105:tag_blue[123],
    106:tag_blue[100],
    107:tag_blue[101],
    108:tag_blue[102],
    109:tag_blue[103],
    110:tag_blue[104],
    111:tag_blue[105],
    112:tag_blue[106],
    113:tag_blue[107],
    114:tag_blue[108],
    115:tag_blue[109],
    116:tag_blue[110],
    117:tag_blue[111],
    118:tag_blue[112],
    119:tag_blue[113],
    120:tag_blue[114],
    121:tag_blue[115],
    122:tag_blue[116],
    123:tag_blue[117],
}

tag_yellow = {
    100:tag_blue[112],
    101:tag_blue[113],
    102:tag_blue[114],
    103:tag_blue[115],
    104:tag_blue[116],
    105:tag_blue[117],
    106:tag_blue[118],
    107:tag_blue[119],
    108:tag_blue[120],
    109:tag_blue[121],
    110:tag_blue[122],
    111:tag_blue[123],
    112:tag_blue[100],
    113:tag_blue[101],
    114:tag_blue[102],
    115:tag_blue[103],
    116:tag_blue[104],
    117:tag_blue[105],
    118:tag_blue[106],
    119:tag_blue[107],
    120:tag_blue[108],
    121:tag_blue[109],
    122:tag_blue[110],
    123:tag_blue[111],
}

tag_green = {
    100:tag_blue[106],
    101:tag_blue[107],
    102:tag_blue[108],
    103:tag_blue[109],
    104:tag_blue[110],
    105:tag_blue[111],
    106:tag_blue[112],
    107:tag_blue[113],
    108:tag_blue[114],
    109:tag_blue[115],
    110:tag_blue[116],
    111:tag_blue[117],
    112:tag_blue[118],
    113:tag_blue[119],
    114:tag_blue[120],
    115:tag_blue[121],
    116:tag_blue[122],
    117:tag_blue[123],
    118:tag_blue[100],
    119:tag_blue[101],
    120:tag_blue[102],
    121:tag_blue[103],
    122:tag_blue[104],
    123:tag_blue[105],
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


if team == "blue":
    tag_id = tag_blue
elif team == "red":
    tag_id = tag_red
elif team == "green":
    tag_id = tag_green
else:
    team_id = tag_yellow

def correct_pos():
    cpos[0] = max(-3, min(3, cpos[0]))
    cpos[1] = max(-3, min(3, cpos[1]))
    
    
    if abs(cpos[0]) < 0.000001:
        cpos[0] = 0
    if abs(cpos[1]) < 0.000001:
        cpos[1] = 0
    

def rotate_vector(vector, angle_degrees):
    
    angle_radians = math.radians(-angle_degrees)
    
    
    cos_a = math.cos(angle_radians)
    sin_a = math.sin(angle_radians)
    
    x_rot = vector[0] * cos_a - vector[1] * sin_a
    y_rot = vector[0] * sin_a + vector[1] * cos_a

    return [x_rot, y_rot]




def update_dir(angle,clockwise):
    
    global cdir
    
    if clockwise:
        cdir = rotate_vector(cdir, angle)
    else:
        cdir = rotate_vector(cdir, -angle)
        

    
def update_pos(dist):
    global cpos
    global cdir
    
    cpos[0] += cdir[0] * dist
    cpos[1] += cdir[1] * dist

        
def vectorcon(dist,angle):
    global orientation_map
    angle %= 360
    orientation = angle // 90
    angle %= 90
    
    orient = orientation_map[orientation]
    if orientation % 2 != 0:
        angle = 90 - angle
    
    angle_rad = math.radians(angle)
    
    return [math.cos(angle_rad) * dist * orient[0], math.sin(angle_rad) * dist * orient[1]]

def update_ALL(dist,bearing,rotation,tag):
    global cdir
    global cpos
    global tag_id
    
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
    
    vg_x = tag_dir[0] * dist
    vg_y = tag_dir[1] * dist
    cpos[0] = tag[0] + vg_x
    cpos[1] = tag[1] + vg_y
    
    vector_guide = [-tag_dir[0], -tag_dir[1]]
    if bearing < 0:
        bearing += 360
    
    
    cdir = rotate_vector(vector_guide, bearing)

def work_to_coords(dest):
    
    dx = dest[0] - cpos[0]
    dy = dest[1] - cpos[1]
    length = math.hypot(dx, dy)  
    
    
    if length == 0:
        return [0, 0]
    
    
    inv_length = 1.0 / length
    vx = dx * inv_length
    vy = dy * inv_length
    
   
    dot = vx * cdir[0] + vy * cdir[1]
    det_cw = vy * cdir[0] - vx * cdir[1]
    angle = -math.degrees(math.atan2(det_cw, dot))
    return [length, angle]
    
def work_to_dir(direction):
    cx, cy = cdir
    dx, dy = direction

    dot = cx * dx + cy * dy
    determinant = cx * dy - cy * dx

    angle = math.degrees(math.atan2(determinant, dot))
    return -angle
    
def dist_between(pos1,pos2):
    return math.hypot(pos1[0]-pos2[0], pos1[1]-pos2[1])


def move(dist):
    global c
    # Motor 0 is right
    # Motor 1 is left

    if dist > 0:
        r.motors[0] = 490 * 0.5 * c
        r.motors[1] = 500 * 0.5 * c
    elif dist < 0:
        r.motors[0] = -490 * 0.5 * c
        r.motors[1] = -500 * 0.5 * c
    else:
        return

    delay = (82 / 50) * abs(dist)
    print(f"Time to move: {delay} for {abs(dist)} metres")

    r.gpio[0].mode = robot.INPUT

    startTime = perf_counter()
    endTime = startTime + delay
    stateThen = r.gpio[0].digital
    lastChangeTime = startTime

    while perf_counter() < endTime:
        stateNow = r.gpio[0].digital
        now = perf_counter()
        if stateNow != stateThen:
            timeSinceLastChange = now - lastChangeTime
            totalTime = now - startTime
            stateThen = stateNow
            lastChangeTime = now
            

        if now - lastChangeTime > 3:
            print("stuck")
            r.motors[0] = 495 * 0.5
            r.motors[1] = 500 * 0.5
            sleep(1)
            r.motors[0] = 0
            r.motors[1] = 0
            return

            '''
            We must rescan and know our position after we have backed out ourselves from a robot or something.
            I wrote sample code to what we could do after we collide (reverse ourselves) and 
            this can obviously easily be changed if we agree to something different.
            We should also agree on how long we reverse for.
            '''

    r.motors[0] = 0
    r.motors[1] = 0
    update_pos(dist)


def turn(deg, speed=50):
    if deg > 0:
        r.motors[0] = -495 * (speed / 100)
        r.motors[1] = 500 * (speed / 100)
    else:
        r.motors[1] = -500 * (speed / 100)
        r.motors[0] = 495 * (speed / 100)
    t = abs(0.178/90*deg) / (speed / 100)
    print(f"Time to sleep: {t} For {deg} degrees")
    sleep(t)
    r.motors[0] = 0
    r.motors[1] = 0
    print(deg)
    update_dir(deg,True)


def scan():
    '''
    This is Richard's work 2026
    '''
    global last_markers

    markers = r.see()
    last_markers = []

    for m in markers:
        mtype = m.info.type
        if mtype in ("CRATE", "DROP"):
            last_markers.append(m)

def find_box():
    markers = r.see()
    if len(markers) == 0:
        return False
    marker = markers[0]
    print("Found marker: info:", marker)
    turn(float(marker.bearing.y), 50)
    sleep(.25)
    print(f"Marker info: {float(marker.bearing.y), float(marker.dist)}")
    if float(marker.dist) > 1:
        disctance = float(marker.dist) / 2.5
        move(disctance)
        sleep(.5)
        markers = r.see()
        if len(markers) == 0:
            move(disctance)
        else:
            marker = markers[0]
            turn(float(marker.bearing.y), 50)
            sleep(.25)
            print(f"Marker info: {float(marker.bearing.y), float(marker.dist)}")
            
            move((float(marker.dist)) + 0.1)
        move(0.3)
    else:
        move((float(marker.dist)) + 0.1)
    return True


cpos = [-2.5,-2.5]
cdir = [1,0]

starttime = time.perf_counter()
boxes = 0
    
while boxes < 4 or (time.perf_counter() - starttime) <= 160.0:
    update_ALL()
    go = work_to_coords([0, 0])
    turn(go[1])
    move(go[0])
    update_ALL()
    temp = 0
    while temp < 360:
        if find_box():
            break
        temp += 30
        turn(30, 100)
go = work_to_coords([-2.5, -2.5])
turn(go[1])
move(go[0])  

