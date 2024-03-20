from flask import Blueprint, jsonify, request
from mongo_client import Mongo2Client

joueurs_bp = Blueprint('joueur_bp', __name__)


@joueurs_bp.route('/', methods=['GET'])
def get_all_joueurs():
    with Mongo2Client() as mongo_client:
        db_joueur = mongo_client.db['joueur']
        joueurs = db_joueur.find()
        joueurs_dict = [joueur for joueur in joueurs]
        return jsonify(joueurs_dict)


@joueurs_bp.route('/<int:id_joueur>', methods=['GET'])
def get_joueur_by_id(id_joueur):
    with Mongo2Client() as mongo_client:
        db_joueur = mongo_client.db['joueur']
        joueur = db_joueur.find_one({'_id': id_joueur})
        if joueur:
            return jsonify(joueur)
        else:
            return jsonify({'erreur': f"le joueur d'identifiant {id_joueur} n'existe pas."}), 404


@joueurs_bp.route('/', methods=['POST'])
def add_joueur():
    data = request.get_json()
    with Mongo2Client() as mongo_client:
        db_joueur = mongo_client.db['joueur']
        insert_joueur = db_joueur.insert_one(data)
        if insert_joueur:
            return jsonify({"True": "La requete a bien été insérée"})
        else:
            return jsonify({"False": "Erreur lors de l'insertion"}), 404


@joueurs_bp.route('/<int:id_joueur>', methods=['DELETE'])
def delete_joueur_by_id(id_joueur):
    with Mongo2Client() as mongo_client:
        db_joueur = mongo_client.db['joueur']
        delete_joueur = db_joueur.delete_one({'_id': id_joueur})

        if delete_joueur:
            return jsonify({"True": "La suppression a bien été réalisée."})
        else:
            return jsonify({'False': 'Erreur lors de la suppression'}), 404


@joueurs_bp.route('/<int:id_joueur>', methods=['PUT'])
def update_joueur_by_id(id_joueur):
    data = request.json

    with Mongo2Client() as mongo_client:
        db_joueur = mongo_client.db['joueur']
        update_joueur = db_joueur.update_one({'_id': id_joueur}, {'$set': data})

        if update_joueur.modified_count > 0:
            return jsonify({"True": "La mise à jour a bien été réalisée."})
        else:
            return jsonify({'False': 'Erreur lors de la mise à jour'}), 404
