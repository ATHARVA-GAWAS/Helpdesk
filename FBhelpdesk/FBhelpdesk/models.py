from djongo import models
from django.contrib.auth.models import User

class FacebookPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Page ID: {self.page_id}"

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fb_page = models.ForeignKey(FacebookPage, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=100)  # ID of the customer who sent the message
    last_message_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation with {self.customer_id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender_id = models.CharField(max_length=100)  # ID of the sender (customer or agent)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message in {self.conversation} from {self.sender_id}"
