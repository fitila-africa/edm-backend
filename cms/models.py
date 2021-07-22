from django.db import models

# class AboutUsContent(models.Model):
#     body = models.TextField()
    
    
#     def __str__(self) -> str:
#         return self.body[:5]



class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question
    
    
    def delete(self):
        self.is_active = False
        self.save()
        return 