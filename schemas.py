from typing import Literal

from pydantic import BaseModel, Field, field_validator

from .config import MAX_AGE, MIN_AGE


class WorkoutRequest(BaseModel):
    user_id: str = Field(
        min_length=3,
        max_length=50,
    )

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    age: int = Field(
        ge=MIN_AGE,
        le=MAX_AGE,
    )

    weight: float = Field(
        gt=0,
        le=500,
    )

    goal: str = Field(
        min_length=3,
        max_length=200,
    )

    intensity: Literal[
        "low",
        "medium",
        "high",
    ]

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("User ID cannot be empty.")

        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty.")

        return value

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Goal cannot be empty.")

        return value


class FeedbackRequest(BaseModel):
    user_id: str = Field(
        min_length=3,
        max_length=50,
    )

    feedback: str = Field(
        min_length=3,
        max_length=1000,
    )

    @field_validator("feedback")
    @classmethod
    def validate_feedback(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Feedback cannot be empty.")

        return value