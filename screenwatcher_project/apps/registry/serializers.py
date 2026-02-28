from rest_framework import serializers
from .models import Factory, Department, Line, Machine, Interface

class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interface
        fields = '__all__'

class MachineSerializer(serializers.ModelSerializer):
    interfaces = InterfaceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Machine
        fields = '__all__'

class LineSerializer(serializers.ModelSerializer):
    machines = MachineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Line
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    lines = LineSerializer(many=True, read_only=True)
    
    class Meta:
        model = Department
        fields = '__all__'

class FactorySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Factory
        fields = '__all__'