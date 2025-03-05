class Auth:
    def __init__(self):
        self.logged_in_users = {}

    def login(self, user_id):
        self.logged_in_users[user_id] = True

    def logout(self, user_id):
        self.logged_in_users.pop(user_id, None)