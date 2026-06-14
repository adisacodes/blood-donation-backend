from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password

def seed_super_admin(db: Session):
    # 1. Search the database for any user with the 'admin' role
    admin_user = db.query(User).filter(User.role == "admin").first()
    
    # Target credentials
    target_email = "ahado@gmail.com"
    target_password_plain = "Syrafi@25!"
    
    if not admin_user:
        # Case A: No admin exists at all -> Create a brand new one
        print("Seeding fresh Super Admin account into database...")
        super_admin = User(
            email=target_email,          
            hashed_password=hash_password(target_password_plain), 
            role="admin",
            first_name="System",
            last_name="Administrator"
        )
        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)
        print("Super Admin initialized successfully!")
    else:
        # Case B: An admin exists -> Verify it uses your updated credentials
        if admin_user.email != target_email:
            print(f"Updating outdated Admin email from '{admin_user.email}' to '{target_email}'...")
            admin_user.email = target_email
            admin_user.hashed_password = hash_password(target_password_plain)
            db.commit()
            print(" Super Admin credentials updated successfully!")
        else:
            print("ℹ Super Admin account is already up-to-date in the database.")