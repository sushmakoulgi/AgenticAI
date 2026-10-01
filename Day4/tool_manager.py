from tools import generate_password,get_current_timestamp,roll_dice

def decide_tool(user_input):
    if "time" in user_input.lower():
        return get_current_timestamp()
    if "dice" in user_input.lower():
        return roll_dice()
    if "password" in user_input.lower():
        return generate_password()
    return None
    

