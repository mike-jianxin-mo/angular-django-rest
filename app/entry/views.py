from django.views.generic.base import TemplateView

class Entry(TemplateView):
	template_name = 'entry/index.html'

