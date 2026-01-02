

target_path = "/home/grzegorz-lesniowski/cloud/screenwatcher_project/apps/dashboards/models.py"

with open(target_path, 'r') as f:
    content = f.read()

# Insert WidgetDefinition before Widget class
insertion_point = "class Widget(BaseModel):"
new_model_code = """class WidgetDefinition(BaseModel):
    # Defines available widget types in the system, manageable via Admin.
    type_code = models.CharField(max_length=50, unique=True, help_text="Unique code, e.g., 'production_trend'")
    name = models.CharField(max_length=100, help_text="Display name")
    description = models.TextField(blank=True)
    default_config = models.JSONField(default=dict, help_text="Default configuration (JSON)")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

"""

if "class WidgetDefinition" not in content:
    new_content = content.replace(insertion_point, new_model_code + insertion_point)

    with open(target_path, 'w') as f:
        f.write(new_content)
    print("Added WidgetDefinition model.")
else:
    print("WidgetDefinition already exists.")
