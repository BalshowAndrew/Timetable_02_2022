from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# импорт для генерации csv файлов:
import csv
# импорт для генерации PDF файлов:
from django.http import FileResponse
import io
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFountGryphs = 0
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



from .forms import *
from .models import Classes, Queries


def index(request):
    context = {
        'title': 'Расписание кафедры',
    }
    return render(request, 'classes/index.html', context=context)




def show_person(request):
    context = {
        'title': 'Личный кабинет',
    }
    return render(request, 'classes/person.html', context=context)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'classes/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('person')


def logout_user(request):
    logout(request)
    Queries.objects.all().delete()
    return redirect('home')


def get_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('result')
    else:
        form = QueryForm()
    return render(request, 'classes/query.html', {'form': form})


# Генерация ответа на запрос пользователя
def get_result(request):
    query = Queries.objects.order_by('pk').last()
    if query.category == 'P':
        result = Classes.objects.filter(
            teacher_id=request.user.pk,
            category='P',
            start_day__gte=query.first_day,
            start_day__lte=query.last_day
        )
    elif query.category == 'L':
        result = Classes.objects.filter(
            teacher_id=request.user.pk,
            category='L',
            start_day__gte=query.first_day,
            start_day__lte=query.last_day
        )

    context = {
        'query': query,
        'result': result,
        'title': 'Результат запроса',

    }
    # Генерация сообщения об отсутствии значений в результате запроса
    if len(result) == 0:
        return render(request, 'classes/non_result.html', context=context)
    else:
        return render(request, 'classes/result.html', context=context)


# Генерация csv файла по результату запроса пользователя
def result_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=result.csv'
    writer = csv.writer(response)
    # выбираем данные из моделей:
    query = Queries.objects.order_by('pk').last()
    if query.category == 'P':
        result = Classes.objects.filter(
            teacher_id=request.user.pk,
            category='P',
            start_day__gte=query.first_day,
            start_day__lte=query.last_day
        )
        # заголовки столбцов для практических занятий:
        writer.writerow(['Группа', 'Начало цикла', 'Окончание цикла', 'Время занятия'])
        # заполняем ячейки данными, полученными по запросу:
        for r in result:
            writer.writerow([r.group, r.start_day, r.end_day, r.start])

    elif query.category == 'L':
        result = Classes.objects.filter(
            teacher_id=request.user.pk,
            category='L',
            start_day__gte=query.first_day,
            start_day__lte=query.last_day
        )
        # заголовки столбцов для лекций:
        writer.writerow(['факультет', 'Курс', 'Дата проведения', 'Время проведения'])
        # заполняем ячейки данными, полученными по запросу:
        for r in result:
            writer.writerow([r.faculty, r.course, r.start_day, r.start])

    return response


# Генерация PDF файла по результатам запроса пользователя
def result_pdf(request):
    buf = io.BytesIO()
    # выбираем данные из моделей:
    global classesName
    global resultList
    user = User.objects.get(id=request.user.pk)
    query = Queries.objects.order_by('pk').last()
    if query.category == 'P':
        result = Classes.objects.filter(
            teacher_id=request.user.pk,
            category='P',
            start_day__gte=query.first_day,
            start_day__lte=query.last_day
        )
        classesName = 'практических занятий'
        resultList = [['Группа', 'Начало цикла', 'Окончание цикла', 'Время занятий']]
        for r in result:
            resultList.append([r.group, r.start_day, r.end_day, r.start])
    elif query.category == 'L':
        result = Classes.objects.filter(
            teacher_id=request.user.pk,
            category='L',
            start_day__gte=query.first_day,
            start_day__lte=query.last_day
        )
        classesName = 'лекций'
        resultList = [['Факультет', 'Курс', 'Дата проведения', 'Время проведения']]
        for r in result:
            resultList.append([r.faculty, r.course, r.start_day, r.start])

    # регистрация шрифта:
    pdfmetrics.registerFont(TTFont('ARIALUNI', 'classes/static/classes/fonts/ARIALUNI.ttf'))
    # стили по умолчанию:
    styles = getSampleStyleSheet()
    # дополняем стили абзацев
    styles.add(ParagraphStyle(
        name='Normal_CENTER',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontName='ARIALUNI',
    ))
    styles.add(ParagraphStyle(
        name='Heading1_CENTER',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontName='ARIALUNI',
    ))

    doc = SimpleDocTemplate(buf,
                            pagesize=A4,
                            title='Timetable',
                            author='Andrew')

    # словарь документа
    pdf_result = []
    # заголовок
    pdf_result.append(Paragraph(f"{user.first_name} {user.last_name}", styles["Heading1_CENTER"]))
    pdf_result.append(Paragraph(f'Расписание {classesName}', styles['Heading1_CENTER']))
    pdf_result.append(Paragraph(f'c {query.first_day} по {query.last_day}', styles['Heading1_CENTER']))
    # таблица
    t = Table(resultList)
    # стиль таблицы:
    stile = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'ARIALUNI'),
        ('FONTSIZE', (0, 0), (3, 0), 14),
        ('FONTSIZE', (0, 1), (-1, -1), 13),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LINEBELOW', (0, 0), (3, 0), 1, colors.black),
    ])
    t.setStyle(stile)
    pdf_result.append(t)

    doc.build(pdf_result)
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='result.pdf')
