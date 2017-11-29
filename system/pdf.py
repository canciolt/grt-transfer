from django.views.generic.base import View
from wkhtmltopdf.views import PDFTemplateResponse


class MyPDFView(View):
    template = 'prefactura_form.html'
    context = {'title': 'Hello World!'}

    def get(self, request):
        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename="hello.pdf",
                                       context=self.context,
                                       show_content_in_browser=False,
                                       cmd_options={'margin-top': 50, },
                                       )
        return response
