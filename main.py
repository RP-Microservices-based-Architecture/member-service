import os
import time
import threading
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from MemberService import MemberService  # Import the MemberService class
from DatabaseManager import DatabaseManager  # Assuming DatabaseManager is required
import pymysql
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration for the Member Service
SERVICE_NAME = "MemberService"
INSTANCE_ID = "member-service-1"
SERVICE_IP = os.getenv("SERVICE_IP", "https://member-f7hdcjgnh7e3ejak.canadacentral-01.azurewebsites.net")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 443))
SERVICE_REGISTRY_URL = os.getenv("SERVICE_REGISTRY_URL")

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 443)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'ssl': {'ssl': {'ssl-mode': os.getenv('DB_SSL_MODE', 'REQUIRED')}}
}

# Initialize DatabaseManager and MemberService
db_manager = DatabaseManager(**DB_CONFIG)
member_service = MemberService(db_manager)

# Register the service with the service registry
def register_service():
    payload = {
        "service_name": "MemberService",
        "instance_id": "member-service-1",
        "ip_address": "https://member-f7hdcjgnh7e3ejak.canadacentral-01.azurewebsites.net",
        "port": 443
    }
    print("Payload:", payload)  # Debugging
    try:
        response = requests.post("https://serviceregistry-b5hsbsgnc3aaembu.canadacentral-01.azurewebsites.net/register", json=payload)
        print("Registration Response status code:", response.status_code)
        print("Registration Response content:", response.content.decode())  # Decode response for clarity
        
        if response.status_code == 200:
            try:
                print("Service registered successfully:", response.json())
            except ValueError:
                print("Service registered, but received non-JSON response:", response.content.decode())
        else:
            print("Failed to register service:", response.content.decode())
    except Exception as e:
        print("Error registering service:", e)

# Discover a specific service
def discover_service(service_name):
    try:
        response = requests.get(f"{SERVICE_REGISTRY_URL}/discover/{service_name}")
        if response.status_code == 200:
            services = response.json().get("services", [])
            print(f"Discovered {service_name} instances:", services)
            return services
        else:
            print("No available services found for", service_name)
            return None
    except Exception as e:
        print("Error discovering service:", e)
        return None

# Heartbeat endpoint for health checks
@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    instance_id = data.get('instance_id')

    if instance_id == INSTANCE_ID:
        return jsonify({"message": "Service is healthy"}), 200
    else:
        return jsonify({"error": "Instance ID mismatch"}), 400

# Initialize MemberService
# member_service = MemberService(DB_CONFIG)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view_members')
def view_members():
    members = member_service.get_all_members()  # Ensure `get_all_members` is implemented in your service
    return jsonify(members)

@app.route('/members', methods=['POST'])
def add_member():
    member_data = request.json
    response = member_service.add_member(member_data)
    return jsonify({"message": response}), 200 if "successfully" in response else 400

@app.route('/members', methods=['GET'])
def get_all_members():
    members = member_service.get_all_members()  # This method should be defined in MemberService
    return jsonify(members)


# Initialize DatabaseManager and MemberService
db_manager = DatabaseManager(**DB_CONFIG)
member_service = MemberService(db_manager)

# Routes

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """
    Retrieves a specific member by ID.
    """
    member = member_service.get_member(member_id)
    if member:
        return jsonify(member)
    else:
        return jsonify({"message": "Member not found"}), 404

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """
    Updates a specific member's details by ID.
    """
    updated_data = request.json
    response = member_service.update_member(member_id, updated_data)
    return jsonify({"message": response}), 200 if "successfully" in response else 400

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """
    Deletes a specific member by ID.
    """
    response = member_service.delete_member(member_id)
    return jsonify({"message": response}), 200 if "successfully" in response else 400

@app.route('/members/search', methods=['GET'])
def find_members():
    """
    Finds members based on skill level and sport interest.
    Expects query parameters: skill_level and interest.
    """
    skill_level = request.args.get('skill_level', type=int)
    interest = request.args.get('interest', type=str)
    
    if skill_level is None or interest is None:
        return jsonify({"message": "Please provide skill_level and interest query parameters"}), 400

    members = member_service.find_members_by_skill_level_and_interest(skill_level, interest)
    return jsonify(members), 200

# Register the service and start the Flask app
if __name__ == '__main__':
    # Register this service with the registry at startup
    register_service()

    # Start a background thread to send heartbeats periodically
    # heartbeat_thread = threading.Thread(target=send_heartbeat)
    # heartbeat_thread.daemon = True
    # heartbeat_thread.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=SERVICE_PORT, debug=True)