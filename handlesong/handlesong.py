from flask import Flask, request, jsonify# type: ignore
import requests# type: ignore

app = Flask(__name__)

# Substitua pelo seu JWT Token do StreamElements
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjaXRhZGVsIiwiZXhwIjoxNzQ2MzU3OTc4LCJqdGkiOiJjMjk2ZGNiOS0zNDczLTRjZDUtYjEwNi1lYjU0NjBmNThlOWMiLCJjaGFubmVsIjoiNjAzZDRkYTI2YTJiMmY0ZmUyYjljMWIxIiwicm9sZSI6Im93bmVyIiwiYXV0aFRva2VuIjoiZFBwNGstUnhOWEk0UURLOUZZN0hjUkVrUTNLZ0c4aEZSYUdwdWdzVkMxcU0xRGxqIiwidXNlciI6IjYwM2Q0ZGEyNmEyYjJmZWFjMGI5YzFiMCIsInVzZXJfaWQiOiJlYWRkMWM4YS00MjQyLTQ5ODYtOGMxNi1kOTY5Zjc2OTYzMzAiLCJ1c2VyX3JvbGUiOiJjcmVhdG9yIiwicHJvdmlkZXIiOiJ0d2l0Y2giLCJwcm92aWRlcl9pZCI6IjQzNzcwNDQyMyIsImNoYW5uZWxfaWQiOiI5OTA2ZTk4Mi01NmI4LTRmN2YtYTI5Yi04ZjRiMzcwYzFiYjYiLCJjcmVhdG9yX2lkIjoiNTVlZWUwOTAtNTg3NC00ZDIzLWE4MzgtYzdjNzMwZjllZDFhIn0.AWe54WPkcsKApF405A_gGPxwRqggttydrDJkiQoa32g"

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
