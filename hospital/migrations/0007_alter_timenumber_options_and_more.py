from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_timenumber_default_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timenumber',
            options={'verbose_name': '某时间点可预约人数', 'verbose_name_plural': '某时间点可预约人数列表'},
        ),
        migrations.AlterField(
            model_name='register',
            name='registration_time',
            field=models.DateTimeField(verbose_name='挂号时间'),
        ),
    ]
