import json, os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

ROOT=Path(__file__).parent
PDF_DIR=ROOT/'sample_leases'/'sample_leases'
OUT=ROOT/'leases.json'
MODEL='gpt-5.6-luna'

def read_pdf(path):
    return '\n'.join(page.extract_text() or '' for page in PdfReader(str(path)).pages)

def main():
    load_dotenv(ROOT.parent/'.env')
    key=os.getenv('PORTKEY_API_KEY')
    if not key or key.startswith('paste_'):
        raise SystemExit('Add your real PORTKEY_API_KEY to the root .env before extraction.')
    client=OpenAI(api_key=key,base_url='https://api.portkey.ai/v1',default_headers={'x-portkey-api-key':key})
    schema={'property_name':'string','address':'string','city':'string','state':'string','zip_code':'string','latitude':'number or null','longitude':'number or null','property_type':'string','tenant':'string','lease_start':'YYYY-MM-DD or null','lease_end':'YYYY-MM-DD or null','monthly_rent':'number or null','annual_rent':'number or null','annual_expenses':'number or null','annual_noi':'number or null','purchase_price':'number or null','cap_rate':'number or null','occupancy':'number or null','notes':'string'}
    records=[]
    for path in sorted(PDF_DIR.glob('*.pdf')):
        prompt=f"Extract this lease into one JSON object matching this schema: {json.dumps(schema)}. Use null for unknown values; do not invent coordinates. Source file: {path.name}\nDocument:\n{read_pdf(path)[:60000]}"
        response=client.chat.completions.create(model=MODEL,response_format={'type':'json_object'},messages=[{'role':'system','content':'You are a careful commercial real-estate analyst. Return only valid JSON.'},{'role':'user','content':prompt}])
        item=json.loads(response.choices[0].message.content); item['source_file']=path.name; records.append(item)
        print('Extracted',path.name)
    OUT.write_text(json.dumps(records,indent=2),encoding='utf-8'); print(f'Wrote {len(records)} records to {OUT}')

if __name__=='__main__': main()
