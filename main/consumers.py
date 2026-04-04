import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            # Tolak koneksi dari pengguna yang tidak login
            await self.close()
        else:
            self.user_id = self.scope["user"].id
            self.room_group_name = f"user_dashboard_{self.user_id}"

            # Bergabung ke "Ruang Siaran" khusus milik pengguna
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        # Keluar dari "Ruang Siaran"
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    # Fungsi ini dipanggil secara internal oleh channel layer saat menyebarkan sinyal
    async def new_message(self, event):
        message_data = event["message"]

        # Kirim pesan tersebut langsung ke Jaringan WebSocket *Browser* Pengguna
        await self.send(
            text_data=json.dumps({"type": "new_message", "data": message_data})
        )
