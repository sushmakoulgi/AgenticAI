

from tools import get_current_timestamp,roll_dice,generate_password,read_text_file
from tool_manager import decide_tool


print("Current Timestamp:", get_current_timestamp())
print(roll_dice(3))
print(generate_password())
print(decide_tool("time"))
print(read_text_file("Data/notes.txt"))