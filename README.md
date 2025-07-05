# Private Flask Gallery

Eine minimale Galerie-Anwendung in Flask. Bilder liegen in thematischen Ordnern unter `gallery_app/galleries`. Jeder Ordner enthält eine `folder_meta.yaml` mit Titel, Datum und Tags. Die App liest IPTC-Daten der Bilder aus und ermöglicht deren Bearbeitung im Backoffice.

## Starten

1. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
2. Anwendung starten:
   ```bash
   python run.py
   ```

Die Galerie ist dann unter `http://localhost:5000` erreichbar, das Backoffice unter `http://localhost:5000/admin`.

In der Galerie kann optional nach Tags gefiltert werden, indem man einen Tag aus der Dropdown-Liste auswählt.
