from drf_yasg.utils import (
    swagger_auto_schema,
)

from drf_yasg.openapi import (
    Parameter,
    IN_QUERY,
    TYPE_OBJECT,
    TYPE_STRING,
    TYPE_NUMBER,
    TYPE_INTEGER,
    TYPE_BOOLEAN,
    TYPE_ARRAY,
    TYPE_FILE,
    FORMAT_DATE,
    FORMAT_DATETIME,
    FORMAT_PASSWORD,
    FORMAT_BINARY,
    FORMAT_BASE64,
    FORMAT_FLOAT,
    FORMAT_DOUBLE,
    FORMAT_INT32,
    FORMAT_INT64,

    # defined in JSON-schema
    FORMAT_EMAIL,
    FORMAT_IPV4,
    FORMAT_IPV6,
    FORMAT_URI,

    # pulled out of my ass
    FORMAT_UUID,
    FORMAT_SLUG,
    FORMAT_DECIMAL,

    IN_BODY,
    IN_PATH,
    IN_QUERY,
    IN_FORM,
    IN_HEADER,
)
