from db import Query
from random import randint

def random():
    query = Query()
    number_of_users = query.select_users(order="DESC", limit=1)[0]["user_id"] - 1

    loops = 0
    while loops < 100:
        loops += 1
        try:
            random_user = query.select_users(user_id=randint(0, number_of_users))[0]

            if random_user["visible"]:
                return random_user
        
        except IndexError:
            pass
    
    