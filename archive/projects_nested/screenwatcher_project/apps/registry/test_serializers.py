import pytest
from apps.registry.models import Factory, Department, Line, Machine
from apps.registry.serializers import FactorySerializer

@pytest.mark.django_db
class TestRegistrySerializers:
    
    def test_factory_serializer_nested(self):
        # 1. Setup deep hierarchy
        factory = Factory.objects.create(name="F1", code="F1")
        dept = Department.objects.create(factory=factory, name="D1", code="D1")
        line = Line.objects.create(department=dept, name="L1", code="L1")
        Machine.objects.create(line=line, name="M1", code="M1")
        
        # 2. Serialize
        serializer = FactorySerializer(instance=factory)
        data = serializer.data
        
        # 3. Verify nesting
        assert data['code'] == "F1"
        assert len(data['departments']) == 1
        assert data['departments'][0]['code'] == "D1"
        assert len(data['departments'][0]['lines']) == 1
        assert data['departments'][0]['lines'][0]['code'] == "L1"
        assert len(data['departments'][0]['lines'][0]['machines']) == 1
        assert data['departments'][0]['lines'][0]['machines'][0]['code'] == "M1"
