# Generated by Django 5.1.3 on 2025-02-11 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_rename_parket_price_product_bulk_pirce'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='description_de',
            field=models.TextField(default='Willkommen bei One-Stop Afroshop, einem afrikanischen Geschäft in Deutschland, \n        das sich darauf spezialisiert hat, die lebendigen und vielfältigen Aromen Afrikas direkt zu Ihnen nach Hause zu bringen. \n        Wir bieten eine breite Palette authentischer afrikanischer Produkte an, von traditionellen Lebensmitteln bis hin zu \n        Schönheits- und Hautpflegeprodukten, die die reiche Kultur und das Erbe des afrikanischen Kontinents feiern.\n\n        Unsere Mission ist es, die afrikanische Diaspora in Deutschland mit den Produkten zu verbinden, \n        die sie lieben und von zu Hause vermissen. Ob Sie sich nach einem Stück Heimat sehnen \n        mit unserer vielfältigen Auswahl an afrikanischen Lebensmitteln oder nach hochwertigen Kosmetika \n        suchen, die mit natürlichen afrikanischen Inhaltsstoffen hergestellt wurden – wir haben für jeden etwas dabei.\n\n        Wir sind leidenschaftlich darum bemüht, das Wesen der afrikanischen Kultur durch unsere Produkte zu teilen, \n        und bieten Ihnen ein One-Stop-Shop für alles, was mit Afrika zu tun hat. Wir legen großen Wert auf Qualität, Authentizität \n        und ein tiefes Engagement für die Zufriedenheit unserer Kunden. Während wir weiter wachsen, \n        wollen wir unser Produktsortiment erweitern und noch mehr Möglichkeiten bieten, das Beste aus Afrika hier in Deutschland zu erleben.\n        '),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
