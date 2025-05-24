from flask import Flask, Blueprint, request, jsonify

# Import fungsi require_api_key dari auth
from app.auth import require_api_key
# Import variabel topup_data dari models
from app.models import topup_data


# Inisialisasi blueprint dengan prefix "/api"
bp = Blueprint("main", __name__, url_prefix="/api")


# --- Endpoint Topup ---


@bp.route("/topup", methods=["GET"])
@require_api_key
def get_all():
    """Ambil semua data topup."""
    return jsonify(topup_data)


@bp.route("/topup", methods=["POST"])
@require_api_key
def create():
    """Buat entri topup baru."""
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Format data tidak valid atau kosong"}), 400

    if 'user' not in data or 'amount' not in data:
        return jsonify({"error": "Data 'user' atau 'amount' tidak lengkap"}), 400

    topup_data.append(data)
    return jsonify({
        "message": "Topup berhasil ditambahkan",
        "data": data
    }), 201


@bp.route("/topup/<int:idx>", methods=["PUT"])
@require_api_key
def update(idx):
    """Perbarui entri topup berdasarkan indeks."""
    if idx < 0 or idx >= len(topup_data):
        return jsonify({"error": "Data tidak ditemukan"}), 404

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Format data tidak valid atau kosong"}), 400

    if 'user' not in data or 'amount' not in data:
        return jsonify({"error": "Data 'user' atau 'amount' tidak lengkap"}), 400

    topup_data[idx] = data
    return jsonify({
        "message": "Topup berhasil diperbarui",
        "data": data
    })


@bp.route("/topup/<int:idx>", methods=["DELETE"])
@require_api_key
def delete(idx):
    """Hapus entri topup berdasarkan indeks."""
    if idx < 0 or idx >= len(topup_data):
        return jsonify({"error": "Data tidak ditemukan"}), 404

    deleted_item = topup_data.pop(idx)
    return jsonify({
        "message": "Topup berhasil dihapus",
        "data_terhapus": deleted_item
    })


# --- Health Check Endpoint ---


@bp.route("/health")
def health_check():
    """Endpoint untuk mengecek status layanan."""
    return jsonify({"status": "sehat"})


# --- Daftarkan blueprint ke Flask app ---


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app