# Sommertermine 2026

Diese kleine Webseite zeigt eine Auswahl von Veranstaltungen im Sommer 2026 im Stil von Quartettkarten.

## Nutzung

Öffne die Datei `index.html` in einem Browser deiner Wahl. Beim Überfahren einer Karte mit der Maus wird sie leicht vergrößert, als würde man sie hochheben.

## Struktur

- `index.html` – Einstiegspunkt der Webseite
- `styles.css` – Gestaltung der Karten und des Layouts
- `script.js` – Logik zum Erzeugen der Karten aus den Termindaten

## Anforderungen

Die Seite nutzt ausschließlich HTML, CSS und JavaScript ohne zusätzliche Bibliotheken.

## KeePass Bereinigungsskript

Im Ordner `tools` liegt das Skript `cleanup_kdbx.py`, das verwaiste Einträge in einer
KeePass-Datenbank aufräumt. Es erwartet eine CSV-Datei mit allen gültigen
E-Mail-Adressen und löscht in den angegebenen Gruppen alle Einträge, deren Adresse
nicht in der CSV vorhanden ist. Das Skript benötigt die Python-Bibliothek
[`pykeepass`](https://pykeepass.readthedocs.io/).

Beispielaufruf:

```bash
python tools/cleanup_kdbx.py \
    --database pfad/zur/datei.kdbx \
    --password geheim \
    --csv aktive_konten.csv \
    --groups "Root/FirmaA" "Root/FirmaB" \
    --email-column email \
    --dry-run
```

Mit `--dry-run` erhältst du lediglich eine Liste der zu löschenden Einträge, ohne die
Datenbank zu verändern. Lässt du die Option weg, speichert das Skript die bereinigte
Datenbank standardmäßig wieder unter dem ursprünglichen Pfad oder – falls angegeben –
unter dem Pfad aus `--output`.
