from django.core.paginator import Paginator, EmptyPage


def paginate(objects, request, per_page=15):
    paginator = Paginator(objects, per_page)
    try:
        page = int(request.GET.get('page', 1))
        return paginator.page(page)
    except EmptyPage:
        pass
    except ValueError:
        pass
    return paginator.page(1)