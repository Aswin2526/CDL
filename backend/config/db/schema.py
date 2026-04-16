from django.db.backends.mysql.schema import DatabaseSchemaEditor as MySQLSchemaEditor


class DatabaseSchemaEditor(MySQLSchemaEditor):
    """Use CHANGE COLUMN for renames on XAMPP MariaDB 10.4."""

    def _rename_field_sql(self, table, old_field, new_field, new_type):
        new_type = self._set_field_new_type(old_field, new_type)
        return (
            "ALTER TABLE %(table)s CHANGE %(old_column)s %(new_column)s %(type)s"
            % {
                "table": self.quote_name(table),
                "old_column": self.quote_name(old_field.column),
                "new_column": self.quote_name(new_field.column),
                "type": new_type,
            }
        )
