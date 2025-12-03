
from typing import Dict, Any
from openai import OpenAI

from app.models import FieldSpec

client = OpenAI()


def build_parser_prompt(raw_text: str, fields: Dict[str, FieldSpec]) -> str:
    lines = [
        "You are a strict information extraction engine.",
        "You will be given the full OCR text of a document and a list of fields to extract.",
        "For each field, you must return a JSON object mapping field keys to extracted values.",
        "If a value cannot be found, return null for that field.",
        "",
        "Fields:",
    ]
    for key, spec in fields.items():
        lines.append(
            f'- key: "{key}", name: "{spec.name}", description: "{spec.description}", type: "{spec.type}"'
        )
    lines.extend([
        "",
        "Full OCR text:",
        raw_text,
        "",
        "Return ONLY valid JSON in this format:",
        '{',
        '  "field_key_1": "value or null",',
        '  "field_key_2": "value or null"',
        '}'
    ])
    return "\n".join(lines)


def parse_fields_with_llm(
    raw_text: str,
    fields: Dict[str, FieldSpec],
    model: str = "gpt-4.1-mini",
) -> Dict[str, Any]:
    prompt = build_parser_prompt(raw_text, fields)

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You extract structured data as JSON."},
            {"role": "user", "content": prompt},
        ]
    )

    content = completion.choices[0].message.content

    
    import json
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # fallback: return all nulls
        data = {key: None for key in fields.keys()}

    return data
