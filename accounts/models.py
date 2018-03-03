from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from  django.core.validators import RegexValidator
from django.core.mail import send_mail

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    tel_number_regex = RegexValidator(regex = r'^[0-9]+$', message = ("Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed."))

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), validators=[tel_number_regex], max_length=15,unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Member(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name=_('user'))
    jender = models.SmallIntegerField(_('jender'))
    birthday = models.DateField(_('birthday'))
    profession = models.CharField(_('profession'), max_length=50, blank=True)
    line_id = models.CharField(_('LINE ID'), max_length=255, blank=True, unique=True)
    twitter_id = models.CharField(_('Twitter ID'), max_length=255, blank=True, unique=True)
    instagram_id = models.CharField(_('Instagram ID'), max_length=255, blank=True, unique=True)
    facebook_id = models.CharField(_('Facebook ID'), max_length=255, blank=True, unique=True)
    whatsapp_id = models.CharField(_('WhatsApp ID'), max_length=255, blank=True, unique=True)
    kik_id = models.CharField(_('KIK ID'), max_length=255, blank=True, unique=True)
    wechat_id = models.CharField(_('WeChat ID'), max_length=255, blank=True, unique=True)
    level = models.SmallIntegerField(_('member level'), default=1)
    notice = models.BooleanField(_('notice'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    is_banned = models.BooleanField(_('banned'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')

    def __str__(self):
        return '%s' % self.user__username

class MemberAddress(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name=_('member'))
    district = models.ForeignKey('meta.District', on_delete=models.CASCADE, verbose_name=_('district'))
    postal_code = models.CharField(_('postal code'), max_length=9)
    address1 = models.CharField(_('address1'), max_length=255)
    address2 = models.CharField(_('address2'), max_length=255, blank=True)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    is_default = models.BooleanField(_('default'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('member\'s address')
        verbose_name_plural = _('member\'s addresses')

    def __str__(self):
        return '%s' % self.district__name

class Itinerary(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE, verbose_name=_('member'))
    purpose = models.SmallIntegerField(_('purpose'))
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('itinerary')
        verbose_name_plural = _('itineraries')

    def __str__(self):
        return '%s' % self.member__name

class Transfer(models.Model):
    itinerary = models.ForeignKey('Itinerary', on_delete=models.CASCADE, verbose_name=_('itinerary'))
    departure = models.OneToOneField('Departure', on_delete=models.CASCADE, verbose_name=_('departure'))
    arrival = models.OneToOneField('Arrival', on_delete=models.CASCADE, verbose_name=_('arrival'))
    ticket = models.SmallIntegerField(_('ticket'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('transfer')
        verbose_name_plural = _('transfers')

    def __str__(self):
        return '%s' % self.departure__district__name + ' -> ' + '%s' %  self.arrival__district__name

class Departure(models.Model):
    country = models.OneToOneField('meta.Country', on_delete=models.CASCADE, verbose_name=_('country'))
    district = models.OneToOneField('meta.District', on_delete=models.CASCADE, verbose_name=_('district'))
    departing_at = models.DateTimeField(_('departure time'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('departure')
        verbose_name_plural = _('departures')

    def __str__(self):
        return '%s' % self.departing_at

class Arrival(models.Model):
    country = models.OneToOneField('meta.Country', on_delete=models.CASCADE, verbose_name=_('country'))
    district = models.OneToOneField('meta.District', on_delete=models.CASCADE, verbose_name=_('district'))
    arriving_at  = models.DateTimeField(_('arrival time'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('arrival')
        verbose_name_plural = _('arrivals')

    def __str__(self):
        return '%s' % self.arriving_at
