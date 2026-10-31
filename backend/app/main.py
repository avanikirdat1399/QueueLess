
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt, JWTError

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .database import SessionLocal
from .models import Counter, User, Token, QueueHistory
from .auth_utils import hash_password, verify_password


# Load environment variables
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


app = FastAPI(
    title="QueueLess",
    description="Smart Queue Management System",
    version="1.0.0"
)


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


# Registration request format
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


# Login request format
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenRequest(BaseModel):
    counter_id: int


# Generate JWT access token
def create_access_token(user_id):

    if not SECRET_KEY:
        raise HTTPException(
            status_code=500,
            detail="JWT secret key is not configured"
        )

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def get_current_user_id(authorization: str = Header(default=None)):

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Please log in first"
        )

    access_token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return int(payload["sub"])

    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired login session"
        )

# Home page
@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/auth")
def authentication_page():
    return FileResponse(FRONTEND_DIR / "auth.html")

@app.get("/dashboard")
def student_dashboard():
    return FileResponse(FRONTEND_DIR / "dashboard.html")


# Backend health check
@app.get("/api/health")
def health_check():
    return {
        "status": "success",
        "message": "QueueLess backend is running"
    }


# Get available services
@app.get("/api/counters")
def get_counters():

    db = SessionLocal()

    try:
        counters = db.query(Counter).all()

        return [
            {
                "id": counter.id,
                "service_name": counter.service_name,
                "status": counter.status
            }
            for counter in counters
        ]

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to fetch services"
        )

    finally:
        db.close()


# Student registration API
@app.post("/api/register")
def register_student(data: RegisterRequest):

    db = SessionLocal()

    try:
        name = data.name.strip()
        email = data.email.strip().lower()
        password = data.password

        if not name or not email or not password:
            raise HTTPException(
                status_code=400,
                detail="All fields are required"
            )

        if "@" not in email:
            raise HTTPException(
                status_code=400,
                detail="Enter a valid email address"
            )

        if len(password) < 8:
            raise HTTPException(
                status_code=400,
                detail="Password must contain at least 8 characters"
            )

        existing_user = db.query(User).filter(
            User.email == email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email is already registered"
            )

        new_user = User(
            name=name,
            email=email,
            password=hash_password(password),
            role="student"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Student registered successfully!",
            "user_id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Registration failed. Please try again."
        )

    finally:
        db.close()


# Student login API
@app.post("/api/login")
def login_student(data: LoginRequest):

    db = SessionLocal()

    try:
        email = data.email.strip().lower()

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user or not verify_password(
            data.password,
            user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(user.id)

        return {
            "message": "Login successful!",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Login failed. Please try again."
        )

    finally:
        db.close()

@app.post("/api/tokens")
def generate_token(
    data: TokenRequest,
    authorization: str = Header(default=None)
):

    user_id = get_current_user_id(authorization)

    db = SessionLocal()

    try:
        # Find the selected service
        counter = db.query(Counter).filter(
            Counter.id == data.counter_id
        ).first()

        if not counter:
            raise HTTPException(
                status_code=404,
                detail="Service not found"
            )

        # Check if student already has an active token
        active_token = db.query(Token).filter(
            Token.user_id == user_id,
            Token.status == "waiting"
        ).first()

        if active_token:
            raise HTTPException(
                status_code=400,
                detail="You already have an active token"
            )

        # Assign a prefix to each service
        prefixes = {
            "Administrative Office": "AO",
            "Fees Counter": "FC",
            "Student Section": "SS"
        }

        prefix = prefixes.get(counter.service_name, "QL")

        # Calculate the next token number
        total_tokens = db.query(Token).filter(
            Token.counter_id == counter.id
        ).count()

        token_number = f"{prefix}-{total_tokens + 1:03d}"

        # Create the token
        new_token = Token(
            user_id=user_id,
            counter_id=counter.id,
            token_number=token_number,
            status="waiting"
        )

        db.add(new_token)
        db.commit()
        db.refresh(new_token)

        # Save token activity in queue history
        history = QueueHistory(
            token_id=new_token.id,
            action="Token Generated"
        )

        db.add(history)
        db.commit()

        return {
            "message": "Token generated successfully!",
            "token_number": new_token.token_number,
            "service": counter.service_name,
            "status": new_token.status
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to generate token"
        )

    finally:
        db.close()

@app.get("/api/my-token")
def get_my_token(authorization: str = Header(default=None)):

    user_id = get_current_user_id(authorization)

    db = SessionLocal()

    try:
        # Find the student's active token
        current = db.query(Token).filter(
            Token.user_id == user_id,
            Token.status == "waiting"
        ).first()

        if not current:
            return {"message": "No active token"}

        # Find the selected service
        counter = db.query(Counter).filter(
            Counter.id == current.counter_id
        ).first()

        # Count people waiting before this student
        people_ahead = db.query(Token).filter(
            Token.counter_id == current.counter_id,
            Token.status == "waiting",
            Token.id < current.id
        ).count()

        return {
            "token_number": current.token_number,
            "service": counter.service_name,
            "status": current.status,
            "people_ahead": people_ahead,
            "estimated_wait_minutes": people_ahead * 5
        }

    finally:
        db.close()

@app.post("/api/cancel-token")
def cancel_token(authorization: str = Header(default=None)):

    user_id = get_current_user_id(authorization)

    db = SessionLocal()

    try:
        # Find the student's active token
        current = db.query(Token).filter(
            Token.user_id == user_id,
            Token.status == "waiting"
        ).first()

        if not current:
            raise HTTPException(
                status_code=404,
                detail="No active token found"
            )

        # Change token status
        current.status = "cancelled"

        # Record cancellation in queue history
        history = QueueHistory(
            token_id=current.id,
            action="Token Cancelled"
        )

        db.add(history)
        db.commit()

        return {
            "message": "Token cancelled successfully!",
            "token_number": current.token_number,
            "status": current.status
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to cancel token"
        )

    finally:
        db.close()