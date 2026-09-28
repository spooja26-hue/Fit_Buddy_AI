from .config import (
    ALLOW_DEMO_FALLBACK,
    GEMINI_NUTRITION_MODEL,
)

from .gemini_client import generate_text


SYSTEM = """
You are FitBuddy, a safe and supportive AI fitness and wellness assistant.

Your job is to provide a useful Nutrition & Recovery Tip based on the
user's age, fitness goal, preferred workout intensity, and general profile.

IMPORTANT SAFETY RULES:

- Give general healthy-habit guidance, not medical advice.
- Do not provide calorie targets.
- Do not recommend starvation, meal skipping, crash diets,
  or restrictive eating.
- Do not recommend unsafe supplements.
- Do not encourage rapid weight loss.
- Do not create body-shape pressure.
- For users under 18, focus on balanced meals, hydration,
  sleep, recovery and healthy development rather than weight change.
- If the user mentions illness, injury, severe pain, dizziness,
  or another medical concern, recommend speaking with a parent/guardian
  and an appropriate healthcare professional.
- Keep the advice practical and easy to understand.
"""


def generate_nutrition_tip(
    name: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
):

    prompt = f"""
Create a personalized Nutrition & Recovery Tip for this FitBuddy user.

USER INFORMATION

Name: {name}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

Write a complete and useful nutrition and recovery section.

The response must:

1. Start with one short sentence connecting the advice
   to the user's fitness goal.

2. Give practical advice about balanced meals and
   suitable food choices.

3. Mention useful protein or nutrient-rich food sources
   when appropriate.

4. Include hydration advice.

5. Include sleep and recovery advice.

6. Explain how these habits support the user's fitness goal.

7. Give one simple daily habit the user can follow.

IMPORTANT:

- Do NOT calculate calories.
- Do NOT give calorie targets.
- Do NOT recommend restrictive diets.
- Do NOT recommend starvation or meal skipping.
- Do NOT recommend unsafe supplements.
- Do NOT make medical claims.
- Keep the advice age-appropriate.
- If the user is under 18, focus on healthy growth,
  balanced nutrition, hydration, sleep and recovery.

FORMAT:

Nutrition & Recovery Tip

Write 5 to 7 complete sentences in clear, simple English.

Use 2 or 3 short paragraphs if needed.

Do not stop in the middle of a sentence.
Do not give unnecessary explanations.
"""


    try:

        result = generate_text(
            prompt=prompt,
            model=GEMINI_NUTRITION_MODEL,
            system_instruction=SYSTEM,
            temperature=0.5,
            max_output_tokens=700,
        )

        if not result or len(result.strip()) < 80:
            raise RuntimeError(
                "Gemini returned an incomplete nutrition tip."
            )

        return result.strip()

    except Exception as exc:

        print(
            "NUTRITION GEMINI ERROR:",
            repr(exc)
        )

        if ALLOW_DEMO_FALLBACK:
            return (
                f"For your {goal} goal, focus on regular balanced "
                f"meals that include a variety of vegetables or "
                f"fruits, whole grains, and a protein source such "
                f"as eggs, beans, fish, chicken, paneer or yogurt. "
                f"Drink water regularly throughout the day, "
                f"especially around physical activity. After "
                f"exercise, give your body enough time to rest and "
                f"recover. Aim for a consistent sleep routine "
                f"because good sleep supports energy, recovery "
                f"and overall fitness. One simple habit is to "
                f"prepare a balanced meal or snack before you "
                f"become very hungry so you can make a steady "
                f"and nutritious choice."
            )

        raise