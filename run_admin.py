from sqlalchemy.orm import Session
from app.database import engine
from app.utils.seed_admin import seed_super_admin

with Session(engine) as db:
    seed_super_admin(db)
    
print("✅ Admin setup complete!")
print("Email: ahado@gmail.com")
print("Password: Syrafi@25!")