"""Local assistant utilities: bounded arithmetic, notes and in-app timers."""
import ast
from datetime import datetime,timedelta
import json
import math
import operator
import threading
import time
import uuid
from agent.chat_store import APP_DIR,_atomic_write

# 200 notes of 4000 characters, including JSON escapes and Unicode text.
MAX_NOTES_BYTES = 6_000_000

ASSISTANT_TOOLS=[
 {'type':'function','function':{'name':'get_local_time','description':'Текущие местные дата, время и день недели этого ПК.','parameters':{'type':'object','properties':{},'additionalProperties':False}}},
 {'type':'function','function':{'name':'calculate','description':'Вычислить арифметическое выражение: + - * / // % ** и скобки. Без Python-кода и функций.','parameters':{'type':'object','properties':{'expression':{'type':'string'}},'required':['expression'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'save_note','description':'Сохранить локальную заметку по просьбе пользователя. Не меняет файлы проекта.','parameters':{'type':'object','properties':{'text':{'type':'string'},'title':{'type':'string'}},'required':['text'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'list_notes','description':'Найти свои локальные заметки по запросу или показать последние.','parameters':{'type':'object','properties':{'query':{'type':'string'}},'additionalProperties':False}}},
 {'type':'function','function':{'name':'set_timer','description':'Поставить таймер, пока LocalAgent и ПК работают. При закрытии приложения таймеры отменяются.','parameters':{'type':'object','properties':{'seconds':{'type':'integer','minimum':1,'maximum':86400},'label':{'type':'string'}},'required':['seconds'],'additionalProperties':False}}},
 {'type':'function','function':{'name':'list_timers','description':'Показать активные таймеры и их ID.','parameters':{'type':'object','properties':{},'additionalProperties':False}}},
 {'type':'function','function':{'name':'cancel_timer','description':'Отменить таймер по точному ID из list_timers или set_timer.','parameters':{'type':'object','properties':{'id':{'type':'string'}},'required':['id'],'additionalProperties':False}}},
]


def calculate(expression):
    if not isinstance(expression,str) or not 1<=len(expression)<=200:raise ValueError('Выражение: до 200 символов')
    tree=ast.parse(expression,mode='eval')
    if len(list(ast.walk(tree)))>50:raise ValueError('Слишком сложное выражение')
    operations={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.FloorDiv:operator.floordiv,ast.Mod:operator.mod,ast.Pow:operator.pow}
    def evaluate(node):
        if isinstance(node,ast.Constant) and type(node.value) in (int,float):value=node.value
        elif isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):value=evaluate(node.operand)*(1 if isinstance(node.op,ast.UAdd) else -1)
        elif isinstance(node,ast.BinOp) and type(node.op) in operations:
            left,right=evaluate(node.left),evaluate(node.right)
            if isinstance(node.op,ast.Pow) and abs(right)>12:raise ValueError('Степень слишком велика')
            value=operations[type(node.op)](left,right)
        else:raise ValueError('Разрешены только числа и арифметика')
        if not isinstance(value,(int,float)) or not math.isfinite(value) or abs(value)>1e100:raise ValueError('Результат вне допустимого диапазона')
        return value
    return evaluate(tree.body)


class AssistantService:
    def __init__(self,emit):
        self.emit=emit;self.notes_file=APP_DIR/'assistant-notes.json';self.lock=threading.RLock();self.timers={};self.closed=False

    def notes(self):
        if not self.notes_file.exists():return []
        if self.notes_file.stat().st_size>MAX_NOTES_BYTES:raise ValueError('Хранилище заметок слишком велико')
        with self.notes_file.open('rb') as source:raw=source.read(MAX_NOTES_BYTES+1)
        if len(raw)>MAX_NOTES_BYTES:raise ValueError('Хранилище заметок слишком велико')
        value=json.loads(raw.decode('utf8'))
        if not isinstance(value,list) or any(not isinstance(item,dict) for item in value):raise ValueError('Файл заметок повреждён; исходник сохранён')
        return value

    def execute(self,name,args):
        with self.lock:
            if self.closed:raise ValueError('Ассистент завершает работу')
            if name=='get_local_time':return {'ok':True,'local_time':datetime.now().astimezone().isoformat(),'weekday':datetime.now().weekday()}
            if name=='calculate':return {'ok':True,'result':calculate(args.get('expression'))}
            if name=='save_note':
                text=args.get('text');title=args.get('title','Заметка')
                if not isinstance(text,str) or not text.strip() or len(text)>4000 or not isinstance(title,str) or len(title)>120:raise ValueError('Заметка: текст до 4000 и заголовок до 120 символов')
                values=self.notes()
                if len(values)>=200:raise ValueError('Достигнут предел 200 заметок')
                item={'id':uuid.uuid4().hex,'title':title,'text':text,'created_at':datetime.now().astimezone().isoformat()}
                values.append(item)
                serialized=json.dumps(values,ensure_ascii=False,indent=2).replace('\n','\r\n')
                if len(serialized.encode('utf8'))>MAX_NOTES_BYTES:raise ValueError('Хранилище заметок слишком велико; прежние заметки сохранены')
                _atomic_write(self.notes_file,values);return {'ok':True,'note':item}
            if name=='list_notes':
                query=args.get('query','')
                if not isinstance(query,str) or len(query)>300:raise ValueError('Запрос заметок: до 300 символов')
                values=[item for item in self.notes() if query.casefold() in (str(item.get('title',''))+' '+str(item.get('text',''))).casefold()]
                return {'ok':True,'notes':values[-20:],'total':len(values)}
            if name=='set_timer':
                seconds=args.get('seconds');label=args.get('label','Таймер Лолы')
                if type(seconds) is not int or not 1<=seconds<=86400 or not isinstance(label,str) or not 1<=len(label)<=120:raise ValueError('Таймер: 1–86400 секунд, подпись до 120 символов')
                if len(self.timers)>=20:raise ValueError('Уже запущено 20 таймеров')
                key=uuid.uuid4().hex;deadline=datetime.now().astimezone()+timedelta(seconds=seconds)
                timer=threading.Timer(seconds,self.fire,args=(key,));timer.daemon=True
                self.timers[key]={'id':key,'label':label,'deadline':deadline.isoformat(),'monotonic':time.monotonic()+seconds,'timer':timer};timer.start()
                return {'ok':True,'timer':{'id':key,'label':label,'deadline':deadline.isoformat()},'requires_app_open':True}
            if name=='list_timers':return {'ok':True,'timers':[{'id':item['id'],'label':item['label'],'deadline':item['deadline'],'remaining_seconds':max(0,math.ceil(item['monotonic']-time.monotonic()))} for item in self.timers.values()]}
            if name=='cancel_timer':
                item=self.timers.pop(args.get('id'),None)
                if not item:return {'ok':False,'error':'Таймер не найден'}
                item['timer'].cancel();return {'ok':True,'cancelled':item['id']}
            return {'ok':False,'error':'Неизвестный инструмент ассистента'}

    def fire(self,key):
        with self.lock:
            item=self.timers.pop(key,None)
            if item:item['timer'].cancel()
            if item and not self.closed:self.emit({'event':'assistant_notice','title':'Лола · таймер завершён','text':item['label']})

    def shutdown(self):
        with self.lock:
            self.closed=True
            for item in self.timers.values():item['timer'].cancel()
            self.timers.clear()
