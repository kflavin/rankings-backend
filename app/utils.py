from datetime import date, timedelta

# Helper function to add in active attribute
def isActive(d):
    if date.today() > d and date.today() <= d + timedelta(2):
        return True
    else:
        return False