"""Publications model."""

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from usados.utils import BaseModel


class Category(BaseModel):
    """Category model."""

    name = models.CharField(
        _('name'), max_length=255
    )
    is_active = models.BooleanField(
        _('is active'), default=True,
    )

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        """Return category name."""
        return f"Category: {self.name}"


class Publication(BaseModel):
    """Publications model."""
    TYPE_OF_PUBLICATION = (
        (1, 'new'),
        (2, 'old'),
    )
    profile = models.ForeignKey(
        'users.Profile', on_delete=models.CASCADE,
        related_name='publications',
    )
    title = models.CharField(
        _('title'),
        max_length=255
    )

    description = models.TextField(_('description'),)
    type_of_publication = models.IntegerField(
        choices=TYPE_OF_PUBLICATION, default=1, db_index=True
    )
    price = models.DecimalField(
        _('price'),
        default=0, max_digits=16, decimal_places=2
    )

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )

    is_active = models.BooleanField(
        _('is active'), default=True,
    )

    is_premium = models.BooleanField(
        _('is premium'), default=False,
    )
    created = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    modified = models.DateTimeField(
        _('modified at'),
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta:
        verbose_name = 'publication'
        verbose_name_plural = 'publications'

    def __str__(self):
        """Return publication title."""
        return f"# {self.id} - {self.title}"

    def get_pictures(self):
        """Get all images of the publication"""
        return self.pictures.all()

    def change_status(self):
        """Change publication status"""
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()


class PublicationPicture(BaseModel):
    """PublicationPicture model."""
    publication = models.ForeignKey(
        Publication,
        related_name='pictures',
        on_delete=models.CASCADE
    )
    picture = models.ImageField(
        _('publication picture'),
        upload_to='publications/pictures/',
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )
    modified = models.DateTimeField(
        _('modified at'),
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    def __str__(self):
        """Return pictures."""
        return f"{self.id}"
