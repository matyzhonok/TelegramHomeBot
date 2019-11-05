auth_user = {}
auth_user[291335695] = "Витя"
auth_user[896436298] = "Маша"
auth_user[566283560] = "Андрей"

def isAuthorized (user_id):
    if user_id in auth_user:
        return True
    else:
        return False

def getName (user_id):
    return auth_user[user_id]

def getUserList ():
    return auth_user