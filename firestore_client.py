"""
Firestore client — singleton initialisé une seule fois.

Configuration via variables d'environnement (priorité) ou fichier clé :
  - GOOGLE_APPLICATION_CREDENTIALS=/path/to/serviceAccountKey.json  (standard GCP)
  - FIRESTORE_PROJECT_ID=mon-projet                                  (optionnel, détecté auto)
  - FIRESTORE_EMULATOR_HOST=localhost:8080                           (dev local avec émulateur)

Si aucune credential n'est configurée, l'import lève une exception claire.
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore

_app = None
_client = None


def get_firestore_client():
    """
    Retourne le client Firestore initialisé (singleton).
    Appeler cette fonction au lieu de recréer le client à chaque requête.
    """
    global _app, _client

    if _client is not None:
        return _client

    if not firebase_admin._apps:
        key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if key_path and os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
        else:
            # Application Default Credentials (gcloud auth, GCE, Cloud Run…)
            cred = credentials.ApplicationDefault()

        project_id = os.environ.get("FIRESTORE_PROJECT_ID")
        _app = firebase_admin.initialize_app(cred, {"projectId": project_id} if project_id else {})
    else:
        _app = firebase_admin.get_app()

    _client = firestore.client()
    return _client
