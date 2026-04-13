from sqlalchemy import Column, Integer, String
from db import Base
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer)
    password = Column(String, nullable=False)  # store hashed password

    # Helper methods for password management
    def set_password(self, raw_password: str):
        """Hash and store the password securely."""
        self.password = pwd_context.hash(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return pwd_context.verify(raw_password, self.password)
