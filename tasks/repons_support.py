from celery import app
from core.utils.make_request import bot_mess_sender
from core.models.model_func import get_all_query_question,response_support
from tasks.logging_conf import logg
@logg
@app.shared_task(name='resp_support')
def resp_support():
    all_active_question=get_all_query_question().filter_by(verified=False)
    for question in all_active_question:
        user_tg=question.user.id_tg
        bot_mess_sender(user_tg, f'Пользователь {user_tg} задает вопрос- \n\n {question.question}') #Отправляем сообщение разрабу
        response_support(question.id, True) #Маркеруем сообщение как отправленное