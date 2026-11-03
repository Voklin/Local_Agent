"""Miya can request a primary-model task without obtaining file-tool access."""
DELEGATE_TOOL = {'type':'function','function':{
    'name':'delegate_task','description':'Передать только задачу программирования или изменения кода основной модели Chat. Связь с IDE отключена. Бытовые вопросы, поиск и музыку не делегировать. Не утверждать, что задача уже выполнена.',
    'parameters':{'type':'object','properties':{'target':{'type':'string','enum':['chat']},
        'prompt':{'type':'string','description':'Конкретное задание основной модели'}},'required':['target','prompt'],'additionalProperties':False}}}
