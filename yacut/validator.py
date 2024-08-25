from .constants import MIN_CHARACTERS, MAX_CHARACTERS


def is_valid_custom_id(custom_id):
    return (
        custom_id.isalnum()
        and MIN_CHARACTERS <= len(custom_id) <= MAX_CHARACTERS
    )
