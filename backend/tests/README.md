# backend/tests/

Suite pengujian backend. **Cara jalan:** `cd app && python3 -m pytest ../backend/tests -q`
(setelah `requirements-dev.txt` dipasang).

Target cakupan (BACKEND_PLAN Tahap B4/B5):

| Area | File | Yang diuji |
|---|---|---|
| Parser Excel | `test_parser.py` | header bergeser 0–N baris · nama kolom dicocokkan dari NAMA · `norm_*` · angka/komposisi |
| Sinkron & idempotensi | `test_upsert.py` | upsert tidak menggandakan · re-run aman · baris hilang → tanda "terhapus di sumber" |
| Kontrak API | `test_contract_state.py` | `/api/state` & `/api/admin` sesuai `docs/API_CONTRACT.md` (jsonschema) |

Fixture kecil boleh di `fixtures/`; **jangan commit berkas Excel produksi** — pakai hasil
`docs/scripts/analyze_workbook.py` atau mini-fixture buatan sendiri.
