from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ArticleInfo, NewsInfo, RawArticleInfo, PagerInfo, CategoryInfo, IncidentInfo, RawArticleImageInfo
from .serializers import ArticleSerializer, NewsInfoSerializer, RawArticleInfoSerializer, PagerInfoSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework import status
import json 
import datetime
import pytz

#언론사 뉴스조회
@csrf_exempt
@api_view(['GET'])
def get_news_list(request, provider):
    if request.method == 'GET':
        try:
            query_set = NewsInfo.objects.filter(provider=provider)
            if not query_set:
                raise NewsInfo.DoesNotExist("조회할 데이터가 없습니다.")
            serializer = NewsInfoSerializer(query_set, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        
        except NewsInfo.DoesNotExist as e:
                content = {"status_code":status.HTTP_404_NOT_FOUND,
                           "provider_id":provider,
                           "message":str(e)}        
                return Response(content, status=404)



# 지면 조회
@csrf_exempt
@api_view(['GET'])
def get_pager_list(request, news):
        if request.method == 'GET':
            try:
                query_set = PagerInfo.objects.filter(news=news)
                if not query_set:
                    raise PagerInfo.DoesNotExist("조회할 데이터가 없습니다.")
                serializer = PagerInfoSerializer(query_set, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

            except PagerInfo.DoesNotExist as e:
                content = {"status_code":status.HTTP_404_NOT_FOUND,
                           "news_id":news,
                           "message":str(e)}  
                return Response(content, status=404)


# 지면기사조회
@csrf_exempt
@api_view(['GET'])
def article_search(request):
    if request.method == 'GET':
        raw_startDate = request.GET.get('startDate')
        raw_endDate = request.GET.get('endDate')
        date_format = "%Y%m%d"
        raw_startdate = datetime.datetime.strptime(raw_startDate, date_format)
        raw_end_Date = datetime.datetime.strptime(raw_endDate, date_format)
        raw_enddate = raw_end_Date + datetime.timedelta(hours=23,minutes=59,seconds=59)
        search = request.GET.get('search', '')
        check_box = request.GET.get('chk')
        q=Q()

       #발행일
        if raw_startDate:
            q &= Q(raw_article__published_at__range=[raw_startdate, raw_enddate])

        if check_box:
            check = check_box.split(sep=',')
            for i in check:
                box_list = i
                # 제목
                if box_list == '1':
                    q &= Q(raw_article__title__icontains=search)
                #본문
                elif box_list == '2':
                    q &= Q(raw_article__content__icontains=search)
                #언론사
                elif box_list == '3':
                    q &= Q(raw_article__provider__icontains = search)
                #기자명
                elif box_list=='4':
                    q &= Q(raw_article__byline__icontains = search)
        queryset = ArticleInfo.objects.select_related('raw_article').filter(q)
        serializer = ArticleSerializer(queryset, many=True)
        return JsonResponse({"search":search, "searchData":serializer.data}, safe=False, status=status.HTTP_200_OK)


# 뉴스,기사,페이지 추가
@csrf_exempt
@api_view(['POST'])
def article_create(request):
    if request.method == 'POST':
        code = request.POST.get('code')

        date_code = code.split(sep="-")
        dates_codes = "".join(date_code)

        codes = dates_codes.split(sep='_')

        newscodes =  codes[:2]
        newscode = '_'.join(newscodes)

        pagecodes = codes[:3]
        pagecode = '_'.join(pagecodes)

        articlecodes = codes[:4]
        articlecode = '_'.join(articlecodes)

        newsinfos = NewsInfo.objects.filter(code=newscode)
        pageinfos = PagerInfo.objects.filter(code=pagecode)
        articleinfos = ArticleInfo.objects.filter(code=articlecode)
    try:
        #뉴스 추가
        if len(newsinfos) == 0:
            newsinfo = NewsInfo.objects.create(
                published_date_time = request.POST.get('published_date_time'),
                code = newscode,
                provider_id = request.POST.get('provider')
            )
            newsinfo.save()
        else:
            newsinfo = newsinfos[0]

        #지면 추가
        if len(pageinfos) == 0:
            pageinfo = PagerInfo.objects.create(
                news_id = newsinfo.no,
                page = request.POST.get('page'),
                pager_image = request.POST.get('pager_image'),
                code = pagecode,
                order = request.POST.get('order')
            )
            pageinfo.save()
        else:
            pageinfo = pageinfos[0]

        # 기사 추가
        if len(articleinfos) == 0:
            articleinfo = ArticleInfo.objects.create(
                raw_article_id = request.POST.get('raw_article'),
                paper_id = pageinfo.no,
                paper_image = request.POST.get('paper_image'),
                code = articlecode,
            )
            articleinfo.save()
        else:
            articleinfo = articleinfos[0]

        return Response({"status_code":status.HTTP_200_OK, "detail":"success"}, status=status.HTTP_200_OK) 
    except KeyError as e:
        content = {"status_code":status.HTTP_400_BAD_REQUEST,
                   "ker_error":str(e)}  
        return JsonResponse(content, status=400)
#기사 목록조회
@csrf_exempt
@api_view(['GET'])
def get_article_list(request, paper):
    if request.method == 'GET':
        try:    
            query_set = ArticleInfo.objects.filter(paper=paper)
            if not query_set:
                raise ArticleInfo.DoesNotExist("조회할 데이터가 없습니다.")
            serializer = ArticleSerializer(query_set, many=True)           
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except ArticleInfo.DoesNotExist as e:
                content = {"status_code":status.HTTP_404_NOT_FOUND,
                           "paper_id":paper,
                           "message":str(e)}            
                return Response(content, status=404)



#기사 정보조회
@csrf_exempt
@api_view(['GET'])
def article_info(request, no):
    if request.method == 'GET':
        try:
            query_set = ArticleInfo.objects.get(no=no)  
            serializer = ArticleSerializer(query_set)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ArticleInfo.DoesNotExist:
            content = {"status_code":status.HTTP_404_NOT_FOUND,
                       "article_id":no,
                       "message":"조회할 수 없습니다"}
            return Response(content, status=404) 




# 원본기사API 요청
@csrf_exempt
@api_view(['GET', 'POST'])
def raw_article_info(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        content = request.GET.get('content')
        provider = request.GET.get('provider')
        startDate = request.GET.get('startDate')
        endDate = request.GET.get('endDate')
        date_format = "%Y%m%d"
        startdate = datetime.datetime.strptime(startDate, date_format)
        end_Date = datetime.datetime.strptime(endDate, date_format)
        enddate = end_Date + datetime.timedelta(hours=23,minutes=59,seconds=59)
        q=Q()
        
        #제목
        if title:
            q &= Q(title__contains = title)                      
        #본문
        if content:
            q &= Q(content__contains = content)                      
        #언론사
        if provider:
            q &= Q(provider__contains = provider)
        #발행일
        if startDate:       
            q &= Q(published_at__range=[startdate, enddate])          

        query_set = RawArticleInfo.objects.filter(q)
        serializer = RawArticleInfoSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    # 원본 기사 저장부분
    elif request.method == 'POST':
        object = request.data
        serializer = RawArticleInfoSerializer(data=object)
        if serializer.is_valid(): # 생성한 모델과 일치하면
            serializer.save()# 데이터 저장
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 원본기사API 요청
@csrf_exempt
@api_view(['POST'])
def raw_article_create(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            save_count = 0
            for i in data:
                news_code = i['news_id'] 
                rawinfo = RawArticleInfo.objects.filter(code=news_code)
                if len(rawinfo) == 0:
                    raw_article_info = RawArticleInfo.objects.create(
                        code = i['news_id'],
                        title = i['title'],
                        content = i['content'],
                        provider = i['provider'],
                        # category = i['category'],
                        category = "",                          
                        byline = i['byline'],
                        provider_news_id = i['provider_news_id'],
                        publisher_code = i['publisher_code'],
                        provider_link_page = i['provider_link_page'],
                        printing_page = i['printing_page'],
                        published_at = i['published_at'],
                        enveloped_at = i['enveloped_at'],
                        dateline = i['dateline']
                    )
                    save_count+=1

                    img_addr = i['images']
                    
                    if len(img_addr) > 0:
                        if img_addr == list(img_addr):
                            imgs = list(filter(None, img_addr))
                            for img in imgs:
                                img_adrs = img.replace("\n", "").replace(" ", "")
                                RawArticleImageInfo.objects.create(
                                    raw_article_id = raw_article_info.no,
                                    address = img_adrs
                                )
                        else:
                            img_adr = img_addr.strip("\n").replace("\n", ",").replace(" ", "")
                            img_adrss = img_adr.split(sep=",")

                            for img_addrs in img_adrss:
                                RawArticleImageInfo.objects.create(
                                    raw_article_id = raw_article_info.no,
                                    address = img_addrs
                                )
                    categorys = i['category']
                    category_incidents= i['category_incident']
                    for cate in categorys:
                        category_data = cate
                        category_info = CategoryInfo.objects.filter(name=category_data)

                        if len(category_info) == 0:
                            category = CategoryInfo.objects.create(
                                name = category_data
                            )
                            raw_article_info.categoryinfo_set.add(category)
                        raw_article_info.categoryinfo_set.add(*category_info)

                    for inc in category_incidents:
                        incident_data = inc
                        incident_info = IncidentInfo.objects.filter(name=incident_data)
                        if len(incident_info) == 0:
                            incident =IncidentInfo.objects.create(
                                    name = incident_data
                                )
                            raw_article_info.incidentinfo_set.add(incident)
                        raw_article_info.incidentinfo_set.add(*incident_info)
        return Response({"status_code":status.HTTP_200_OK, "save":save_count, "message":"success"}, status=status.HTTP_200_OK) 
            
    except KeyError as e:
        content = {"status_code":status.HTTP_400_BAD_REQUEST,
                "save":save_count,
                "ker_error":str(e)}
        return JsonResponse(content, status=400)