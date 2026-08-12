# context_processors.py
import logging
from django.core.cache import cache
from .models import Download, Spiritual

logger = logging.getLogger(__name__)

def spiritual_categories(request):
    """
    Add spiritual categories to all templates
    """
    return {
        'spirituals': Spiritual.objects.all().order_by('category_title')
    }
from .models import Download


def downloads(request):
    return {
        'church_account_manual': Download.objects.filter(
            document_type='church_account_manual'
        ).first(),

        'guidelines': Download.objects.filter(
            document_type='guidelines'
        ).first(),

        'constitution_1934': Download.objects.filter(
            document_type='constitution_1934'
        ).first(),
    }