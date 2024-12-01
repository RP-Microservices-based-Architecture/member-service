from flask import Flask


members = ["river", "mountain", "forest", "sky", "sea"]

app = Flask(__name__)

@app.route('/members')
def hello_world():
    
    toReturn = "<ul> \n"

    for member in members:
        toReturn += "<li>" + member + "</li> \n"
        
    toReturn += "</ul>"
    
    return toReturn

def registerSelf():
    # Register service to the service registry
    # This is a placeholder for the actual implementation
    print("Service registered")
    pass

registerSelf()