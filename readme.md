Mo Books Laz Problems API

Classes:
- User
    Endpoints:
    - /user/add (POST)
        Adds a new user
    - /user/verifications (POST)
        Verifiys a users login attempt
    - /user/get (GET)
        Returns all of the users

- Book
    Endpoints:
    - /book/add (POST)
        Adds a new book
    - /book/get (GET)
        Returns all of the books
    - /book/get/<user_id> (GET)
        Returns all of the books by a single user
    - /book/delete/<id> (GET)
        Deletes a single book by the id