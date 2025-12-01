'''
Bot Yueyue Pseudocode:

    Repeat until proximity timer (supply drop):
        Go to centre
        Repeat until target:
        Scan
            if target break
            Turn 15
        Go forward to box
        Use Kaan's vectors and stuff
        Go to home
        Unload (stack?)

'''

import robot
import time
import kaans_vectors

r = robot.Robot()
start = time.perf_counter()

# --- Placeholder functions you must implement ---
def proximity_timer_triggered():
    end = time.perf_counter()
    time =  120 - (start - end) #This assumes each round is 2 minutes - CHANGE IF NOT!
    
    if time < 35: # CAN CHANGE
        return True
    return False
    

def go_to_centre():
    '''
    TODO implement going to centre - Yueyue 2025
    '''
    pass

def scan():
    """
    THIS IS MY WORK - Yueyue 2025
    """
    global last_markers

    markers = r.see()
    last_markers = []

    for m in markers:
        mtype = m.info.type
        if mtype in ("CRATE", "DROP"):
            last_markers.append(m)


def target_found():
    """
    ALSO MINE - Yueyue 2025
    """
    global last_markers
    return len(last_markers) > 0

def turn(deg):
    pass

def go_forward_to_box():
    """
    ALSO MINE - Yueyue 2025
    """
    global last_markers
    if target_found():
        for target in last_markers:
            turn(target.bearing.y)


def apply_kaans_vectors():
    '''
    TODO implement vector handling - Yueyue 2025
    '''
    pass

def go_home():
    '''
    TODO implement going home - Yueyue 2025
    '''
    pass

def unload_stack():
    '''
    TODO implement unloading - Yueyue 2025
    '''
    pass


def run_supply_drop_sequence():
    apply_kaans_vectors()
    # Repeat until proximity timer (supply drop)
    while not proximity_timer_triggered():
        
        go_to_centre()

        # Repeat until target found
        while True:
            scan()
            if target_found():
                break
            turn(15)

        go_forward_to_box()

        go_home()

        unload_stack()


# Example entry point
if __name__ == "__main__":
    run_supply_drop_sequence()
