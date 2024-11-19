from flask import Flask, request, jsonify# type: ignore
import requests# type: ignore

app = Flask(__name__)

# Substitua pelo seu JWT Token do StreamElements
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjaXRhZGVsIiwiZXhwIjoxNzQ2NjMxMTMzLCJqdGkiOiIxZGIzOWJiZS0zZjIwLTRiMzYtYTY2MC0yOTBmOWI3OTdjM2YiLCJjaGFubmVsIjoiNWY2ZmQ0ZDUxNDI0Njk4NGI3MjAxOGY0Iiwicm9sZSI6Im93bmVyIiwiYXV0aFRva2VuIjoia0dkbHg0ZGtjY2d4RVhnYTQ2cEc2V0VfVjRTTnhEbnExTHozRGVHNFF3bl9LcmdNIiwidXNlciI6IjVmNmZkNGQ1MTQyNDY5ZTJhMjIwMThmMyIsInVzZXJfaWQiOiJmMDk2NmM2Yi01Nzg5LTQ0MzItOWRjOS0wYzMxYmQwOTA3MmEiLCJ1c2VyX3JvbGUiOiJjcmVhdG9yIiwicHJvdmlkZXIiOiJ0d2l0Y2giLCJwcm92aWRlcl9pZCI6IjQ2ODc3ODkzNCIsImNoYW5uZWxfaWQiOiJhNmQ2MGVhYS1hODdiLTQzNGUtODFlZS0zYTU0YzAxNDJkZjIiLCJjcmVhdG9yX2lkIjoiMjQzMTljMmUtYTVmMy00ZDQ5LWI4ZTItM2Q4Njk4MzBhN2Y2In0.jKZsCAmrgKWAyWvE5CnTDTx-FRiRerNwn-SRubRp3AU"

@app.route('/api/handlesong', methods=['GET'])
def handle_song():
    try:
        action = request.args.get('action', 'approve')
        url = "https://api.streamelements.com/kappa/v2/songrequest/queue"
        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        songs = response.json()

        if not songs:
            return jsonify({"message": "Nenhuma música pendente para processamento."})

        song_id = songs[0]["_id"]

        if action == 'approve':
            action_url = f"{url}/{song_id}/approve"
        elif action == 'reject':
            action_url = f"{url}/{song_id}/reject"
        else:
            return jsonify({"error": "Ação inválida. Use 'approve' ou 'reject'."}), 400

        action_response = requests.put(action_url, headers=headers)
        action_response.raise_for_status()

        return jsonify({"message": f"Música {action} com sucesso!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Exigência do Vercel: atribuir o app a uma variável chamada `app`
app = app
