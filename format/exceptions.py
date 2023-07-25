class InvalidEmailException(Exception):
    def __init__(self, email):
        self.email = email
        self.message = f"Invalid email address: {email}"
        super().__init__(self.message)


class InvalidQueryException(Exception):
    def __init__(self, query):
        self.message = f"The query has no name information: {query}"
        super().__init__(self.message)
