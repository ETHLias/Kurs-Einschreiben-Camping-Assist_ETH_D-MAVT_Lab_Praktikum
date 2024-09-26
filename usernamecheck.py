
# 2023-03-08

#user = ''

usernames = "||admin_example_1||user_example_2||" \
            ""

def check_user_registration(user):

    if user == '':
        return False

    checker = "||" + user + "||"

    if checker in usernames:
        return True
    return False


#print(check_user_registration(user))