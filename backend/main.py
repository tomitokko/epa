from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path
from typing import List

app = FastAPI()

DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'standards.json'

with open(DATA_PATH) as f:
    STANDARDS = json.load(f)

class ReviewRequest(BaseModel):
    standard: str
    evidence: int
    text: str

class KSBFeedback(BaseModel):
    ksb: str
    required: bool
    tagged: bool
    passMet: bool
    distinctionMet: bool
    suggestion: str

@app.post('/review')
def review_evidence(req: ReviewRequest) -> List[KSBFeedback]:
    standard = STANDARDS.get(req.standard)
    if not standard:
        raise HTTPException(status_code=404, detail='Standard not found')
    evid_key = str(req.evidence)
    required = standard['evidence'].get(evid_key, [])
    result = []
    for ksb in required:
        criteria = standard['ksbs'].get(ksb, {})
        tagged = ksb in req.text
        # naive pass/distinction detection
        passMet = bool(criteria.get('pass') and criteria['pass'].lower() in req.text.lower())
        distinctionMet = bool(criteria.get('distinction') and criteria['distinction'].lower() in req.text.lower())
        suggestion = ''
        if not tagged:
            suggestion += f'Tag this section as {ksb}. '
        if not passMet:
            suggestion += 'Pass not met.'
        elif not distinctionMet:
            suggestion += 'Consider adding more detail for Distinction.'
        result.append({
            'ksb': ksb,
            'required': True,
            'tagged': tagged,
            'passMet': passMet,
            'distinctionMet': distinctionMet,
            'suggestion': suggestion.strip()
        })
    return result
