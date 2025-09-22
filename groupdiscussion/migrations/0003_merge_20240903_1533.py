from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration merges two branches:
    - 0002_alter_gdparticipant_unique_together
    - 0002_gdparticipant_is_blocked
    """

    dependencies = [
        ('groupdiscussion', '0002_alter_gdparticipant_unique_together'),
        ('groupdiscussion', '0002_gdparticipant_is_blocked'),
    ]

    operations = [
    ]
