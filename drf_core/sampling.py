from pydoc import locate
from importlib import import_module
from django.conf import settings

from drf_core.utils import pluralize


class Sampling(object):

    def __init__(self):
        # How many records will be created for each model.
        self.sampling_records = 50
        self.apps = settings.API_APPS
        self.factories = {}
        self.data = {}

        if hasattr(settings, 'SAMPLING_RECORDS'):
            self.sampling_records = settings.SAMPLING_RECORDS

        self._import_factories()

    def generate_all(self):
        # Gererate all data
        for app, factory_apps in self.factories.items():
            self.data[app] = {}

            for factory_app in factory_apps:
                items = []
                sampling = self.sampling_records
                model_name = factory_app.__name__.replace('Factory', '')

                if model_name in ['User', 'SuperUser']:
                    sampling=5

                for _ in range(0, sampling):
                    item = factory_app()
                    items.append(item)

                self.data[app][model_name] = items

    def generate_by_model(self, app_name, model_name, sampling=0):
        """
        Generate data for a single model.
        """
        factory = self._import_factory_by_model(app_name, model_name)
        items = [] # list of generated items

        # make sure we put sample data in the right place.
        if app_name not in self.data:
            self.data[app_name] = {}
        if model_name not in self.data[app_name]:
            self.data[app_name][model_name] = []

        # fallback to default sampling setting.
        if sampling == 0:
            sampling = self.sampling_records

        for _ in range(0, sampling):
            item = factory()
            items.append(item)
            self.data[app_name][model_name].append(item)

        return items

    def clean_up(self):
        # Clean all generated data.
        for app, data_models in self.data.items():
            for model_name, items in data_models.items():
                try:
                    # Load model
                    ids = []
                    model = locate(f'{app}.models.{model_name}')

                    for item in items:
                        ids.append(item.id)

                    model.objects.filter(id__in=ids).delete()
                except:
                    for item in items:
                        item.delete()

    def _import_factory_by_model(self, app_name, model_name):
        return locate(f'{app_name}.factories.{model_name}Factory')

    def _import_factories(self):
        # Import all needed factories.
        for app in self.apps:
            self.factories[app] = []
            try:
                module = import_module(f'{app}.factories')

                for factory_app in module.apps:
                    self.factories[app].append(factory_app)
            except Exception as ex:
                pass

        return self.factories
