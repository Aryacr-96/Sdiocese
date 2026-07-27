# context_processors.py
from .models import Spiritual

def spiritual_categories(request):
    """
    Add spiritual categories to all templates
    """
    return {
        'spirituals': Spiritual.objects.all().order_by('category_title')
    }