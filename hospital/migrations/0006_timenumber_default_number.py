from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_alter_doctor_img_timenumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='timenumber',
            name='default_number',
            field=models.IntegerField(default=1, verbose_name='默认一个时间点可预约人数'),
            preserve_default=False,
        ),
    ]
