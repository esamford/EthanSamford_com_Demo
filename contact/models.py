from django.db import models


class Message(models.Model):
    read = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    message = models.TextField(max_length=3000)
    time_submitted = models.DateTimeField(auto_now=True)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def message_snip(self):
        snip_length = 30
        if len(str(self.message)) > snip_length:
            return str(self.message)[:snip_length] + "..."
        else:
            return self.message

    def __str__(self):
        return "{}, {} ({}) - {}".format(self.last_name, self.first_name, self.email, self.time_submitted)
