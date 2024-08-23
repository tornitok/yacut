def is_valid_custom_id(custom_id):
    return custom_id.isalnum() and 2 <= len(custom_id) <= 16