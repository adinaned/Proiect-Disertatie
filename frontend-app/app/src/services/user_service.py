import hashlib

def anonymize_user_data(user):
    user.first_name = "Anonymous"
    user.last_name = "Anonymous"
    user.email_id = hashlib.sha256(str(user.email_id).encode()).hexdigest()
    user.national_id = hashlib.sha256(str(user.national_id).encode()).hexdigest()
    return user
