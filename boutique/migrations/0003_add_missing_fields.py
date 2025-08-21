from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('boutique', '0002_fix_database_schema'),
    ]

    operations = [
        # Ajouter date_creation à Gateau si elle n'existe pas
        migrations.RunSQL(
            "ALTER TABLE boutique_gateau ADD COLUMN date_creation DATETIME DEFAULT CURRENT_TIMESTAMP;",
            "ALTER TABLE boutique_gateau DROP COLUMN date_creation;"
        ),
        
        # Ajouter contenu à ArticleEvenement si elle n'existe pas
        migrations.RunSQL(
            "ALTER TABLE boutique_articleevenement ADD COLUMN contenu TEXT;",
            "ALTER TABLE boutique_articleevenement DROP COLUMN contenu;"
        ),
        
        # Ajouter date_evenement à ArticleEvenement si elle n'existe pas
        migrations.RunSQL(
            "ALTER TABLE boutique_articleevenement ADD COLUMN date_evenement DATETIME;",
            "ALTER TABLE boutique_articleevenement DROP COLUMN date_evenement;"
        ),
        
        # Ajouter actif à ArticleEvenement si elle n'existe pas
        migrations.RunSQL(
            "ALTER TABLE boutique_articleevenement ADD COLUMN actif BOOLEAN DEFAULT 1;",
            "ALTER TABLE boutique_articleevenement DROP COLUMN actif;"
        ),
    ]
