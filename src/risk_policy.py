"""Conservative policy: do not treat missing prerequisites as established exploitability."""

def rate(applicability: str, impact: str) -> dict:
    valid_app = {'confirmed', 'potential', 'not_applicable', 'unknown'}
    valid_impact = {'high', 'medium', 'low', 'unknown'}
    if applicability not in valid_app or impact not in valid_impact:
        raise ValueError('Invalid policy input')
    if applicability == 'not_applicable':
        return {'decision': 'Low', 'rule': 'P0: confirmed non-applicability'}
    if applicability == 'unknown' or impact == 'unknown':
        return {'decision': 'Insufficient Evidence', 'rule': 'P1: decisive evidence missing'}
    matrix = {
        'confirmed': {'high': 'High', 'medium': 'High', 'low': 'Medium'},
        'potential': {'high': 'Medium', 'medium': 'Medium', 'low': 'Low'}
    }
    return {'decision': matrix[applicability][impact], 'rule': f'P2: {applicability} applicability + {impact} impact'}
