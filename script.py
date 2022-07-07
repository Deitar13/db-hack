import random

from datacenter.models import Subject, Schoolkid, Lesson, Commendation


def create_commendation():

    some_commendations = '''Молодец!
    Отлично!
    Хорошо!
    Гораздо лучше, чем я ожидал!
    Ты меня приятно удивил!
    Великолепно!
    Прекрасно!
    Ты меня очень обрадовал!
    Именно этого я давно ждал от тебя!
    Сказано здорово – просто и ясно!
    Ты, как всегда, точен!
    Очень хороший ответ!
    Талантливо!
    Ты сегодня прыгнул выше головы!
    Я поражен!
    Уже существенно лучше!
    Потрясающе!
    Замечательно!
    Прекрасное начало!
    Так держать!
    Ты на верном пути!
    Здорово!
    Это как раз то, что нужно!
    Я тобой горжусь!
    С каждым разом у тебя получается всё лучше!
    Мы с тобой не зря поработали!
    Я вижу, как ты стараешься!
    Ты растешь над собой!
    Ты многое сделал, я это вижу!
    Теперь у тебя точно все получится!
    '''

    schoolkid = input('Введите ФИО ученика: ')


    commendations_list = some_commendations.split('\n')
    random_commendations = random.choice(commendations_list)

    child = Schoolkid.objects.filter(full_name__contains=f'{schoolkid}')

    if len(child) > 1 or len(child) == 0:
        print('ПРОБЛЕМА С ПОИСКОМ УЧЕНИКА, РЕЗУЛЬТАТОВ ПОИСКА:', len(child))
        return

    else:
        subject = Subject.objects.filter(
            year_of_study=child[0].year_of_study
        ).order_by('?').first()

        lesson = Lesson.objects.filter(
            year_of_study=child[0].year_of_study,
            group_letter__contains=child[0].group_letter,
            subject=subject
        ).order_by('?').first()

        Commendation.objects.create(
            text=f'{random_commendations}',
            schoolkid=child[0],
            created=lesson.date,
            teacher=lesson.teacher,
            subject=lesson.subject
        )

        print(f'Создана похвала: {random_commendations}')
        print(f'Предмет: {lesson.subject}')
        print(f'Для ученика: {child[0]}')
        print(f'От учителя: {lesson.teacher}')
        return
