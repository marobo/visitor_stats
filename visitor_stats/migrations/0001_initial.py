import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('page', models.CharField(max_length=500)),
                ('user_agent', models.TextField(blank=True)),
                ('visited_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('browser', models.CharField(blank=True, max_length=100)),
                ('operating_system', models.CharField(blank=True, max_length=100)),
                ('device_type', models.CharField(blank=True, max_length=20)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-visited_at'],
            },
        ),
    ]
