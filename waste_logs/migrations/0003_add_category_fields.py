from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('waste_logs', '0002_add_default_categories'),
    ]

    operations = [
        # Add fields to WasteCategory
        migrations.AddField(
            model_name='wastecategory',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wastecategory',
            name='icon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='wastecategory',
            name='color',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='wastecategory',
            name='is_recyclable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='wastecategory',
            name='is_compostable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='wastecategory',
            name='is_hazardous',
            field=models.BooleanField(default=False),
        ),
        
        # Add verbose_name_plural to WasteCategory
        migrations.AlterModelOptions(
            name='wastecategory',
            options={'verbose_name_plural': 'Waste Categories'},
        ),
    ]
