from django.db import models


class Message(models.Model):
    user_id = models.CharField(max_length=20)
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    content = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ])

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"
