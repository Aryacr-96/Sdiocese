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

def downloads(request):
    """
    Add downloads to all templates (matching your view logic)
    """
    try:
        # Try to get from cache for performance
        cache_key = 'public_downloads_data'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data
        
        # Get all downloads
        downloads = Download.objects.all().order_by('document_type')
        
        # Create download map (same as your view)
        download_map = {
            'church_account_manual': None,
            'constitution_1934': None,
            'guidelines': None,
        }
        
        for download in downloads:
            # Map document_type to dictionary keys
            if download.document_type in download_map:
                download_map[download.document_type] = download
        
        context_data = {
            'downloads': downloads,
            'church_account_manual': download_map.get('church_account_manual'),
            'constitution_1934': download_map.get('constitution_1934'),
            'guidelines': download_map.get('guidelines'),
        }
        
        # Cache for 1 hour
        cache.set(cache_key, context_data, 3600)
        
        return context_data
        
    except Exception as e:
        logger.error(f"Error in downloads_context: {str(e)}")
        # Return empty context if there's an error
        return {
            'downloads': [],
            'church_account_manual': None,
            'constitution_1934': None,
            'guidelines': None,
        }