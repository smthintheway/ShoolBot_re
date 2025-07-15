greeting = 'Здравствуй'
user_edit_form = 'Введите ваш класс:'
user_edit_group = 'Введите вашу группу:\n(Если их нет поставте 0)'

def user_info_template(username,form,group,privileges,tg_id):
    return f'@{username}\n{tg_id}\nКласс: {form}\nГруппа: {group}\nСтатус: {privileges}'

