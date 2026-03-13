from django.db import models
from apps.core.models import BaseModel

class Factory(BaseModel):
    name = models.CharField(max_length=100)
    code = models.SlugField(max_length=50, unique=True, help_text="Unique identifier for the factory (e.g., 'FACTORY-01')")
    address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Factories"
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Department(BaseModel):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    code = models.SlugField(max_length=50, help_text="Department code (e.g., 'DEPT-ASSEMBLY')")
    
    class Meta:
        unique_together = ('factory', 'code')
        ordering = ['code']

    def __str__(self):
        return f"{self.name} - {self.factory.code}"

class Line(BaseModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='lines')
    name = models.CharField(max_length=100)
    code = models.SlugField(max_length=50, help_text="Line code (e.g., 'LINE-01')")
    
    class Meta:
        unique_together = ('department', 'code')
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Machine(BaseModel):
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='machines')
    name = models.CharField(max_length=100)
    code = models.SlugField(max_length=50, unique=True, help_text="Unique Machine ID (e.g., 'M-001')")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    # Integration
    legacy_connection = models.ForeignKey(
        'legacy_integration.ConnectionProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='machines'
    )
    
    # Configuration
    cycle_time_ideal = models.FloatField(default=0.0, help_text="Ideal cycle time in seconds")
    
    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.name} [{self.code}]"

class Interface(BaseModel):
    PROTOCOL_CHOICES = [
        ('mqtt', 'MQTT'),
        ('opcua', 'OPC UA'),
        ('rest', 'REST API'),
        ('modbus', 'Modbus TCP'),
    ]
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='interfaces')
    name = models.CharField(max_length=100, help_text="Interface name (e.g., 'Main PLC')")
    protocol = models.CharField(max_length=20, choices=PROTOCOL_CHOICES, default='mqtt')
    
    # Configuration (JSON for flexibility)
    connection_details = models.JSONField(default=dict, help_text="Protocol specific settings (IP, Port, Topic)")
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.machine.code} - {self.name} ({self.protocol})"

class Shift(BaseModel):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name='shifts')
    name = models.CharField(max_length=50) # e.g. "Morning", "Afternoon"
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        ordering = ['start_time']
        
    def __str__(self):
        return f"{self.name} ({self.start_time}-{self.end_time})"