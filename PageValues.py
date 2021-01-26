default_values = {"name": "Series Recommendation System"}
pages = {"login": {"url": "login.html",
                   "header": "Login Page"},
         "register": {"url": "register.html",
                      "header": "Register Page"},
         "search": {"url": "search.html",
                    "header": "Search Page"},
         "results": {"url": "results.html",
                     "header": "Results Page"},
         "like": {"url": "like.html",
                  "header": "Like Page"}}

for page_name in pages:
    pages[page_name].update(default_values)
