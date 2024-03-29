from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_rename_consultationhours_register_consultation_hours_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': '科室', 'verbose_name_plural': '科室列表'},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'verbose_name': '医生', 'verbose_name_plural': '医生列表'},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name': '患者', 'verbose_name_plural': '患者列表'},
        ),
        migrations.AlterModelOptions(
            name='register',
            options={'verbose_name': '挂号单', 'verbose_name_plural': '挂号单列表'},
        ),
        migrations.AddField(
            model_name='department',
            name='parentid',
            field=models.IntegerField(default=0, verbose_name='上级科室id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='doctor',
            name='description',
            field=models.CharField(default='what', max_length=50, verbose_name='详细描述'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='doctor',
            name='img',
            field=models.ImageField(default='doctorimages/linjunjun.png', upload_to='doctorimages/', verbose_name='商品图片'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='doctor',
            name='level',
            field=models.CharField(default='院长', max_length=10, verbose_name='职位等级'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='department',
            name='address',
            field=models.CharField(max_length=30, verbose_name='科室地址'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=10, verbose_name='科室名字'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='age',
            field=models.CharField(max_length=3, verbose_name='医生年龄'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='name',
            field=models.CharField(max_length=10, verbose_name='医生姓名'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='password',
            field=models.CharField(max_length=30, verbose_name='医生密码'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='医生电话'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='sex',
            field=models.CharField(max_length=1, verbose_name='医生性别'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.CharField(max_length=3, verbose_name='患者年龄'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(max_length=10, verbose_name='患者姓名'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='password',
            field=models.CharField(max_length=30, verbose_name='患者密码'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='患者电话'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='sex',
            field=models.CharField(max_length=1, verbose_name='患者性别'),
        ),
        migrations.AlterField(
            model_name='register',
            name='address',
            field=models.CharField(max_length=30, verbose_name='会诊地址'),
        ),
        migrations.AlterField(
            model_name='register',
            name='consultation_hours',
            field=models.DateTimeField(verbose_name='会诊时间'),
        ),
        migrations.AlterField(
            model_name='register',
            name='doctor_name',
            field=models.CharField(max_length=10, verbose_name='医生姓名'),
        ),
        migrations.AlterField(
            model_name='register',
            name='illness',
            field=models.CharField(max_length=50, verbose_name='病情概要'),
        ),
        migrations.AlterField(
            model_name='register',
            name='isdelete',
            field=models.BooleanField(default=False, verbose_name='挂号是否已经删除'),
        ),
        migrations.AlterField(
            model_name='register',
            name='patient_name',
            field=models.CharField(max_length=10, verbose_name='患者姓名'),
        ),
        migrations.AlterField(
            model_name='register',
            name='registration_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='挂号时间'),
        ),
    ]
