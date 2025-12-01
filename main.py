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


r = robot.Robot()
start = time.perf_counter()

def run_supply_drop_sequence():
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

        # Use Kaan's vectors and stuff (placeholder)
        apply_kaans_vectors()

        go_home()

        unload_stack()


# --- Placeholder functions you must implement ---
def proximity_timer_triggered():
    end = time.perf_counter()
    time =  120 - (start - end) #This assumes each round is 2 minutes - CHANGE IF NOT!
    
    if time < 35: # CAN CHANGE
        return True
    return False
    

def go_to_centre():
    pass

def scan():
    pass

def target_found():
    return False

def turn(deg):
    pass

def go_forward_to_box():
    pass

def apply_kaans_vectors():
    pass

def go_home():
    pass

def unload_stack():
    pass


# Example entry point
if __name__ == "__main__":
    run_supply_drop_sequence()
