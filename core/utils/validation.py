from email_validator import validate_email, EmailNotValidError
ERROR_RESPONSES={'str_not_int':'Значение слишком большое или не является числом',}
def mail_validate(text: str) -> dict:
    try:
        email = validate_email(text, check_deliverability=False)
        return {'status':True,'text':email.normalized}
    except EmailNotValidError:
        return {'status':False,'text':'Не верный формат email, повторите.'}
    
def str_to_int(val: str, check_count_char: int = 5) -> int or bool:
    # sourcery skip: remove-unnecessary-cast
    if val.isnumeric() and check_count_char is None:
        return int(val)
    elif check_count_char is not None:
        return int(val) if str(val).isnumeric() and len(str(val))<=check_count_char else False
    else:
        return False

def check_hour(time: str) -> bool:
    return  len(time)==5 and time[2] == ":"
