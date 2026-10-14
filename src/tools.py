import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = 'https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview'


def lookup_environment(asset_id: str) -> dict:
    data = json.loads((ROOT / 'data/environment.json').read_text(encoding='utf-8'))
    asset = next((a for a in data['assets'] if a['id'] == asset_id), None)
    if asset is None:
        return {'status': 'not_found', 'asset_id': asset_id, 'source_mode': 'simulated'}
    evidence = [e for e in data['evidence'] if e['id'] in asset.get('evidence_ids', [])]
    # Include contextual evidence, explicitly labeled as context, not FILE04-specific proof.
    context = [e for e in data['evidence'] if e['id'] == 'S05' and e['id'] not in asset.get('evidence_ids', [])]
    return {'status': 'ok', 'asset': asset, 'evidence': evidence,
            'context_evidence': context, 'source_mode': 'simulated',
            'snapshot_date': data.get('snapshot_date')}


def _clean_markdown(raw: str) -> str:
    raw = re.sub(r'(?s)^---\s*\n.*?\n---\s*\n', '', raw)
    raw = re.sub(r'!\[([^]]*)\]\([^)]*\)', r'\1', raw)
    raw = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', raw)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    raw = re.sub(r'\n{3,}', '\n\n', raw)
    return raw.strip()


def lookup_external_reference(url: str) -> dict:
    if url != REFERENCE:
        return {'status': 'blocked', 'reason': 'URL not allowlisted'}
    # Microsoft Learn supports a markdown representation; avoid passing HTML headers to the LLM.
    markdown_url = url + '?accept=text/markdown'
    try:
        req = Request(markdown_url, headers={
            'User-Agent': 'Assignment2-Risk-Agent/0.2',
            'Accept': 'text/markdown'
        })
        with urlopen(req, timeout=15) as response:
            content_type = response.headers.get('Content-Type', '')
            raw = response.read(300000).decode('utf-8', errors='replace')
        if '<html' in raw[:1000].lower() or '<!doctype html' in raw[:1000].lower():
            return {'status': 'unavailable', 'url': url, 'source_mode': 'live_lookup_failed',
                    'error_type': 'UnexpectedHTML', 'reason': 'Markdown endpoint returned HTML'}
        text = _clean_markdown(raw)
        if len(text) < 150 or not re.search(r'\bSMB\b|signing', text, re.I):
            return {'status': 'unavailable', 'url': url, 'source_mode': 'live_lookup_failed',
                    'error_type': 'InsufficientContent'}
        from datetime import datetime, timezone
        return {'status': 'ok', 'url': url, 'retrieval_url': markdown_url,
                'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
                'source_mode': 'live', 'content_type': content_type,
                'content_excerpt': text[:16000], 'note': 'Retrieved reference content; verify relevance to FILE04.'}
    except Exception as exc:
        return {'status': 'unavailable', 'url': url, 'error_type': type(exc).__name__,
                'source_mode': 'live_lookup_failed'}
