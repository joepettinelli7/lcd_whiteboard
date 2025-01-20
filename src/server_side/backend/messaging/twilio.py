"""
    LCD Whiteboard to create touchscreen whiteboard interface and send MMS.
    Copyright (C) 2025 Joseph Pettinelli

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see https://www.gnu.org/licenses/.
"""

import os
import pickle
import traceback
import typing
from datetime import datetime
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from src.server_side.app import ROOT_DIR

TWILIO_INFO_PATH: str = os.path.join(ROOT_DIR, 'src', 'server_side', 'backend', 'configs', 'wb_accounts_config.pkl')


class TwilioClient:
    """
    Use Twilio client to access the Twilio API
    to send whiteboard images to phone numbers
    """

    def __init__(self) -> None:
        self._client: typing.Optional[Client] = None
        self._phone_number: typing.Optional[str] = None
        self._ngrok_url: typing.Optional[str] = None

    def set_account_info(self) -> bool:
        """
        1. Set client
        2. Set the twilio phone number

        Returns:
             True if success, False if account info not found
        """
        try:
            twilio_info = pickle.load(open(TWILIO_INFO_PATH, 'rb'))
            sid = twilio_info['twilio_account_sid']
            auth_token = twilio_info['twilio_auth_token']
            number = twilio_info['twilio_number']
            self._client = Client(sid, auth_token)
            self._phone_number = number
            return True
        except FileNotFoundError:
            traceback.print_exc()
            print('There is not twilio account info.')
            return False

    def send_to_all(self, image_page: str, phone_numbers: typing.List[str]) -> None:
        """
        Send an image of the current drawing surface to phone numbers

        Args:
            image_page: Name of image webpage where image is
            phone_numbers: The list of phone numbers to send image to

        Returns:

        """
        if len(phone_numbers) > 0:
            try:
                assert self.ngrok_url is not None
                url = self.ngrok_url
                # requests.get(url=url, headers={"ngrok-skip-browser-warning": "1999"}, stream=True)
                image_url = f"{url}/{image_page}"
                c_time = self.get_time()
                for phone_number in phone_numbers:
                    self.send_single(image_url, phone_number, c_time)
            except AssertionError:
                print('Error: ngrok URL is None.')
        else:
            return None

    def send_single(self, image_url: str, to_phone_number: str, c_time: str) -> None:
        """
        Send an image of the current drawing surface to phone number

        Args:
            image_url: The full URL to image
            to_phone_number: The phone number to send image to
            c_time: Current date and time

        Returns:

        """
        try:
            print(f'Sending message to {to_phone_number}.')
            message = self._client.messages.create(
                body=c_time,
                from_=f"{self._phone_number}",
                to=to_phone_number,
                media_url=[image_url],
                send_as_mms=True)
            print(message.sid)
        except TwilioRestException:
            print('Error: Twilio phone number is not valid SMS-capable number.')

    @staticmethod
    def get_time() -> str:
        """
        Get the date and time for message body

        Returns:
             The date and time
        """
        now = datetime.now()
        # format to minute precision
        formatted_now = now.strftime("%Y-%m-%d %H:%M")
        assert isinstance(formatted_now, str)
        return formatted_now

    @property
    def ngrok_url(self) -> typing.Optional[str]:
        """

        Returns:
             The ngrok public URL
        """
        return self._ngrok_url

    @ngrok_url.setter
    def ngrok_url(self, new_url: str) -> None:
        """
        Set the new ngrok public URL

        Args:
            new_url: Public ngrok URL

        Returns:

        """
        assert isinstance(new_url, str)
        self._ngrok_url = new_url


if __name__ == "__main__":
    pass
