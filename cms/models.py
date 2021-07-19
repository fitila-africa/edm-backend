from django.db import models

class AboutUsContent(models.Model):
    body = models.TextField()
    
    
    def __str__(self) -> str:
        return self.body[:5]
