import os
from flask_mail import Mail

# Create a Mail instance
mail = Mail()

def init_mail(app):
    # Initialize the mail instance with the Flask app
    mail.init_app(app)
