# Generated by Django 2.2.5 on 2020-11-02 16:39

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupName', models.CharField(max_length=128)),
                ('language', models.CharField(max_length=128)),
                ('schedule', models.CharField(max_length=128)),
                ('maxNumberStudents', models.IntegerField()),
                ('counter', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['groupName'],
            },
        ),
        migrations.CreateModel(
            name='OtherConstraints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selectGroupStartDate', models.DateTimeField()),
                ('minGradeTheoryConv', models.FloatField()),
                ('minGradeLabConv', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='TheoryGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupName', models.CharField(max_length=128)),
                ('language', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ['groupName'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('gradeTheoryLastYear', models.FloatField(blank=True, null=True)),
                ('gradeLabLastYear', models.FloatField(blank=True, null=True)),
                ('convalidationGranted', models.BooleanField(default=False)),
                ('labGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.LabGroup')),
                ('theoryGroup', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.TheoryGroup')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validated', models.BooleanField(default=False)),
                ('student1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='student1', to='core.Student')),
                ('student2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='student2', to='core.Student')),
                ('studentBreakRequest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='studentBreakRequest', to='core.Student')),
            ],
        ),
        migrations.AddField(
            model_name='labgroup',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Teacher'),
        ),
        migrations.CreateModel(
            name='GroupConstraints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('labGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.LabGroup')),
                ('theoryGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TheoryGroup')),
            ],
            options={
                'ordering': ['labGroup'],
            },
        ),
    ]
