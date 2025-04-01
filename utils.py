def validate_email(email):
    import re
    return bool(re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))

# def validate_phone(phone):
#     return phone.isdigit() and 7 <= len(phone) <= 15

def validate_phone(phone):
    import re
    return bool(re.match(r"^[6789]\d{9}$", phone))