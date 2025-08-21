from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('boutique', '0001_initial'),
    ]

    operations = [
        # Ajouter date_creation à Gateau
        migrations.RunSQL(
            "ALTER TABLE boutique_gateau ADD COLUMN date_creation DATETIME;",
            "ALTER TABLE boutique_gateau DROP COLUMN date_creation;"
        ),
        
        # Ajouter contenu à ArticleEvenement (renommer description si nécessaire)
        migrations.RunSQL(
            """
            ALTER TABLE boutique_articleevenement ADD COLUMN contenu TEXT;
            UPDATE boutique_articleevenement SET contenu = description WHERE description IS NOT NULL;
            """,
            "ALTER TABLE boutique_articleevenement DROP COLUMN contenu;"
        ),
        
        # Ajouter date_evenement à ArticleEvenement
        migrations.RunSQL(
            "ALTER TABLE boutique_articleevenement ADD COLUMN date_evenement DATETIME;",
            "ALTER TABLE boutique_articleevenement DROP COLUMN date_evenement;"
        ),
        
        # Ajouter actif à ArticleEvenement
        migrations.RunSQL(
            "ALTER TABLE boutique_articleevenement ADD COLUMN actif BOOLEAN DEFAULT 1;",
            "ALTER TABLE boutique_articleevenement DROP COLUMN actif;"
        ),
    ]
