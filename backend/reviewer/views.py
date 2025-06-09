import json
from pathlib import Path
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

DATA_PATH = Path(__file__).resolve().parents[2] / 'data' / 'standards.json'
with open(DATA_PATH) as f:
    STANDARDS = json.load(f)

@csrf_exempt
def review(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST allowed')
    try:
        body = json.loads(request.body)
        standard_id = body['standard']
        evidence_num = body['evidence']
        text = body['text']
    except (KeyError, json.JSONDecodeError):
        return HttpResponseBadRequest('Invalid JSON')

    standard = STANDARDS.get(standard_id)
    if not standard:
        return JsonResponse({'error': 'Standard not found'}, status=404)

    required = standard['evidence'].get(str(evidence_num), [])
    result = []
    for ksb in required:
        criteria = standard['ksbs'].get(ksb, {})
        tagged = ksb in text
        passMet = bool(criteria.get('pass') and criteria['pass'].lower() in text.lower())
        distinctionMet = bool(criteria.get('distinction') and criteria['distinction'].lower() in text.lower())
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
            'suggestion': suggestion.strip(),
        })
    return JsonResponse(result, safe=False)
