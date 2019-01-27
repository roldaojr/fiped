from import_export import resources, fields, widgets, results
from eventos.models import Inscricao
from .models import Certificado


class CertificadoResource(resources.ModelResource):
    tipo_atividade = fields.Field(
        attribute='tipo_atividade', column_name='tipo')
    inscricao = fields.Field(
        attribute='inscricao', column_name='email',
        widget=widgets.ForeignKeyWidget(Inscricao, 'usuario__email'))

    class Meta:
        model = Certificado
        exclude = ('id', 'modelo')

    def __init__(self, modelo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modelo = modelo

    def get_instance(self, instance_loader, row):
        return False

    def before_save_instance(self, instance, *args, **kwargs):
        instance.modelo = self.modelo

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super().import_row(row, instance_loader, **kwargs)
        if import_result.import_type == results.RowResult.IMPORT_TYPE_ERROR:
            # Copy the values to display in the preview report
            import_result.diff = [row[val] for val in row]
            # Add a column with the error message
            import_result.diff.append(
                'Erros: %s' % (', '.join([
                    str(err.error) for err in import_result.errors
                ]))
            )
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = results.RowResult.IMPORT_TYPE_SKIP

        return import_result
