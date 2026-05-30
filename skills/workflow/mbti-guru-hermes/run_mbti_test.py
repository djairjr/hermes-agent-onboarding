#!/usr/bin/env python3
"""
run_mbti_test — módulo autônomo do MBTI Guru Hermes
Permite executar o teste sem interação conversacional:
via import, script, ou terminal.

Uso:
    python3 run_mbti_test.py                    # teste completo (70q, respostas simuladas)
    python3 run_mbti_test.py 93                 # versão 93
    python3 run_mbti_test.py 144 --all-b        # todas respostas B
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from questions_pt_BR import get_questions
from scorer import calculate_type, calculate_clarity, format_scores
from types_pt_BR import get_type


def run_mbti_test(answers: list, version: int = 70) -> dict:
    """
    Executa o teste MBTI completo sem interação.

    Args:
        answers: lista de (question_id, "A"|"B")
        version: 70, 93, 144, ou 200

    Returns:
        dict com type_code, name_pt_BR, scores, clarity, summary, strengths, weaknesses, careers
    """
    questions = get_questions(version)
    type_code, scores = calculate_type(answers, questions)
    tdata = get_type(type_code)

    clarities = {}
    for dim in ["EI", "SN", "TF", "JP"]:
        _, level = calculate_clarity(scores.get(dim, 50))
        clarities[dim] = level

    return {
        "type_code": type_code,
        "name_pt_BR": tdata.get("name_pt_BR", type_code),
        "scores": scores,
        "clarity": clarities,
        "summary_pt_BR": tdata.get("summary_pt_BR", ""),
        "strengths": tdata.get("strengths_pt_BR", []),
        "weaknesses": tdata.get("weaknesses_pt_BR", []),
        "careers": tdata.get("careers_pt_BR", [])
    }


if __name__ == "__main__":
    import json

    version = 70
    default_choice = "A"

    if len(sys.argv) > 1:
        try:
            version = int(sys.argv[1])
        except ValueError:
            pass

    if "--all-b" in sys.argv or "--all-B" in sys.argv:
        default_choice = "B"

    questions = get_questions(version)
    answers = [(q["id"], default_choice) for q in questions]

    result = run_mbti_test(answers, version)

    print(f"=== MBTI GURU — RESULTADO AUTÔNOMO ===\n")
    print(f"Versão: {version} perguntas")
    print(f"Tipo: {result['type_code']} — {result['name_pt_BR']}")
    print()
    print("Dimensões:")
    dim_names = {
        "EI": "E/I (Energia)", "SN": "S/N (Informação)",
        "TF": "T/F (Decisão)", "JP": "J/P (Estrutura)"
    }
    for dim in ["EI", "SN", "TF", "JP"]:
        score = result["scores"].get(dim, 50)
        pref = dim[0] if score > 50 else dim[1]
        pref_desc = {"E":"Extroversão","I":"Introversão","S":"Sensorial",
                     "N":"Intuição","T":"Racional","F":"Emocional","J":"Julgador","P":"Perceptivo"}
        print(f"  {dim_names[dim]}: {pref} ({pref_desc[pref]}) — {score}% — {result['clarity'][dim]}")
    print()
    print(f"Descrição: {result['summary_pt_BR']}")
    print()
    print("JSON completo:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
