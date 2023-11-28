from core.models.model_func import get_filter_id_tg

def user_is_verified(id_tg: int):
    user_data = get_filter_id_tg(id_tg)
    try:
        if user_data.valid is True:
            return({'user_id_in_serv':user_data.id_server,'local_id':user_data.id,})
        else:
            # у юзера нет валидации через почту, сделать повторную отправку
            return False
    except AttributeError: # вообще нет такокого юзера
        return