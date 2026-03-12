import json
from pathlib import Path

# Load questions from test.json
TEST_FILE = Path(__file__).parent / "data" / "test.json"
with open(TEST_FILE, "r", encoding="utf-8") as f:
    TEST_DATA = json.load(f)

QUESTIONS = TEST_DATA["questions"]

MAX_QUESTIONS = 10
PASS_THRESHOLD = 60
LEVELS_ORDER = ["A1", "A2", "B1", "B2"]


def get_available_questions(user_level: str) -> list[dict]:
    """Get questions at or below the user's level."""
    level_index = LEVELS_ORDER.index(user_level)
    allowed_levels = LEVELS_ORDER[: level_index + 1]
    return [q for q in QUESTIONS if q["level"] in allowed_levels]


def format_question_text(question: dict, current: int, total: int) -> str:
    """Format question text with number and type hint."""
    q_type = question["type"]

    type_hints = {
        "multiple_choice": "Выбери правильный вариант:",
        "fill_in_the_blank": "Напиши ответ текстом:",
        "translate": "Напиши перевод текстом:",
        "error_correction": "Напиши исправленное предложение:",
        "word_order": "Напиши правильное предложение:",
    }
    hint = type_hints.get(q_type, "")

    return f"📝 Вопрос {current}/{total} [{question['level']}]\n\n{question['question']}\n\n{hint}"


def check_answer(question: dict, user_answer: str) -> bool:
    """Check if the user's answer is correct."""
    q_type = question["type"]
    clean = user_answer.strip().lower().rstrip(".")

    if q_type == "multiple_choice":
        return clean == question["answer"].strip().lower()

    if q_type == "translate":
        acceptable = question.get("acceptable_answers", [question["answer"]])
        return clean in [a.strip().lower().rstrip(".") for a in acceptable]

    # fill_in_the_blank, error_correction, word_order
    return clean == question["answer"].strip().lower().rstrip(".")
