# ==============================================================================
# ChoiceEnum
# ==============================================================================


class ChoiceEnum:
    """ The base class for choices enumeration. This enumeration is often
    uses with Django fields. """

    CHOICES = []

    # The cached value for the name_value_json method
    # This cache is computed only once, assumes that the CHOICES field
    # never change.
    _id_value_json_cached = None

    _values_cached = None

    @classmethod
    def values(cls):
        if cls._values_cached:
            return cls._values_cached

        cls._values_cached = [
            x[0]
            for x in cls.CHOICES
        ]
        return cls._values_cached

    @classmethod
    def name_value_json(cls):
        if cls._id_value_json_cached:
            return cls._id_value_json_cached

        choices = cls.CHOICES
        # Builds up the catched json
        assert choices, 'this instance must have a CHOICES field'
        cls._id_value_json_cached = [
            {
                'value': data[0] or '',
                'name': data[1] or '',
            }

            for data in choices
        ]

        return cls._id_value_json_cached
