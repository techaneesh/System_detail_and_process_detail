from django.db import models

class SystemInfo(models.Model):
    hostname = models.CharField(max_length=100, unique=True)
    os = models.CharField(max_length=100)
    cpu = models.CharField(max_length=100)
    cpu_threads = models.IntegerField(null=True, blank=True)
    cpu_cores = models.IntegerField(null=True, blank=True)
    ram_total = models.FloatField()
    ram_available = models.FloatField(null=True, blank=True)
    ram_used = models.FloatField(null=True, blank=True)
    ram_free = models.FloatField(null=True, blank=True)
    storage_total = models.FloatField()
    storage_free = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname

class ProcessData(models.Model):
    hostname = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    process_name = models.CharField(max_length=255)
    pid = models.IntegerField()
    ppid = models.IntegerField()
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    api_key = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.process_name} ({self.pid})'
