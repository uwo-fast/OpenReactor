import datetime

class User:
    """A member of FriendFace for now we are only storing their name and birthday."""
    def __init__(self ,full_name, birthday):
        self.name = full_name
        self.birthday = birthday # yyyymmdd

        # Extract first and last names
        name_pieces = full_name.split(" ")
        self.first_name = name_pieces[0]
        self.last_name = name_pieces[1]
    
    def age(self):
        """Returns the age of the user in years"""
        today = datetime.date(2001, 5, 12)


user = User("Dave Bowman", 19710315)
print(user.name)
print(user.first_name)
print(user.last_name)
print(user.birthday)

help(User)