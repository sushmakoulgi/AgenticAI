from tools import generate_password,get_current_timestamp,roll_dice,read_text_file

def decide_tool(user_input):
    if "time" in user_input.lower():
        return get_current_timestamp()
    if "dice" in user_input.lower():
        return roll_dice()
    if "password" in user_input.lower():
        return generate_password()
    if "summarize" in user_input.lower():
        filename=user_input.split(" ")[1]
        content= read_text_file(filename=filename)
        return f"Summarize following document with content {content}"
    if "ask" in  user_input.lower():
        args=user_input.split(maxsplit=2)
        print(args[1])
        print(args[2])
        content=read_text_file(filename=args[1])
        return f"Read the following document with content {content} , answer the question {args[2]} by only using provided content, if you dont find the answer, return 'couldnt find the answer"
    return None
    

