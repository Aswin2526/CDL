"""
MySQL backend compatible with XAMPP MariaDB 10.4 (Django 6 defaults require 10.6+).
"""

from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures as MySQLDatabaseFeatures

from config.db.schema import DatabaseSchemaEditor


class DatabaseFeatures(MySQLDatabaseFeatures):
    # MariaDB 10.4 does not support INSERT ... RETURNING (Django 6 enables this).
    can_return_columns_from_insert = False
    can_return_rows_from_bulk_insert = False


class DatabaseWrapper(MySQLDatabaseWrapper):
    features_class = DatabaseFeatures
    SchemaEditorClass = DatabaseSchemaEditor

    def check_database_version_supported(self):
        """Allow local XAMPP MariaDB 10.4 without raising NotSupportedError."""
        return
