from db import Query


# returns an array of dictionaries containing items related to the input
def search(search_text):
    query = Query()
    search_results = {
        "users": None,
        "blogs": None
    }

    # checks if input is similar to any usernames in 'users'
    res2 = query.search_usernames(search_text)
    if res2:
        search_results["users"] = res2

    # checks if input is similar to any to blog titles or corpi in 'blogs'
    res3 = query.search_blogs(search_text)
    if res3:
        search_results["blogs"] = res3

    return search_results
