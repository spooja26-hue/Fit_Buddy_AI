from .config import (
    ALLOW_DEMO_FALLBACK,
    GEMINI_WORKOUT_MODEL,
)
from .gemini_client import generate_text


SYSTEM_INSTRUCTION = """
You are FitBuddy's plan improvement assistant.

Improve a fitness plan using user feedback.

Safety requirements:

- Never recommend extreme exercise.
- Never recommend starvation.
- Never recommend rapid weight loss.
- Never recommend unsafe supplements.
- Never tell a person to exercise through pain.
- Keep rest and recovery.
- Avoid calorie targets.
- Avoid body-shaming.
- Keep recommendations practical.
- If medical concerns are mentioned, recommend appropriate
  professional advice.
"""


def demo_updated_plan(original_plan: str, feedback: str):
    return f"""
UPDATED FITBUDDY PLAN

Your feedback:
{feedback}

The plan can be adjusted by:

• Keeping workouts comfortable and progressive.
• Adding extra recovery if you feel tired.
• Reducing repetitions when an activity feels too difficult.
• Choosing walking or gentle mobility on recovery days.
• Keeping regular meals, hydration, and sleep.

Previous plan:

{original_plan}

This updated version should be adjusted further based on
comfort, ability, and professional advice when necessary.
"""


def generate_updated_plan(
    original_plan: str,
    feedback: str,
):
    prompt = f"""
Update the following fitness plan based on the user's feedback.

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Return a complete updated 7-day plan.

Clearly show:
DAY 1
DAY 2
DAY 3
DAY 4
DAY 5
DAY 6
DAY 7

Also include short recovery and safety guidance.

Do not use extreme exercise or restrictive dieting.
"""

    try:
        return generate_text(
            prompt=prompt,
            model=GEMINI_WORKOUT_MODEL,
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.6,
            max_output_tokens=3500,
        )

    except Exception:
        if ALLOW_DEMO_FALLBACK:
            return demo_updated_plan(
                original_plan=original_plan,
                feedback=feedback,
            )

        raise