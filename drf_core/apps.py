"""
Import
"""
from django.apps import AppConfig


class BaseConfig(AppConfig):
    """
    The base configuration. All django app should extends from this config.
    """
    def ready(self):
        # Reads the following article to understand why the following print
        # command might run twice.
        # http://stackoverflow.com/questions/33814615/how-to-avoid-appconfig-ready-method-running-twice-in-django
        #
        # Runs ` python manage.py runserver --noreload` command solves
        # the issue.
        print('Loads %s app' % self.name)


class CoreConfig(BaseConfig):
    """ The core application provides common functionalities
        used by other applications in this project.
    """
    name = 'drf_core'

    def ready(self):
        super().ready()

        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('signals')
