from db import Query


# returns an array of dictionaries containing items related to the input
def search(search_term):
    query = Query()
    search_results = {
        "users": None,
        "blogs": None
    }

    # checks if input is similar to any usernames in 'users'
    users = query.search_users(search_term=search_term)
    if users:
        search_results["users"] = users

    # checks if input is similar to any to blog titles or corpi in 'blogs'
    blogs = query.search_blogs(search_term=search_term)
    if blogs:
        search_results["blogs"] = blogs

    return search_results
