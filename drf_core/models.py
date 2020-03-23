from django.db.models import ( # noqa
    Model as BaseModel,
    SET_NULL
)
from django.conf import settings
from django.db.models.query import QuerySet as BaseQuerySet

from django_extensions.db.models import (
    TimeStampedModel as BaseTimeStampedModel
)
from rest_framework.authtoken.models import Token

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

    def _archive_on_delete(self):
        """ Get all model instance related to manytomany field update
        archive=True when parent modele is removed
        """
        # Get model name
        model_name = self._meta.model_name.capitalize()

        # Get pk value of instance
        field_object_pk = self._meta.get_field('id')
        field_value_pk = field_object_pk.value_from_object(self)

        for field in self._meta.many_to_many:
            # Get through model from 'manytomany' field
            through_model = field.remote_field.through
            filter_field = None

            # Try to loop all fields of through_model.
            # If have any field has foreign key related to model instance,
            # get that field for filtering
            for through_model_field in field.remote_field.through._meta.get_fields():
                try:
                    if through_model_field.remote_field.model.__name__ == model_name:
                        filter_field = through_model_field.name
                except:
                    continue

            # Filter and update related model via 'through_model' and 'filter_field'
            if filter_field:
                for related_queryset in through_model.objects.filter(**{filter_field: field_value_pk}):
                    related_queryset.archived = True
                    related_queryset.save()

    def archive(self):
        """
        Archives the model.
        """
        self.archived = True
        self.save()
        self._archive_on_delete()

    def unarchive(self):
        """
        Unarchives the model.
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


# ==============================================================================
# ContributorModel
# ==============================================================================

class ContributorModel(TimeStampedModel):
    """
    This model contains the contributor information about who is owner, who is
    editor.
    """
    created_by = fields.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Created by',
        blank=True,
        null=True,
        on_delete=SET_NULL,
        related_name='%(class)s_created_by',
    )

    last_modified_by = fields.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Last modified by',
        blank=True,
        null=True,
        on_delete=SET_NULL,
        related_name='%(class)s_modified_by',
    )

    class Meta:
        abstract = True
