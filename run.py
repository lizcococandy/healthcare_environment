from app import create_app, db
from app.models import User
import getpass

app = create_app()


@app.cli.command()
def init_db():
    """Initialize the database and create tables."""
    db.create_all()
    print("Database initialized!")


@app.cli.command()
def create_admin():
    """Create an admin user."""
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = getpass.getpass("Enter admin password: ")
    
    if User.query.filter_by(username=username).first():
        print("User already exists!")
        return
    
    user = User(username=username, email=email, role='admin')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print(f"Admin user '{username}' created successfully!")


if __name__ == '__main__':
    # Note: Debug mode should only be used in development.
    # In production, set DEBUG=False in config or use environment variables.
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode)
