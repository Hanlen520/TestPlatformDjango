from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CalcUtils:

    @classmethod
    def page_data(cls, data_list, page, size):
        print('zhssssss', len(data_list))
        if 0 == len(data_list):
            return {
                "list": [],
                "total": 0,
                "page": page,
                "size": size
            }
        paginator = Paginator(data_list, size)  # Show size contacts per page
        try:
            p = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            p = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            p = paginator.page(paginator.num_pages)

        print("zheshi:", p.object_list)
        return {
            "list": p.object_list,
            "data": "",
            "total": len(data_list),
            "page": page,
            "size": size
        }