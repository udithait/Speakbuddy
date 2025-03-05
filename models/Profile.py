class Profile:
    def __init__(self, user_id, bio):
        self.user_id = user_id
        self.bio = bio

    def update_bio(self, new_bio):
        self.bio = new_bio