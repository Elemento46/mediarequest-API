import os
import requests
from twitchio.ext import commands # type: ignore

TWITCH_TOKEN = "xrhovzl5e36gi1cz1ixss13c2dgwuj"
TWITCH_CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"
TWITCH_NICK = "ElementaryBot"
TWITCH_CHANNEL = "elemento46"
STREAM_ELEMENTS_API_KEY = "https://api.streamelements.com/kappa/v3"
STREAM_ELEMENTS_BASE_URL = "https://api.streamelements.com/kappa/v3/songrequest"

class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(token=TWITCH_TOKEN, prefix='!', initial_channels=[TWITCH_CHANNEL])

    async def event_ready(self):
        print(f"Bot conectado como {self.nick} no canal {TWITCH_CHANNEL}")

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    @commands.command(name="accept")
    async def accept_song(self, ctx):
        """Aceita a primeira música pendente na fila de Song Request."""
        response = self.manage_song_request(action="accept")
        if response:
            await ctx.send("🎵 Música aceita com sucesso!")
        else:
            await ctx.send("❌ Erro ao aceitar a música. Verifique a fila ou a API Key.")

    @commands.command(name="reject")
    async def reject_song(self, ctx):
        """Recusa a primeira música pendente na fila de Song Request."""
        response = self.manage_song_request(action="reject")
        if response:
            await ctx.send("🎵 Música rejeitada com sucesso!")
        else:
            await ctx.send("❌ Erro ao rejeitar a música. Verifique a fila ou a API Key.")

    def manage_song_request(self, action):
        """Gerencia a primeira música pendente com base na ação (accept/reject)."""
        url = f"{STREAM_ELEMENTS_BASE_URL}/{action}"
        headers = {
            "Authorization": f"Bearer {STREAM_ELEMENTS_API_KEY}"
        }
        try:
            response = requests.put(url, headers=headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao gerenciar música: {e}")
            return False

# Inicia o bot
if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()
