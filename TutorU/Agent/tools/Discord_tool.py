import sys
import os
import requests
from typing import Dict


class Discord_tool:
    def __init__(self, discord_webhook):
        self.discord_webhook = discord_webhook
        self.send = self._send

    def _send(self, message: str) -> Dict[str, str]:
        """
        Sends a message to Discord channel via webhook.

        Args:
            message (str): Text content to send to Discord

        Returns:
            dict: {'message': 'success'} if sent, {'message': 'error message'} if failed
        """
        data = {"content": message}
        try:
            response = requests.post(self.discord_webhook, json=data)
            if response.status_code == 204:
                return {'message': 'success'}
            return {'message': f'Failed to send message. Status code: {response.status_code}'}
        except Exception as e:
            return {'message': f'Error: {str(e)}'}


# if __name__ == "__main__": 
#     testing = Discord_tool("")
#     testing.send("Niccy has no Rizz")