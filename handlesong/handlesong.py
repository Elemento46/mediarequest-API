from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Substitua pelo seu JWT Token do StreamElements
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjaXRhZGVsIiwiZXhwIjoxNzQ2NjMxMTMzLCJqdGkiOiIxZGIzOWJiZS0zZjIwLTRiMzYtYTY2MC0yOTBmOWI3OTdjM2YiLCJjaGFubmVsIjoiNWY2ZmQ0ZDUxNDI0Njk4NGI3MjAxOGY0Iiwicm9sZSI6Im93bmVyIiwiYXV0aFRva2VuIjoia0dkbHg0ZGtjY2d4RVhnYTQ2cEc2V0VfVjRTTnhEbnExTHozRGVHNFF3bl9LcmdNIiwidXNlciI6IjVmNmZkNGQ1MTQyNDY5ZTJhMjIwMThmMyIsInVzZXJfaWQiOiJmMDk2NmM2Yi01Nzg5LTQ0MzItOWRjOS0wYzMxYmQwOTA3MmEiLCJ1c2VyX3JvbGUiOiJjcmVhdG9yIiwicHJvdmlkZXIiOiJ0d2l0Y2giLCJwcm92aWRlcl9pZCI6IjQ2ODc3ODkzNCIsImNoYW5uZWxfaWQiOiJhNmQ2MGVhYS1hODdiLTQzNGUtODFlZS0zYTU0YzAxNDJkZjIiLCJjcmVhdG9yX2lkIjoiMjQzMTljMmUtYTVmMy00ZDQ5LWI4ZTItM2Q4Njk4MzBhN2Y2In0.jKZsCAmrgKWAyWvE5CnTDTx-FRiRerNwn-SRubRp3AU"

@app.route('/handlesong/handlesong', methods=['GET'])
def handle_song():
    try:
        # Obter o valor da ação (approve ou reject) do parâmetro da URL
        action = request.args.get('action', 'approve')

        # URL para buscar a fila de músicas pendentes
        url = "https://api.streamelements.com/kappa/v2/songrequest/queue"
        
        # Cabeçalhos da requisição com o JWT Token
        headers = {
            "Authorization": f"Bearer {JWT_TOKEN}",
            "Content-Type": "application/json"
        }

        # Realiza a requisição GET para pegar as músicas pendentes
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta um erro se a resposta não for 2xx
        songs = response.json()

        # Caso não haja músicas pendentes
        if not songs:
            return jsonify({"message": "Nenhuma música pendente para processamento."})

        # Pega o primeiro item da fila de músicas
        song_id = songs[0]["_id"]

        # Definir a URL para aprovação ou rejeição da música
        if action == 'approve':
            action_url = f"{url}/{song_id}/approve"
        elif action == 'reject':
            action_url = f"{url}/{song_id}/reject"
        else:
            return jsonify({"error": "Ação inválida. Use 'approve' ou 'reject'."}), 400

        # Realiza a requisição PUT para aprovar ou rejeitar a música
        action_response = requests.put(action_url, headers=headers)
        action_response.raise_for_status()  # Levanta um erro se a resposta não for 2xx

        # Retorna uma mensagem de sucesso
        return jsonify({"message": f"Música {action} com sucesso!"})

    except requests.exceptions.RequestException as e:
        # Se houver qualquer erro nas requisições HTTP
        return jsonify({"error": f"Erro ao comunicar com StreamElements: {str(e)}"}), 500

    except Exception as e:
        # Qualquer outro tipo de erro
        return jsonify({"error": f"Ocorreu um erro inesperado: {str(e)}"}), 500


# Exigência do Vercel: atribuir a variável `app` corretamente
app = app
