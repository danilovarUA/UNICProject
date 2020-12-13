default_values = {"name": "Series Recommendation System"}
pages = {"login": {"path": "login.html",
                   "header": "Login Page"},
         "register": {"path": "register.html",
                      "header": "Register Page"},
         "search": {"path": "search.html",
                    "header": "Search Page"},
         "results": {"path": "results.html",
                     "header": "Results Page"}}

for page_name in pages:
    pages[page_name].update(default_values)
