from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'mainpage/homepage_index.html'


index = Index.as_view()
