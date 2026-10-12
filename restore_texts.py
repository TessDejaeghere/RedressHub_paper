"""Restore the full annotated texts locally (project members only; never commit the result).

The repository contains no article texts, only character offsets and the URL and SHA-256 checksum of every
text (ls_real/texts.csv). If you have the full texts, this script checks them against the checksums and
writes ls_real/texts_full.json, which the notebooks then use to show span texts and to recompute the
duplicate check. The analyses themselves do not need the texts.

Usage:
    python restore_texts.py path/to/texts_full.json          # {text_key: text}, as kept by the project
    python restore_texts.py path/to/folder_with_full_exports # the original Label Studio exports (export_*.json)
"""
import hashlib
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'ls_real')
POOLS = [('iaa', 'export_reann_cira.json', 'export_reann_elke.json'),
         ('cira_solo', 'export_hesretro_cira.json', 'export_cross_elke.json'),
         ('elke_solo', 'export_hesretro_elke.json', 'export_cross_cira.json'),
         ('iaa_nl', 'export_reann_elke_nl.json', 'export_reann_a3.json'),
         ('elke_solo_nl', 'export_hesretro_elke_nl.json', 'export_cross_a3.json')]


def read_source(path):
    if os.path.isfile(path):
        return json.load(open(path, encoding='utf-8'))
    texts = {}
    for pool, fa, fb in POOLS:
        for f in (fa, fb):
            for t in json.load(open(os.path.join(path, f), encoding='utf-8')):
                texts[f'{pool}:{t["data"]["orig_task_id"]}'] = t['data']['text']
    return texts


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    meta = pd.read_csv(os.path.join(D, 'texts.csv')).set_index('text_key')
    texts = read_source(sys.argv[1])
    missing = sorted(set(meta.index) - set(texts))
    bad = [k for k in meta.index if k in texts and hashlib.sha256(texts[k].encode('utf-8')).hexdigest() != meta.loc[k, 'sha256']]
    if missing or bad:
        sys.exit(f'Not restored. Missing texts: {missing}; checksum mismatches: {bad}')
    out = os.path.join(D, 'texts_full.json')
    json.dump({k: texts[k] for k in meta.index}, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{len(meta)} texts verified and written to {out} (excluded from git by .gitignore)')


if __name__ == '__main__':
    main()
