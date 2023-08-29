import NeuroNetLibrary as nn
import NeuroNluLibrary as nlu
import NeuroVoiceLibrary as nv
import json


def get_recepients():
    with open("./recepients.json", 'r') as f:
        recepients = json.load(f)
    return recepients

def get_operator():
    with open("./operator.json", 'r') as f:
        operator = json.load(f)
    return operator['number']

def promt_txt():
    with open("./prompt_txt.json", 'r') as f:
        prompt_txt = json.load(f)
    return prompt_txt

def get_record():
    
    with nv.listen(entities=entity_list(), recognition_timeout=60000) as r:
        nn.log(r)
    return r

def entity_list():  
    
    entity_list = ['confirm', 'wrong_time', 'repeat', 'recommendation_score',
                   'recommendation', 'question']
    return entity_list

#hello logic unit

def hello(*args):
    
    nn.call(*args)
    nn.log('logic', 'hello_main')
    nv.say(prompt_txt['hello']['main'])
    r = get_record()
    hello_logic(r)

def hello_null():
    
    if nn.counter('hello_null', '+') >= 2:
        nn.log('event', 'hello_null=1')
        hangup_null()
    nn.log('logic', 'hello_null')
    r = get_record()
    nv.say(prompt_txt['hello']['hello_null'])
    hello_logic(r)

def hello_repeat():

    nn.log('logic', 'hello_repeat')
    nv.say(prompt_txt['hello']['hello_repeat'])
    recommend_main()

def hello_logic(r):

nn.log('logic', 'hello_logic')

    if not r:
        nn.log ('condition', 'NULL')
        return hello_null()
    elif r.entity('confirm') == 'true':
        nn.log('condition','confirm=true')
        return recommend_main()
    elif r.entity('confirm') == 'false':
        nn.log('condition','confirm=false')
        return hangup_wrong_time()
    elif r.entity('wrong_time') == 'true':
        nn.log('condition','wrong_time=true')
        return hangup_wrong_time()
    
    if r.entity('repeat') == 'true':
        nn.log('condition','repeat=true')
        return hello_repeat()

#main logic unit

def main_logic(r):

    nn.log('logic', 'main_logic')

    if not r:
        nn.log('condition', 'NULL')
        recommend_null()
    
    if r.entity('recommendation_score') in range(0,9):
        nn.log('condition','recommendation_score')
        hangup_negative()

    if r.entity('recommendation_score') in [9,10]:
        nn.log('condition','recommendation_score')
        hangup_positive()
    
    if r.entity('recommendation') == 'negative':
        nn.log('condition','recommendation=negative')
        recommend_score_negative()

    if r.entity('recommendation') == 'neutral':
        nn.log('condition','recommendation=neutral')
        recommend_score_neutral()

    if r.entity('recommendation') == 'positive':
        nn.log('condition','recommendation=positive')
        recommend_score_positive()

    if r.entity('repeat') == 'true':
        nn.log('condition','repeat=true')
        recommend_repeat()

    if r.entity('recommendation') == 'dont know':
        nn.log('condition','recommendation=dont know')
        recommend_repeat_2()
    
    if r.entity('wrong_time') == 'true':
        nn.log('condition','wrong_time=true')
        hangup_wrong_time()

    if r.entity('question') == 'true':
        nn.log('condition','question=true')
        forward()

    nn.log('condition', 'DEFAULT')
    recommend_default()
        
def recommend_null():

    if nn.counter('recommend_null', '+') >= 2:
        nn.log('event', 'recommend_null=1')
        hangup_null()
    r = get_record()
    nn.log('goto', 'hello_null')
    nv.say(prompt_txt['main']['recommend_null'])
    main_logic(r)

def recommend_default():

    if nn.counter('recommend_default', '+') >= 2:
        nn.log('event', 'recommend_default=1')
        hangup_null()
    r = get_record()
    nn.log('goto', 'recommend_default')
    nv.say(prompt_txt['main']['recommend_default'])
    main_logic(r)

def recommend_score_negative():

    nn.log('goto', 'recommend_score_negative')
    nv.say(prompt_txt['main']['recommend_score_negative'])
    hangup_positive()

def recommend_score_positive():

    nn.log('goto', 'recommend_score_positive')
    nv.say(prompt_txt['main']['recommend_score_positive'])
    recommend_score_neutral()

def recommend_score_neutral():

    nn.log('goto', 'recommend_score_neutral')
    nv.say(prompt_txt['main']['recommend_score_neutral'])
    recommend_default,()

def recommend_repeat():

    nn.log('goto', 'recommend_score_repeat')
    nv.say(prompt_txt['main']['recommend_score_repeat'])
    recommend_score_negative()

def recommend_repeat_2():

    nn.log('goto', 'recommend_score_repeat_2')
    nv.say(prompt_txt['main']['recommend_score_repeat_2'])
    hangup_negative()
    
#hangup

def hangup_positive():
    
    nn.log('tag', 'High score')
    nv.say(prompt_txt['hangup']['hangup_positive'])
    nv.hangup()

def hangup_negative():
    nn.log('tag', 'Low score')
    nv.say(prompt_txt['hangup']['hangup_negative'])
    nv.hangup()

def hangup_wrong_time():
    nn.log('tag', 'No time to talk')
    nv.say(prompt_txt['hangup']['hangup_wrong_time'])
    nv.hangup()

def hangup_null():
    nn.log('tag', 'problems with understanding')
    nv.say(prompt_txt['hangup']['hangup_null'])
    nv.hangup()

#forwarding to operator

def forward():
    nn.log('goto', 'bridge action')
    nv.say(prompt_txt['forward'])
    nv.bridge(get_operator())


###start call across all recepients:
recepients = get_recepients()
for recepient in recepients:
    hello(recepient['data'])
