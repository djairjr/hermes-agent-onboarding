#!/usr/bin/env python3
"""
MBTI Scorer — scoring idêntico ao MBTI Guru original
Adaptado para Hermes: sem dependências externas, sem lib.questions
"""

def calculate_type(answers: list, questions: list) -> tuple:
    """
    Calculate MBTI type from answers using the same logic as Guru original.

    Args:
        answers: list of (question_id, "A"|"B") tuples
        questions: list of question dicts with id, dimension, preference_a

    Returns:
        (type_code: str, scores: dict)
    """
    if not answers or not questions:
        return "UNKNOWN", {}

    # Build question lookup
    q_map = {q["id"]: q for q in questions}

    # Count preferences for each dimension
    dim_counts = {
        "EI": {"E": 0, "I": 0},
        "SN": {"S": 0, "N": 0},
        "TF": {"T": 0, "F": 0},
        "JP": {"J": 0, "P": 0}
    }

    dim_totals = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
    all_prefs = {"EI": ["E", "I"], "SN": ["S", "N"], "TF": ["T", "F"], "JP": ["J", "P"]}

    for q_id, selected in answers:
        if q_id not in q_map:
            continue
        q = q_map[q_id]
        dim = q["dimension"]

        # Get preference based on answer choice
        if selected.upper() == "A":
            pref = q["preference_a"]
        else:
            first_pref = q["preference_a"]
            prefs = all_prefs[dim]
            pref = prefs[1] if first_pref == prefs[0] else prefs[0]

        dim_counts[dim][pref] += 1
        dim_totals[dim] += 1

    # Calculate indices and type
    scores = {}
    type_letters = []

    for dim in ["EI", "SN", "TF", "JP"]:
        first_count = dim_counts[dim][dim[0]]
        total = dim_totals[dim]

        if total == 0:
            scores[dim] = 50.0
            type_letters.append(dim[0])
            continue

        index_first = (first_count / total) * 100
        scores[dim] = round(index_first, 1)

        if index_first > 50:
            type_letters.append(dim[0])
        else:
            type_letters.append(dim[1])

    type_code = "".join(type_letters)
    return type_code, scores


def calculate_clarity(score: float) -> tuple:
    """
    Calculate clarity level from dimension score.
    Returns (clarity_percent, level_string)
    """
    clarity = abs(score - 50) * 2

    if clarity <= 25:
        level = "Leve"
    elif clarity <= 50:
        level = "Moderada"
    elif clarity <= 75:
        level = "Clara"
    else:
        level = "Muito Clara"

    return round(clarity, 1), level


def format_scores(scores: dict) -> str:
    """Format scores for display in pt-BR"""
    result = []
    dim_names = {
        "EI": "E/I (Energia)",
        "SN": "S/N (Informação)",
        "TF": "T/F (Decisão)",
        "JP": "J/P (Estrutura)"
    }
    for dim in ["EI", "SN", "TF", "JP"]:
        score = scores.get(dim, 50)
        clarity, level = calculate_clarity(score)
        pref = dim[0] if score > 50 else dim[1]
        pref_desc = {
            "E": "Extroversão", "I": "Introversão",
            "S": "Sensorial", "N": "Intuição",
            "T": "Racional", "F": "Emocional",
            "J": "Julgador", "P": "Perceptivo"
        }
        result.append(f"  {dim_names[dim]}: {pref} ({pref_desc[pref]}) — {score}% — {level}")
    return "\n".join(result)
