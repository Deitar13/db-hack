import random

from datacenter.models import Subject, Schoolkid, Lesson
from datacenter.models import Commendation, Mark, Chastisement
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def fix_academic_performance():

    commendations = [
        'Молодец!', 'Отлично!', 'Хорошо!',
        'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
        'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!', 'Очень хороший ответ!', 'Талантливо!',
        'Ты сегодня прыгнул выше головы!', 'Я поражен!',
        'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
        'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!',
        'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!',
        'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!']

    schoolkid_name = input('Введите ФИО ученика: ')

    random_commendation = random.choice(commendations)

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print('Ошибка поиска ученика, ученик не найден')
        return
    except MultipleObjectsReturned:
        print('Ошибка поиска ученика, найдено больше одного')
        return

    subject = Subject.objects.filter(
        year_of_study=schoolkid.year_of_study
    ).order_by('?').first()
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter__contains=schoolkid.group_letter,
        subject=subject
    ).order_by('?').first()
    Commendation.objects.create(
        text=random_commendation,
        schoolkid=schoolkid,
        created=lesson.date,
        teacher=lesson.teacher,
        subject=lesson.subject
    )
    print(f'Создана похвала: {random_commendation}')
    print(f'Предмет: {lesson.subject}')
    print(f'Для ученика: {schoolkid}')
    print(f'От учителя: {lesson.teacher}')
    chastisement = Chastisement.objects.filter(
        schoolkid__full_name__contains=schoolkid_name
    )
    chastisement.delete()
    print('Замечания удалены')

    Mark.objects.filter(
        schoolkid__full_name__contains=schoolkid_name,
        points__lte=3).update(points=5)
    print('Плохие оценки исправлены')
    return
