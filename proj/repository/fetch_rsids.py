import pandas as pd
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_rsids_batch(coords, build='hg38'):
    server = "https://rest.ensembl.org" if build == 'hg38' else "https://grch37.rest.ensembl.org"
    ext = "/vep/human/region"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    payload = {"variants": [f"{c.replace(':', ' ')} {c.split(':')[1]} ." for c in coords]}
    
    try:
        r = requests.post(server + ext, headers=headers, data=json.dumps(payload), timeout=15)
        if r.status_code == 429:
            retry_after = float(r.headers.get("Retry-After", 1))
            time.sleep(retry_after)
            return fetch_rsids_batch(coords, build)
        if not r.ok: return {c: "Query_Error" for c in coords}
        mapping = {}
        for entry in r.json():
            inp = entry.get('input').split(' ')
            key = f"{inp[0]}:{inp[1]}"
            colocs = entry.get('colocated_variants', [])
            rsid = next((cv['id'] for cv in colocs if cv['id'].startswith('rs')), "Not_Found")
            mapping[key] = rsid
        return mapping
    except Exception:
        return {c: "Timeout_or_Error" for c in coords}

snp_file = 'proj/data/test_snp.csv' 
df = pd.read_csv(snp_file, sep='\s+', engine='python')
df['temp_coord'] = df['Chr'].astype(str) + ":" + df['Position'].astype(str)
unique_coords = df['temp_coord'].unique().tolist()

batch_size = 200
chunks = [unique_coords[i:i + batch_size] for i in range(0, len(unique_coords), batch_size)]

print(f"Processing {len(unique_coords)} SNPs in {len(chunks)} parallel batches...")

all_results = {}
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(lambda c: fetch_rsids_batch(c, build='hg38'), chunks))

for batch_result in results:
    all_results.update(batch_result)
df['RSID'] = df['temp_coord'].map(all_results)
df_final = df.drop(columns=['temp_coord'])
df_final.to_csv('snp_panel_final.csv', index=False)
print(f"\nProcessing complete! Saved to snp_panel_final.csv")