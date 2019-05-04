from django.shortcuts import render, HttpResponse, Http404

# 재고 부분
def Hello(request):
    return render(request, 'Main/Stock/main.html')
