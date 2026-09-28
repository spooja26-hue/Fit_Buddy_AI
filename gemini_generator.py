from .config import (
    ALLOW_DEMO_FALLBACK,
    GEMINI_WORKOUT_MODEL,
)

from .gemini_client import generate_text


SYSTEM_INSTRUCTION = """
You are FitBuddy, a safe and supportive AI fitness planning assistant.

Create practical, age-appropriate fitness guidance.

Important safety rules:

1. Do not recommend extreme exercise.
2. Do not recommend starvation or meal skipping.
3. Do not recommend rapid weight-loss methods.
4. Do not recommend unsafe supplements.
5. Do not encourage exercising through pain.
6. Include rest and recovery.
7. Use simple language.
8. Do not make medical diagnoses.
9. If the user mentions an injury, illness, severe pain,
   dizziness, chest pain, or another medical concern,
   recommend speaking with a parent/guardian and an appropriate
   healthcare professional.
10. For younger users, avoid calorie targets and body-shape pressure.
11. Focus on healthy habits, strength, mobility, fitness,
    sleep, hydration, and consistency.
"""


def demo_plan(
    name: str,
    goal: str,
    intensity: str,
):
    return f"""
FITBUDDY SAMPLE FITNESS PLAN

Hello {name}!

Goal: {goal}
Intensity: {intensity}

Day 1:
Warm-up + simple full-body exercises + cooldown.

Day 2:
Light cardio + mobility exercises.

Day 3:
Strength and basic bodyweight exercises.

Day 4:
Rest and recovery.

Day 5:
Full-body strength and mobility.

Day 6:
Light cardio and stretching.

Day 7:
Rest and recovery.

Stay hydrated, sleep well, and listen to your body.
"""


def generate_workout_plan(
    name: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
):
    prompt = f"""
Create a personalized 7-day beginner-friendly fitness plan.

USER INFORMATION:

Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Preferred intensity: {intensity}

Create a complete but reasonably concise weekly plan.

For EACH day include:

- Day number and day title
- Warm-up
- 3 to 5 main exercises
- Simple sets/repetitions OR approximate duration
- Cool-down
- Rest/recovery when appropriate

Use this structure:

Day 1:
Warm-up:
Main Workout:
- Exercise 1
- Exercise 2
- Exercise 3
- Exercise 4
Cool-down:

Day 2:
Warm-up:
Main Workout:
- Exercise 1
- Exercise 2
- Exercise 3
- Exercise 4
Cool-down:

Continue through Day 7.

For rest days, clearly mention that it is a recovery/rest day
and give simple mobility or stretching suggestions if appropriate.

At the end include:

Safety & Recovery Tips:
- Hydration
- Sleep
- Rest and recovery
- Safe exercise habits

IMPORTANT:

- Do not provide calorie targets.
- Do not recommend extreme dieting.
- Do not recommend unsafe supplements.
- Do not encourage exercising through pain.
- Keep the plan realistic and age-appropriate.
- Keep each day detailed enough to be useful.
- Avoid unnecessary long explanations.
- Make sure all 7 days are completed.
- Do not stop in the middle of a sentence.
- Give a complete final response.
"""

    try:
        return generate_text(
            prompt=prompt,
            model=GEMINI_WORKOUT_MODEL,
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.5,
            max_output_tokens=2800,
        )

    except Exception as exc:
        print(
            "GEMINI WORKOUT ERROR:",
            repr(exc)
        )

        if ALLOW_DEMO_FALLBACK:
            return demo_plan(
                name=name,
                goal=goal,
                intensity=intensity,
            )

        raise