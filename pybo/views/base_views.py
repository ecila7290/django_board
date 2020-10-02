from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question, Answer


def index(request):
    # 입력 파라미터
    page=request.GET.get('page', '1')
    kw=request.GET.get('kw', '')
    so=request.GET.get('so','recent') # 정렬기준
    
    # 정렬
    if so == 'recommend':
        question_list=Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list=Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list=Question.objects.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw)|
            Q(content__icontains=kw)|
            Q(author__username__icontains=kw)|
            Q(answer__author__username__icontains=kw)
        ).distinct()
    
    # 페이징 처리
    paginator=Paginator(question_list, 10)
    page_obj=paginator.get_page(page)


    context={'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    

    # 입력 파라미터
    page_a=request.GET.get('page', '1')
    so=request.GET.get('so', 'recommend')

    #정렬
    if so=='recent':
        answer_list=Answer.objects.filter(question=question).order_by('-create_date')
    else:
        answer_list=Answer.objects.filter(question=question).annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')


    #조회#########
    

    #페이징###########
    paginator_a=Paginator(answer_list, 10)
    page_obj_a=paginator_a.get_page(page_a)

    context = {'question': question, 'answer_list': page_obj_a, 'page_a': page_a, 'so': so}
    return render(request, 'pybo/question_detail.html', context)
