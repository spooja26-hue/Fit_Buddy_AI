from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .config import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    BASE_DIR,
)

from .database import (
    create_user,
    delete_user,
    get_all_users,
    get_db,
    get_user,
    update_user_plan,
)

from .gemini_flash_generator import generate_nutrition_tip
from .gemini_generator import generate_workout_plan
from .schemas import FeedbackRequest, WorkoutRequest
from .updated_plan import generate_updated_plan


router = APIRouter()


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


security = HTTPBasic()


# ============================================================
# HOME PAGE
# ============================================================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


# ============================================================
# GENERATE WORKOUT PLAN
# ============================================================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse,
)
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:

        # Validate user input
        data = WorkoutRequest(
            user_id=user_id,
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

    except ValidationError as exc:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": str(exc),
            },
            status_code=400,
        )

    try:

        # Check whether User ID already exists
        existing_user = get_user(
            db,
            data.user_id,
        )

        if existing_user:

            return templates.TemplateResponse(
                request=request,
                name="error.html",
                context={
                    "message": (
                        "This User ID already exists. "
                        "Please use another User ID."
                    ),
                },
                status_code=400,
            )

        # ----------------------------------------------------
        # Generate AI Workout Plan
        # ----------------------------------------------------

        plan = generate_workout_plan(
            name=data.name,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity,
        )

        # ----------------------------------------------------
        # Generate Personalized Nutrition & Recovery Tip
        # ----------------------------------------------------
        # IMPORTANT:
        # We now send name, age, weight, goal and intensity
        # so Gemini can personalize the nutrition tip.
        # ----------------------------------------------------

        nutrition_tip = generate_nutrition_tip(
            name=data.name,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity,
        )

        # ----------------------------------------------------
        # Save User
        # ----------------------------------------------------

        create_user(
            db=db,
            user_id=data.user_id,
            name=data.name,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity,
            original_plan=plan,
            nutrition_tip=nutrition_tip,
        )

        # ----------------------------------------------------
        # Display Result
        # ----------------------------------------------------

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": {
                    "user_id": data.user_id,
                    "name": data.name,
                    "age": data.age,
                    "weight": data.weight,
                    "goal": data.goal,
                    "intensity": data.intensity,
                },
                "plan": plan,
                "nutrition_tip": nutrition_tip,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": (
                    f"Could not generate the plan: {exc}"
                ),
            },
            status_code=500,
        )


# ============================================================
# SUBMIT FEEDBACK
# ============================================================

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse,
)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):

    try:

        data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback,
        )

    except ValidationError as exc:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": str(exc),
            },
            status_code=400,
        )

    # Find user
    user = get_user(
        db,
        data.user_id,
    )

    if user is None:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": "User not found.",
            },
            status_code=404,
        )

    try:

        # Generate updated workout plan
        updated_plan = generate_updated_plan(
            original_plan=(
                user.updated_plan
                or user.original_plan
            ),
            feedback=data.feedback,
        )

        # Save updated plan
        update_user_plan(
            db=db,
            user_id=data.user_id,
            updated_plan=updated_plan,
            feedback=data.feedback,
        )

        # Display updated result
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": {
                    "user_id": user.user_id,
                    "name": user.name,
                    "age": user.age,
                    "weight": user.weight,
                    "goal": user.goal,
                    "intensity": user.intensity,
                },
                "plan": updated_plan,
                "nutrition_tip": user.nutrition_tip,
                "feedback_submitted": True,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": (
                    f"Could not update the plan: {exc}"
                ),
            },
            status_code=500,
        )


# ============================================================
# ADMIN AUTHENTICATION
# ============================================================

def verify_admin(
    credentials: HTTPBasicCredentials = Depends(security),
):

    if (
        credentials.username != ADMIN_USERNAME
        or credentials.password != ADMIN_PASSWORD
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials.",
            headers={
                "WWW-Authenticate": "Basic"
            },
        )

    return True


# ============================================================
# VIEW ALL USERS
# ============================================================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse,
)
def view_all_users(
    request: Request,
    _: bool = Depends(verify_admin),
    db: Session = Depends(get_db),
):

    users = get_all_users(db)

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users,
        },
    )


# ============================================================
# DELETE USER
# ============================================================

@router.post(
    "/delete-user/{user_id}"
)
def remove_user(
    user_id: str,
    _: bool = Depends(verify_admin),
    db: Session = Depends(get_db),
):

    deleted = delete_user(
        db,
        user_id,
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return RedirectResponse(
        url="/view-all-users",
        status_code=303,
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/api/health")
def health():

    return {
        "status": "ok",
        "application": "FitBuddy",
    }


# ============================================================
# API - GENERATE WORKOUT
# ============================================================

@router.post(
    "/api/generate-workout"
)
def api_generate_workout(
    data: WorkoutRequest,
    db: Session = Depends(get_db),
):

    # Check existing user
    existing_user = get_user(
        db,
        data.user_id,
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="User ID already exists.",
        )

    # --------------------------------------------------------
    # Generate Workout Plan
    # --------------------------------------------------------

    plan = generate_workout_plan(
        name=data.name,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity,
    )

    # --------------------------------------------------------
    # Generate Personalized Nutrition Tip
    # --------------------------------------------------------

    nutrition_tip = generate_nutrition_tip(
        name=data.name,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity,
    )

    # --------------------------------------------------------
    # Save User
    # --------------------------------------------------------

    user = create_user(
        db=db,
        user_id=data.user_id,
        name=data.name,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity,
        original_plan=plan,
        nutrition_tip=nutrition_tip,
    )

    # --------------------------------------------------------
    # API Response
    # --------------------------------------------------------

    return {
        "message": "Workout plan generated successfully.",
        "user_id": user.user_id,
        "plan": plan,
        "nutrition_tip": nutrition_tip,
    }


# ============================================================
# API - FEEDBACK
# ============================================================

@router.post(
    "/api/feedback"
)
def api_feedback(
    data: FeedbackRequest,
    db: Session = Depends(get_db),
):

    # Find user
    user = get_user(
        db,
        data.user_id,
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    # Generate updated plan
    updated_plan = generate_updated_plan(
        original_plan=(
            user.updated_plan
            or user.original_plan
        ),
        feedback=data.feedback,
    )

    # Save updated plan
    update_user_plan(
        db=db,
        user_id=data.user_id,
        updated_plan=updated_plan,
        feedback=data.feedback,
    )

    return {
        "message": "Plan updated successfully.",
        "user_id": data.user_id,
        "updated_plan": updated_plan,
    }