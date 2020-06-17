import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    """Metodo che inserisce un file nella cartella relativa all'utente, il file sarà inserito nella cartella MEDIA_ROOT/user_<id>/<filename>
        :return user_<id>/<filename>"""
    return 'user_{0}/{1}'.format(instance.user.id, filename)


def static_avatar_path():
    """Metodo che restituisce il percorso dell'immagine di default"""
    # return os.path.join(STATICFILES_DIRS[0], 'img', 'baseAvatar.png')
    return os.path.join('/static', 'img', 'baseAvatar.png')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(blank=True, default=static_avatar_path(), upload_to=user_directory_path)
    email = models.EmailField(blank=False, unique=True, default='user_{0}@default.com'.format(User.pk))

    def get_user(self):
        return User.objects.filter(pk = self.user.pk).last()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Metodo utilizzato per creare un Profle ogni volta che si crea un User sfruttando il model di django"""
    if created:
        Profile.objects.create(user=instance, email=instance.email)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Metodo utilizzato per salvare un Profile ogni volta che si salva un User creato con il model di django"""
    instance.profile.save()


@property
def avatar_url(self):
    if self.avatar and hasattr(self.avatar, 'url'):
        return self.avatar.url
