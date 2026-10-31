
from .database import SessionLocal
from .models import Counter

db = SessionLocal()

try:
    services = [
        "Administrative Office",
        "Fees Counter",
        "Student Section"
    ]

    for service in services:
        existing = db.query(Counter).filter(
            Counter.service_name == service
        ).first()

        if not existing:
            new_counter = Counter(service_name=service)
            db.add(new_counter)

    db.commit()

    print("QueueLess services added successfully!")

except Exception as error:
    db.rollback()
    print("Error:", error)

finally:
    db.close()
