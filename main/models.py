# main/models.py
from django.db import models
from django.contrib.auth.models import User

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    game_name = models.CharField(max_length=50) # 'snake' or 'tetris'
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']  # Sort highest scores first

    def __str__(self):
        return f"{self.user.username} - {self.game_name}: {self.score}"