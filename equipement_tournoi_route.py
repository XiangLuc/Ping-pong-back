from flask import Blueprint, jsonify, request
from mongo_client import Mongo2Client

equipement_tournoi_bp = Blueprint('equipement_tournoi', __name__)


@equipement_tournoi_bp.route('/', methods=['GET'])
def get_all_equipements_tournoi():
    with Mongo2Client() as mongo_client:
        db_equipement_tournoi = mongo_client.db['equipement_tournoi']
        equipements_tournoi = db_equipement_tournoi.find()
        equipement_dict = [equipement for equipement in equipements_tournoi]
        return jsonify(equipement_dict)


@equipement_tournoi_bp.route('/<int:id_equipement_tournoi>', methods=['GET'])
def get_tournoi_by_id(id_equipement_tournoi):
    with Mongo2Client() as mongo_client:
        db_equipement = mongo_client.db['equipement_tournoi']
        equipement_tournoi = db_equipement.find_one({'_id': id_equipement_tournoi})

        if equipement_tournoi:
            return jsonify(equipement_tournoi)
        else:
            return jsonify({'erreur': f"les équipements d'identifiant {id_equipement_tournoi} n'existe pas."}), 404


@equipement_tournoi_bp.route('/', methods=['POST'])
def add_joueur():
    data = request.get_json()
    with Mongo2Client() as mongo_client:
        db_equipement = mongo_client.db['equipement_tournoi']
        insert_equipement = db_equipement.insert_one(data)
        if insert_equipement:
            return jsonify({"True": "La requete a bien été insérée"})
        else:
            return jsonify({"False": "Erreur lors de l'insertion"}), 404


@equipement_tournoi_bp.route('/<int:id_equipement_tournoi>', methods=['DELETE'])
def delete_joueur_by_id(id_equipement_tournoi):
    with Mongo2Client() as mongo_client:
        db_equipement = mongo_client.db['equipment_tournoi']
        delete_equipement_tournoi = db_equipement.delete_one({'_id': id_equipement_tournoi})

        if delete_equipement_tournoi.modified_count > 0:
            return jsonify({"True": "La suppression a bien été réalisée."})
        else:
            return jsonify({'False': 'Erreur lors de la suppression'}), 404


@equipement_tournoi_bp.route('/<int:id_equipement_tournoi>', methods=['PUT'])
def update_tournoi_by_id(id_equipement_tournoi):
    data = request.json

    with Mongo2Client() as mongo_client:
        db_equipement_tournoi = mongo_client.db['equipement_tournoi']
        update_equipement_tournoi = db_equipement_tournoi.update_one({'_id': id_equipement_tournoi}, {'$set': data})

        if update_equipement_tournoi.modified_count > 0:
            return jsonify({"True": "La mise à jour a bien été réalisée."})
        else:
            return jsonify({'False': 'Erreur lors de la mise à jour'}), 404
