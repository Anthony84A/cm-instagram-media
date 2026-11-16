# cm-instagram-media

Visuels et outils du compte Instagram [@a_arniaud](https://instagram.com/a_arniaud) (Anthony Arniaud, développeur web, Vaucluse).

Ce dépôt est public parce que Metricool récupère les images par lien public.

- `media/AAAA-MM-JJ/` : les JPEG publiés, rangés par semaine de préparation.
- `semaines/AAAA-MM-JJ/` : les fichiers de contenu (slides) de chaque semaine.
- `kit/` : le générateur de visuels (`render.py`), le logo et les captures de réalisations.
- `historique.md` : le journal des posts et des enseignements.

## Générer des visuels

    cd kit
    npm install
    pip install playwright && python -m playwright install chromium
    python render.py ../semaines/AAAA-MM-JJ/post1.json ../media/AAAA-MM-JJ/post1
