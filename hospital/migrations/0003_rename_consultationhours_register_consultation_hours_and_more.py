from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_rename_department_id_doctor_department_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='consultationhours',
            new_name='consultation_hours',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='registrationtime',
            new_name='registration_time',
        ),
        migrations.AddField(
            model_name='department',
            name='address',
            field=models.CharField(default=False, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='address',
            field=models.CharField(default=False, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='isdelete',
            field=models.BooleanField(default=False),
        ),
    ]
