from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diyprojects', '0012_alter_favorite_profile_alter_project_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='project_status',
            field=models.SmallIntegerField(choices=[(0, 'Backlog'), (1, 'To-Do'), (2, 'Done')], default=0),
        ),
    ]
