Initialiser les migrations (⚠️ une seule fois) :
flask --app wsgi db init
Créer une migration (à chaque modification des modèles) :
flask --app wsgi db migrate -m "message_de_migration"
Appliquer la migration (création / update des tables) :
flask --app wsgi db upgrade

Lancer l'app 
flask --app wsgi run
