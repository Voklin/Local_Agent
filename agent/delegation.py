"""Miya can request a primary-model task without obtaining file-tool access."""
DELEGATE_TOOL = {'type':'function','function':{
    'name':'delegate_task','description':'Передать сложную задачу основной модели Chat или IDE. Не утверждать, что задача уже выполнена.',
    'parameters':{'type':'object','properties':{'target':{'type':'string','enum':['chat','ide']},
        'prompt':{'type':'string','description':'Конкретное задание основной модели'}},'required':['target','prompt'],'additionalProperties':False}}}
