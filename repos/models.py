from django.db import models


class Repository(models.Model):
    name = models.CharField(max_length=200)
    html_url = models.CharField(max_length=200)
    description = models.CharField(max_length=512, null=True)
    private = models.BooleanField()
    created_at = models.CharField(max_length=200)
    watchers = models.IntegerField()
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            html_url=data['html_url'],
            description=data['description'],
            private=data['private'],
            created_at=data['created_at'],
            watchers=data['watchers'],
            username=data['username']
        )

    def as_dict(self):
        return {
            'name': self.name,
            'html_url': self.html_url,
            'description': self.description,
            'private': self.private,
            'created_at': self.created_at,
            'watchers': self.watchers,
            'username': self.username
        }
