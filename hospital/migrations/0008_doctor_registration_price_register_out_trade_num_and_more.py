from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0007_alter_timenumber_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='registration_price',
            field=models.IntegerField(default=100, verbose_name='挂号价格'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='out_trade_num',
            field=models.UUIDField(default=100, verbose_name='商户订单号'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='payway',
            field=models.CharField(default='alipay', max_length=10, verbose_name='支付方式'),
        ),
        migrations.AddField(
            model_name='register',
            name='status',
            field=models.CharField(default='待支付', max_length=10, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='timenumber',
            name='default_number',
            field=models.PositiveSmallIntegerField(verbose_name='默认一个时间点可预约人数'),
        ),
        migrations.AlterField(
            model_name='timenumber',
            name='eight',
            field=models.PositiveSmallIntegerField(verbose_name='八点可预约人数'),
        ),
        migrations.AlterField(
            model_name='timenumber',
            name='eleven',
            field=models.PositiveSmallIntegerField(verbose_name='十一点可预约人数'),
        ),
        migrations.AlterField(
            model_name='timenumber',
            name='fifteen',
            field=models.PositiveSmallIntegerField(verbose_name='十五点可预约人数'),
        ),
        migrations.AlterField(
            model_name='timenumber',
            name='fourteen',
            field=models.PositiveSmallIntegerField(verbose_name='十四点可预约人数'),
        ),
        migrations.AlterField(
            model_name='timenumber',
            name='nine',
            field=models.PositiveSmallIntegerField(verbose_name='九点可预约人数'),
        ),
        migrations.AlterField(
            model_name='timenumber',
            name='seventeen',
            field=models.PositiveSmallIntegerField(verbose_name='十七点可预约人数'),
        ),
        migrations.AlterField(
            model_name='timenumber',
            name='sixteen',
            field=models.PositiveSmallIntegerField(verbose_name='十六点可预约人数'),
        ),
        migrations.AlterField(
            model_name='timenumber',
            name='ten',
            field=models.PositiveSmallIntegerField(verbose_name='十点可预约人数'),
        ),
    ]
