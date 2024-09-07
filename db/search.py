from db import Query


# returns an array of dictionaries containing items related to the input
def search(search_term:str) -> dict[str, list]:
    query = Query()
    search_results: dict[str, list] = {
        "users": [],
        "blogs": []
    }

    # checks if input is similar to any usernames in 'users'
    users: list = query.search_users(search_term=search_term)
    if users:
        search_results["users"] = users

    # checks if input is similar to any to blog titles or corpi in 'blogs'
    blogs: list = query.search_blogs(search_term=search_term)
    if blogs:
        search_results["blogs"] = blogs

    return search_results
