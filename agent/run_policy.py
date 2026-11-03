"""Explicit external-API spending estimates and conservative model resource policy."""
from decimal import Decimal,ROUND_CEILING
import math
from .request_budget import BudgetExceededError

DEFAULT_SPENDING={'enabled':False,'amount':1.0,'input_per_million':0.0,'output_per_million':0.0,'currency':'USD'}


class SpendingLimitError(BudgetExceededError):
    """An opt-in planning threshold cannot admit another estimated request."""


class ModelCapacityError(BudgetExceededError):
    """A model server reported memory exhaustion; retrying the same load is unsafe."""


def validate_spending(value=None):
    value=DEFAULT_SPENDING if value is None else value
    if not isinstance(value,dict) or type(value.get('enabled',False)) is not bool:raise ValueError('Некорректный денежный бюджет')
    result={**DEFAULT_SPENDING,**{key:value[key] for key in DEFAULT_SPENDING if key in value}}
    for key in ('amount','input_per_million','output_per_million'):
        number=result[key]
        if type(number) not in (int,float) or not math.isfinite(number) or not 0<=number<=1_000_000:raise ValueError('Бюджет и цены должны быть конечными неотрицательными числами')
    if result['enabled'] and (not result['amount'] or not(result['input_per_million'] or result['output_per_million'])):raise ValueError('Для бюджета укажите сумму и хотя бы одну цену за миллион токенов')
    if result['currency'] not in ('USD','EUR','RUB'):raise ValueError('Валюта бюджета: USD, EUR или RUB')
    return result


def priced_tokens(policy,incoming,outgoing):
    """Integer nanocurrency avoids float subtraction at an admission boundary."""
    amount=Decimal(str(policy['input_per_million']))*max(0,incoming)+Decimal(str(policy['output_per_million']))*max(0,outgoing)
    return int((amount*1000).to_integral_value(rounding=ROUND_CEILING))


def spending_snapshot(connection,run_id):
    row=connection.execute('SELECT data FROM runs WHERE id=?',(run_id,)).fetchone()
    if not row:return None
    import json
    run=json.loads(row[0]);root=run.get('parent_id') or run_id
    if root!=run_id:run=json.loads(connection.execute('SELECT data FROM runs WHERE id=?',(root,)).fetchone()[0])
    policy=run.get('spending_policy',{})
    if not policy.get('enabled'):return None
    total=reserved=unknown=0
    if run.get('journal_id'):
        query="SELECT a.data FROM inference_attempts a JOIN runs r ON r.id=a.run_id LEFT JOIN runs p ON p.id=r.parent_id WHERE (r.parent_id IS NULL AND r.chat_id=? AND json_extract(r.data,'$.journal_id')=?) OR (p.chat_id=? AND json_extract(p.data,'$.journal_id')=?)"
        values=(run['chat_id'],run['journal_id'],run['chat_id'],run['journal_id'])
    else:query='SELECT a.data FROM inference_attempts a JOIN runs r ON r.id=a.run_id WHERE r.id=? OR r.parent_id=?';values=(root,root)
    for row in connection.execute(query,values):
        attempt=json.loads(row[0]);usage=attempt.get('usage');reserve=attempt.get('reservation',{})
        estimate=priced_tokens(policy,reserve.get('input_tokens_estimate',0),reserve.get('output_tokens_reserved',0))
        if usage is not None:total+=priced_tokens(policy,usage['input_tokens'],usage['output_tokens'])
        elif attempt.get('state')=='active':reserved+=estimate
        elif attempt.get('http_attempts'):total+=estimate;unknown+=1
    limit=int(Decimal(str(policy['amount']))*1_000_000_000)
    return {'root_id':root,'currency':policy['currency'],'limit':limit/1e9,'estimated_spent':total/1e9,'reserved':reserved/1e9,
        'unknown_attempts':unknown,'remaining':max(0,limit-total-reserved)/1e9,'_remaining_nanos':limit-total-reserved,'policy':policy}


def require_spending(connection,run_id,reservation):
    value=spending_snapshot(connection,run_id)
    if value is None:return
    estimate=priced_tokens(value['policy'],reservation.get('input_tokens_estimate',0),reservation.get('output_tokens_reserved',0))
    if estimate>value['_remaining_nanos'] or not any(reservation.values()):
        raise SpendingLimitError(f"Порог расходов {value['limit']:g} {value['currency']} на задачу и её детей не позволяет следующий запрос. Измените бюджет в настройках и продолжите задачу. Фактический счёт провайдера может отличаться от оценки.")


def capacity_failure(error):
    body=getattr(error,'body',None)
    text=str(body if body is not None else error).lower()
    return any(word in text for word in ('out of memory','out_of_memory','insufficient_memory','cuda_error_out_of_memory','нехватка памяти'))
