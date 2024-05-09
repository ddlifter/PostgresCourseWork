IsAdmin = True
def change(role):
    global IsAdmin
    if role == "admin":
        IsAdmin = True
    else:
        IsAdmin = False
            