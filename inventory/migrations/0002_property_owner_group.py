from django.db import migrations


def create_property_owner_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    # Create Property Owners group
    property_owner_group, created = Group.objects.get_or_create(name="Property Owners")

    # Assign specific permissions
    permissions = Permission.objects.filter(
        codename__in=["add_accommodation", "change_accommodation", "view_accommodation"]
    )
    property_owner_group.permissions.set(permissions)


def delete_property_owner_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name="Property Owners").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_property_owner_group, delete_property_owner_group),
    ]
