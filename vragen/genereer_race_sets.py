#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genereert Puzzel Race-puzzels per vraagset.

Gebruikt de relaties-logica uit maak_puzzels_race.py maar alleen voor de race-pool:
elke set krijgt 50/50 ×/÷ en +/−, met oplopende difficulty. Per set worden een
Excel-bestand (puzzels/) en frontend-pooldata (netto_race_sets.js) gemaakt.
"""
from __future__ import annotations

import json
import math
import random
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

from openpyxl import Workbook, load_workbook

PUZZLES_DIR = Path(__file__).parent.parent / 'puzzels'
sys.path.insert(0, str(PUZZLES_DIR))

from maak_puzzels_race import (  # noqa: E402
    OPERATORS,
    Puzzle,
    Relation,
    allocate_ids,
    difficulty_for,
    formula,
    load_questions,
    number_text,
    relation_values,
)

SETS_DIR = Path(__file__).parent / 'sets'
OUT_PUZZLES_DIR = PUZZLES_DIR / 'race_sets'
FRONTEND_OUT = Path(__file__).parent.parent / 'netto_race_sets.js'

OPERATOR_PAIRS = [('×', '÷'), ('+', '−')]
TARGET_PER_OPERATOR = 50
BOOST_WEIGHTS = {'×': 3, '÷': 3, '+': 1, '−': 1}


def choose_puzzles(questions: list, seed: int) -> list[Puzzle]:
    """Bouw race-puzzels met round-robin over de vier operators.

    Beurtvolgorde per ronde: ×, +, ÷, − — zodat keer/delen en plus/min gelijkmatig
    verdeeld raken én elkaar niet de waarden laten opvreten. Adaptief target:
    kleine sets kunnen niet 200 puzzels leveren (3 vragen per puzzel).
    """
    rng = random.Random(seed)
    available: defaultdict[Fraction, list[int]] = defaultdict(list)
    for index, question in enumerate(questions):
        available[question.answer].append(index)
    for ids in available.values():
        rng.shuffle(ids)

    target = max(4, min(TARGET_PER_OPERATOR, len(questions) // 12))
    puzzles: list[Puzzle] = []
    per_operator = Counter()
    relation_cache: dict = {}

    # Beurtvolgorde: × + ÷ − herhaald tot het target bereikt is.
    sequence = []
    for _ in range(target):
        sequence.extend(('×', '+', '÷', '−'))

    for operator in sequence:
        if per_operator[operator] >= target:
            continue
        value_set = frozenset(available)
        # Cache relatielijsten per (operator, waardeverzameling): de set krimpt maar,
        # dus een subset-check is voldoende en scheelt veel herberekenen.
        cache_key = (operator, value_set)
        if cache_key in relation_cache:
            all_rels = relation_cache[cache_key]
        else:
            all_rels = relation_values(operator, value_set)
            relation_cache[cache_key] = all_rels
        capacities = {value: len(ids) for value, ids in available.items()}
        feasible = [r for r in all_rels if fits_values(r, capacities)]
        if not feasible:
            continue
        # Moeilijkheidsband: wissel zodat de curve verdeeld raakt.
        scored = [(difficulty_for(operator, r)[0], difficulty_for(operator, r)[1], r) for r in feasible]
        scored.sort(key=lambda item: item[1])
        bands = [(0, 35), (35, 60), (60, 90), (90, 200)]
        chosen_band = None
        for low, high in bands:
            band = [item for item in scored if low <= item[1] < high]
            if band:
                chosen_band = band
                break
        pool = chosen_band or scored
        level, score, relation = rng.choice(pool[: min(24, len(pool))])
        ids = allocate_local(relation, available)
        puzzles.append(Puzzle(operator, ids, level, score))
        per_operator[operator] += 1
    return puzzles


def fits_values(values: tuple[Fraction, Fraction, Fraction], capacities: dict[Fraction, int]) -> bool:
    from collections import Counter as C
    need = C(values)
    return all(capacities.get(value, 0) >= count for value, count in need.items())


def allocate_local(values: tuple[Fraction, Fraction, Fraction], available: dict) -> tuple[int, int, int]:
    """Correcte allocatie: pop per keer dat de waarde voorkomt (origineel had off-by-one)."""
    chosen = []
    for value in values:
        ids = available.get(value)
        if not ids:
            raise RuntimeError("Interne fout: waarde niet beschikbaar.")
        chosen.append(ids.pop())
    return chosen[0], chosen[1], chosen[2]


def puzzle_to_frontend(p: Puzzle, questions: list, index: int, set_key: str) -> dict:
    q1, q2, q3 = (questions[i] for i in p.ids)
    return {
        'id': f'race-{set_key}-{index + 1:03d}',
        'number': index + 1,
        'name': f'Race #{index + 1}',
        'operator': p.operator,
        'q1_label': q1.text,
        'q1_answer': number_text(q1.answer),
        'q2_label': q2.text,
        'q2_answer': number_text(q2.answer),
        'q3_label': q3.text,
        'q3_answer': number_text(q3.answer),
        'calculation': formula(p.operator, (q1.answer, q2.answer, q3.answer)),
        'categories': [q1.category, q2.category, q3.category],
        'difficulty': p.level.lower().replace(' ', '-'),
        'difficulty_score': p.score,
    }


def write_excel(set_key: str, label: str, puzzles: list[Puzzle], questions: list) -> None:
    OUT_PUZZLES_DIR.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Puzzel Race'
    headers = ['Race #', 'Bewerking', 'Antwoord 1', 'Vraag 1', 'Antwoord 2', 'Vraag 2',
               'Antwoord 3', 'Vraag 3', 'Exacte formule', 'Difficulty', 'Difficulty score']
    ws.append(headers)
    for number, p in enumerate(puzzles, start=1):
        q1, q2, q3 = (questions[i] for i in p.ids)
        ws.append([
            number, p.operator,
            number_text(q1.answer), q1.text,
            number_text(q2.answer), q2.text,
            number_text(q3.answer), q3.text,
            formula(p.operator, (q1.answer, q2.answer, q3.answer)),
            p.level, p.score,
        ])
    for column, width in {'A': 10, 'B': 10, 'C': 12, 'D': 70, 'E': 12, 'F': 70, 'G': 12, 'H': 70, 'I': 24, 'J': 16, 'K': 14}.items():
        ws.column_dimensions[column].width = width
    ws.freeze_panes = 'A2'
    wb.save(OUT_PUZZLES_DIR / f'race_set_{set_key}.xlsx')


def main():
    # Verwerk eerst de basisset-bestanden (met alleen questions van die set)
    all_pools = {}
    summary = []
    seeds = {
        'standaard': 1001, 'nederland': 1002, 'usa': 1003, 'europa': 1004,
        'azie': 1005, 'afrika': 1006, 'oceanie': 1007, 'latijns_amerika': 1008,
        'ruimte_wetenschap': 1009, 'dierenrijk': 1010, 'sport': 1011, 'popcultuur': 1012,
    }
    for set_file in sorted(SETS_DIR.glob('set_*.xlsx')):
        set_key = set_file.stem.replace('set_', '')
        questions, skipped = load_questions(set_file)
        # Filter vragen zonder status 'nieuw' hoeft niet; laad_questions leest 'Alle vragen'.
        if len(questions) < 30:
            summary.append((set_key, len(questions), 0, 'te weinig vragen'))
            continue
        puzzles = choose_puzzles(questions, seeds.get(set_key, 2000))
        all_pools[set_key] = [puzzle_to_frontend(p, questions, i, set_key) for i, p in enumerate(puzzles)]
        write_excel(set_key, set_key, puzzles, questions)
        ops = Counter(p.operator for p in puzzles)
        summary.append((set_key, len(questions), len(puzzles), dict(ops)))

    # Frontend JS schrijven
    js = 'window.NETTO_RACE_SETS = ' + json.dumps(all_pools, ensure_ascii=False, separators=(',', ':')) + ';\n'
    FRONTEND_OUT.write_text(js, encoding='utf-8')

    print(f'{"set":22s} {"vragen":>7s} {"puzzels":>8s}  operators')
    for row in summary:
        print(f'{row[0]:22s} {row[1]:7d} {row[2]:8d}  {row[3]}')
    print(f'\nFrontend: {FRONTEND_OUT}')
    print(f'Excel: {OUT_PUZZLES_DIR}')


if __name__ == '__main__':
    main()
