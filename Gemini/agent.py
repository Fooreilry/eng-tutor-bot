from google.genai import types

from Gemini.client import client
from Gemini.prompts import build_system_prompt

MODEL = "gemini-2.5-flash"


async def chat_with_alex(
    message: str,
    history: list[dict],
    name: str,
    level: str,
    interests: str,
    additional: str | None = None,
) -> str:
    system_prompt = build_system_prompt(name, level, interests, additional)

    contents = []
    for msg in history:
        contents.append(
            types.Content(
                role=msg["role"],
                parts=[types.Part.from_text(text=msg["text"])],
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=message)],
        )
    )

    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.9,
            max_output_tokens=500,
        ),
    )

    return response.text
