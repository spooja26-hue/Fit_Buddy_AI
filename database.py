from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from .config import DATABASE_URL


connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
    )

    age: Mapped[int] = mapped_column(
        Integer,
    )

    weight: Mapped[float] = mapped_column(
        Float,
    )

    goal: Mapped[str] = mapped_column(
        String(200),
    )

    intensity: Mapped[str] = mapped_column(
        String(20),
    )

    original_plan: Mapped[str] = mapped_column(
        Text,
    )

    updated_plan: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    nutrition_tip: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    feedback: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_user(db: Session, user_id: str):
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )


def get_all_users(db: Session):
    return (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )


def create_user(
    db: Session,
    user_id: str,
    name: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    original_plan: str,
    nutrition_tip: str,
):
    user = User(
        user_id=user_id,
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
        original_plan=original_plan,
        updated_plan=original_plan,
        nutrition_tip=nutrition_tip,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user_plan(
    db: Session,
    user_id: str,
    updated_plan: str,
    feedback: str,
):
    user = get_user(db, user_id)

    if user is None:
        return None

    user.updated_plan = updated_plan
    user.feedback = feedback
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user_id: str):
    user = get_user(db, user_id)

    if user is None:
        return False

    db.delete(user)
    db.commit()

    return True