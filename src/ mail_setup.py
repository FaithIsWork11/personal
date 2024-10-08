import os
from flask_mail import Mail

mail = Mail()

def init_mail(app):
    # Load mail configuration from environment variables
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    app.config['ADMIN_EMAIL'] = os.getenv('ADMIN_EMAIL')
    # Initialize the mail instance with the Flask app
    mail.init_app(app)
