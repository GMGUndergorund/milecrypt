from datetime import datetime
import json
import threading

class LinksetStorage:
    """In-memory storage for linksets"""
    
    def __init__(self):
        self.linksets = {}
        self.next_id = 1
        self.lock = threading.Lock()
    
    def create_linkset(self, folder_name, slug, links, password=None, expires_at=None):
        """Create a new linkset"""
        with self.lock:
            linkset = {
                'id': self.next_id,
                'folder_name': folder_name,
                'slug': slug,
                'links': links,
                'password': password,
                'created_at': datetime.now().isoformat(),
                'expires_at': expires_at.isoformat() if expires_at else None,
                'views': 0
            }
            
            self.linksets[slug] = linkset
            self.next_id += 1
            return linkset['id']
    
    def get_linkset_by_slug(self, slug):
        """Get linkset by slug"""
        return self.linksets.get(slug)
    
    def get_unique_slug(self, base_slug):
        """Generate a unique slug"""
        slug = base_slug
        counter = 1
        
        while slug in self.linksets:
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
    
    def increment_views(self, slug):
        """Increment view count for a linkset"""
        with self.lock:
            if slug in self.linksets:
                self.linksets[slug]['views'] += 1
    
    def get_recent_linksets(self, limit=10):
        """Get recent linksets for homepage"""
        linksets = list(self.linksets.values())
        # Sort by creation date (newest first)
        linksets.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Filter out expired and password-protected linksets for public display
        public_linksets = []
        for linkset in linksets[:limit]:
            if linkset.get('password'):
                continue
            if linkset['expires_at'] and datetime.fromisoformat(linkset['expires_at']) < datetime.now():
                continue
            # Only show safe info for homepage
            public_linksets.append({
                'folder_name': linkset['folder_name'],
                'slug': linkset['slug'],
                'created_at': linkset['created_at'],
                'views': linkset['views'],
                'link_count': len(linkset['links'])
            })
        
        return public_linksets
