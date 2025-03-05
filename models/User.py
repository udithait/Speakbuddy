class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

    def get_details(self):
        return {'id': self.user_id, 'username': self.username, 'email': self.email}