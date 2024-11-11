class Member:
    def __init__(self, member_id, first_name, last_name, gender, contact_email, date_of_birth, skill_level_rating, sport_interest, membership_type):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.contact_email = contact_email
        self.date_of_birth = date_of_birth
        self.skill_level_rating = skill_level_rating
        self.sport_interest = sport_interest
        self.membership_type = membership_type

    def to_dict(self):
        """Converts the Member object into a dictionary."""
        return {
            "member_id": self.member_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "contact_email": self.contact_email,
            "date_of_birth": self.date_of_birth,
            "skill_level_rating": self.skill_level_rating,
            "sport_interest": self.sport_interest,
            "membership_type": self.membership_type
        }

    @staticmethod
    def from_dict(data):
        """Creates a Member object from a dictionary."""
        return Member(
            member_id=data.get("member_id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            gender=data.get("gender"),
            contact_email=data.get("contact_email"),
            date_of_birth=data.get("date_of_birth"),
            skill_level_rating=data.get("skill_level_rating"),
            sport_interest=data.get("sport_interest"),
            membership_type=data.get("membership_type")
        )

    def __str__(self):
        """String representation of the Member object."""
        return (f"Member({self.member_id}, {self.first_name} {self.last_name}, "
                f"Email: {self.contact_email}, Skill Level: {self.skill_level_rating}, "
                f"Interests: {self.sport_interest}, Membership Type: {self.membership_type})")

    # Optional validation methods
    def validate_email(self):
        """Validates the email format."""
        import re
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, self.contact_email) is not None

    def validate_skill_level(self):
        """Validates the skill level rating is within an acceptable range (e.g., 1-10)."""
        return 1 <= self.skill_level_rating <= 10

    def validate_membership_type(self):
        """Validates the membership type."""
        valid_membership_types = ["Basic", "Premium", "VIP"]
        return self.membership_type in valid_membership_types
