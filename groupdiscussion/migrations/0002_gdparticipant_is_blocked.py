from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('groupdiscussion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gdparticipant',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
