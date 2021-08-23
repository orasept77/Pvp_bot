from handlers.psr.models.variant import Variant
from typing import List


def is_eligible_for_next_round(variants:List[Variant], round_user_variants: list):
    variant_users = {}
    for variant in variants:
        variant_users[variant.id] = []
    for i in round_user_variants:
        variant_users[i['variant_id']].append(i['user_id'])
    
    picked_variants_ids = [key for key,val in variant_users.items() if val]
        
    if len(picked_variants_ids) > 2:
        return (False, [i['user_id'] for i in round_user_variants])
    elif len(picked_variants_ids) == 1:
        return (False, [i['user_id'] for i in round_user_variants])
    elif len(picked_variants_ids) == 2:
        var_id1 = picked_variants_ids[0]
        var_id2 = picked_variants_ids[1]
        var1 = next((i for i in variants if i.id == picked_variants_ids[0]))
        var2 = next((i for i in variants if i.id == picked_variants_ids[1]))
        if var2.id in [i.id for i in var1.variants_beat]:
            return (True, variant_users[var1.id])
        else:
            return (True, variant_users[var2.id])
    return (False, [i['user_id'] for i in round_user_variants])