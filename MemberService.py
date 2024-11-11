class MemberService:
    def __init__(self, db_manager):
        """
        Initializes the MemberService with a DatabaseManager instance.
        :param db_manager: Instance of DatabaseManager to handle database connections.
        """
        self.db_manager = db_manager

    def add_member(self, member_data):
        query = """
        INSERT INTO Members (first_name, last_name, gender, contact_email, date_of_birth, skill_level_rating, sport_interest, membership_type, password_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            member_data['first_name'],
            member_data['last_name'],
            member_data['gender'],
            member_data['contact_email'],
            member_data['date_of_birth'],
            member_data['skill_level_rating'],
            member_data['sport_interest'],
            member_data['membership_type'],
            member_data['password_hash']
        )

        try:
            self.db_manager.execute_query(query, values)  # Use db_manager to execute
            return "Member added successfully."
        except Exception as e:
            print(f"Error executing update: {e}")
            return f"Error adding member: {e}"

    def get_member(self, member_id):
        """
        Retrieves a specific member's details by ID.
        :param member_id: ID of the member to retrieve.
        :return: Member data as a dictionary or None if not found.
        """
        query = "SELECT * FROM Members WHERE member_id = %s"
        
        result = self.db_manager.execute_query(query, (member_id,))
        if result:
            return {
                "member_id": result[0],
                "first_name": result[1],
                "last_name": result[2],
                "gender": result[3],
                "contact_email": result[4],
                "date_of_birth": result[5],
                "skill_level_rating": result[6],
                "sport_interest": result[7],
                "membership_type": result[8]
            }
        else:
            return None
    

    def update_member(self, member_id, updated_data):
        """
        Updates a specific member's details by ID.
        :param member_id: ID of the member to update.
        :param updated_data: Dictionary of updated member data.
        :return: Success message or error message.
        """
        query = """
        UPDATE Members SET first_name = %s, last_name = %s, gender = %s, contact_email = %s, 
        date_of_birth = %s, skill_level_rating = %s, sport_interest = %s, membership_type = %s 
        WHERE member_id = %s
        """
        params = (
            updated_data["first_name"],
            updated_data["last_name"],
            updated_data["gender"],
            updated_data["contact_email"],
            updated_data["date_of_birth"],
            updated_data["skill_level_rating"],
            updated_data["sport_interest"],
            updated_data["membership_type"],
            member_id
        )
        
        try:
            self.db_manager.execute_update(query, params)
            return "Member updated successfully."
        except Exception as e:
            return f"Error updating member: {str(e)}"

    def delete_member(self, member_id):
        """
        Deletes a specific member's record by ID.
        :param member_id: ID of the member to delete.
        :return: Success message or error message.
        """
        query = "DELETE FROM Members WHERE member_id = %s"
        
        try:
            self.db_manager.execute_update(query, (member_id,))
            return "Member deleted successfully."
        except Exception as e:
            return f"Error deleting member: {str(e)}"
        
    def get_all_members(self):
        query = "SELECT * FROM Members"
        results = self.db_manager.execute_query(query)
        members = []
        for result in results:
            members.append({
                "member_id": result[0],
                "first_name": result[1],
                "last_name": result[2],
                "gender": result[3],
                "contact_email": result[4],
                "date_of_birth": result[5],
                "skill_level_rating": result[6],
                "sport_interest": result[7],
                "membership_type": result[8]
            })
        return members



    def find_members_by_skill_level_and_interest(self, skill_level, interest):
        """
        Finds members based on skill level and sport interest.
        :param skill_level: Skill level to filter members.
        :param interest: Sport interest to filter members.
        :return: List of members that match the criteria.
        """
        query = """
        SELECT * FROM Members WHERE skill_level_rating = %s AND sport_interest = %s
        """
        params = (skill_level, interest)
        
        results = self.db_manager.execute_query(query, params)
        members = []
        
        for result in results:
            members.append({
                "member_id": result[0],
                "first_name": result[1],
                "last_name": result[2],
                "gender": result[3],
                "contact_email": result[4],
                "date_of_birth": result[5],
                "skill_level_rating": result[6],
                "sport_interest": result[7],
                "membership_type": result[8]
            })
        
        return members
