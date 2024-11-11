import re
from datetime import datetime

class MemberValidator:
    @staticmethod
    def validate_email(email):
        """
        Validates that the email is in a proper format.
        :param email: The email to validate.
        :return: True if the email format is valid, False otherwise.
        """
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_skill_level(skill_level):
        """
        Validates that the skill level is within an acceptable range.
        :param skill_level: The skill level to validate.
        :return: True if the skill level is within the range, False otherwise.
        """
        return isinstance(skill_level, int) and 1 <= skill_level <= 10

    @staticmethod
    def validate_membership_type(membership_type):
        """
        Validates that the membership type is one of the allowed values.
        :param membership_type: The membership type to validate.
        :return: True if the membership type is valid, False otherwise.
        """
        valid_membership_types = {"Basic", "Premium", "VIP"}
        return membership_type in valid_membership_types

    @staticmethod
    def validate_date_of_birth(date_of_birth):
        """
        Validates that the date of birth is in the past and in the correct format.
        :param date_of_birth: The date of birth to validate (YYYY-MM-DD format).
        :return: True if the date of birth is valid, False otherwise.
        """
        try:
            dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
            return dob < datetime.now()  # Check if date is in the past
        except ValueError:
            return False

    @staticmethod
    def validate_gender(gender):
        """
        Validates that the gender is one of the allowed values.
        :param gender: The gender to validate.
        :return: True if the gender is valid, False otherwise.
        """
        valid_genders = {"Male", "Female", "Other"}
        return gender in valid_genders

    @staticmethod
    def validate_name(name):
        """
        Validates that the name is a non-empty string and contains only alphabetic characters.
        :param name: The name to validate.
        :return: True if the name is valid, False otherwise.
        """
        return isinstance(name, str) and name.isalpha() and len(name) > 0
