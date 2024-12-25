from django.contrib import admin
from .models import Dataset, AlgorithmParameter, ProcessedDataset, ActionLog

admin.site.register(Dataset)
admin.site.register(AlgorithmParameter)
admin.site.register(ProcessedDataset)
admin.site.register(ActionLog)