# import io

# from reportlab.lib.pagesizes import A4
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfgen import canvas


# def get_pdf_file(queryset):
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#     p.setLineWidth(.3)
#     pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
#     p.setFont('FreeSans', 14)
#     t = p.beginText(30, 750, direction=0)
#     t.textLine('Shopping list')
#     p.line(30, 747, 580, 747)
#     t.textLine(' ')
#     for qs in queryset:
#         title = qs['recipe_id__ingredients__name']
#         amount = qs['recipe_id__ingredients_amount__amount__sum']
#         measurements_unit = qs['recipe_id__ingredients__measurements_unit']
#         t.textLine(f'{title} ({measurements_unit}) - {amount}')
#     p.drawText(t)
#     p.showPage()
#     p.save()
#     buffer.seek(0)
#     return buffer
from collections import defaultdict

from django.http import HttpResponse


def form_shop_list(queryset):
    to_buy_list = defaultdict(int)
    for note in queryset:
        to_buy_list[(note.ingredient.name,
                    note.ingredient.measurement_unit)] += note.amount
    final_string = ''
    for ingredient, amount in to_buy_list.items():
        final_string += f'{ingredient[0]} - {amount}({ingredient[1]})\n'
    return final_string


def add_file_to_response(data, content_type):
    response = HttpResponse(data, content_type=content_type)
    response['Content-Disposition'] = ('attachment;'
                                       ' filename="shop_list.txt"')
    return response
