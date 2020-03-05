from django.db.models import ( # noqa
    Model as BaseModel,
    Manager as BaseManager,
    signals,
    Aggregate,
    CharField,
    PositiveSmallIntegerField,
)

from rest_framework.authtoken.models import Token

from django.db.models.query import QuerySet as BaseQuerySet


from django_extensions.db.models import (
    TimeStampedModel as BaseTimeStampedModel
)

from drf_core import fields


# ==============================================================================
# ArchivableModelMixin
# ==============================================================================
class QuerySet(BaseQuerySet):
    def archived_only(self):
        return self.filter(archived=True)

    def non_archived_only(self):
        return self.filter(archived=False)


class ArchivableModelMixin(BaseModel):
    """
    ArchivableModelMixin

    Mixin class that provides an `archived` field. This field is used
    to archive objects instead of deleting them from the database.
    """
    objects = QuerySet.as_manager()

    archived = fields.BooleanField(
        default=False,
        db_index=True,
    )

    class Meta:
        abstract = True

    def archive(self):
        """ Archives the model.
        """
        self.archived = True
        self.save()

    def unarchive(self):
        """ Unarchives the model.
        """
        self.archived = False
        self.save()


# ==============================================================================
# TimeStampedModel
# ==============================================================================
class TimeStampedModel(BaseTimeStampedModel, ArchivableModelMixin):
    class Meta:
        abstract = True


def create_api_key(sender, instance, created, **kwargs):
    if kwargs.get('raw', False) is False and created is True:
        Token.objects.create(user=instance)


# ==============================================================================
# Model
# ==============================================================================
class Model(ArchivableModelMixin, BaseModel):
    objects = QuerySet.as_manager()

    class Meta:
        abstract = True
