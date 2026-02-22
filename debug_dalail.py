import sys
import os
import json

sys.path.append(os.getcwd())

from update_dalail_full import DALAIL_DATA
from update_dalail_english import DALAIL_ENGLISH

print(f"DALAIL_DATA keys: {list(DALAIL_DATA.keys())}")
print(f"DALAIL_ENGLISH keys: {list(DALAIL_ENGLISH.keys())}")

ORDER = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
final_data = []

for day_id in ORDER:
    eng = DALAIL_ENGLISH.get(day_id)
    arb = DALAIL_DATA.get(day_id)
    print(f"{day_id}: English={eng is not None}, Arabic={arb is not None}")
    if eng and arb:
        final_data.append({"id": day_id})

print(f"Final list length: {len(final_data)}")
