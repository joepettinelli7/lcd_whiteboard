import pickle
import re
import typing
from unittest.mock import patch, MagicMock
import pytest
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from src.server_side.backend.messaging.twilio import TwilioClient


@pytest.fixture
def twilio_fix() -> TwilioClient:
    twilio_client = TwilioClient()
    twilio_client._ngrok_url = 'test_url'
    return twilio_client


@pytest.fixture
def info_fix() -> typing.Dict[str, str]:
    test_info = {'twilio_account_sid': 'aaa',
                 'twilio_auth_token': 'bbb',
                 'twilio_number': '+123',
                 'ngrok_auth_token': 'ccc'}
    return test_info


class TestTwilioClient:

    def test_set_account_info(self, twilio_fix: TwilioClient, info_fix: typing.Dict[str, str]) -> None:
        """

        """
        with patch.object(pickle, 'load') as patch_load:
            with patch("builtins.open"):
                patch_load.return_value = info_fix
                sid = info_fix['twilio_account_sid']
                auth_token = info_fix['twilio_auth_token']
                with patch.object(Client, '__new__') as patch_client:
                    patch_client.return_value = MagicMock()
                    twilio_fix.set_account_info()
                    patch_load.assert_called_once()
                    patch_client.assert_called_with(Client, sid, auth_token)
                    assert twilio_fix._client is patch_client.return_value
                    assert twilio_fix._phone_number is info_fix['twilio_number']

    @pytest.mark.parametrize('nums', [['111'], ['111', '222'], []])
    def test_send_to_all1(self, twilio_fix: TwilioClient, nums: typing.List[str]) -> None:
        """
        Test that the function works regardless of length of numbers list
        """
        test_img_name = 'mock_name.png'
        time = '2024-07-9 14:00'
        with patch.object(twilio_fix, 'send_single') as patch_send_sing:
            with patch.object(twilio_fix, 'get_time') as patch_time:
                patch_time.return_value = time
                twilio_fix.send_to_all(test_img_name, nums)
                if len(nums) == 0:
                    patch_send_sing.assert_not_called()
                    patch_time.assert_not_called()
                else:
                    assert patch_send_sing.call_count == len(nums)
                    patch_time.assert_called_once()
                    url_base = twilio_fix._ngrok_url
                    patch_send_sing.assert_any_call(f'{url_base}/{test_img_name}', nums[0], time)

    @pytest.mark.parametrize('ngrok_url', ['mock_url', None])
    def test_send_to_all2(self, twilio_fix: TwilioClient, ngrok_url: typing.Optional[str]) -> None:
        """
        Test that the function works regardless of ngrok URL
        """
        twilio_fix._ngrok_url = ngrok_url
        test_img_name = 'mock_name.png'
        num = '111'
        time = '2024-07-9 14:00'
        with patch.object(twilio_fix, 'send_single') as patch_send_sing:
            with patch.object(twilio_fix, 'get_time') as patch_time:
                patch_time.return_value = time
                if ngrok_url is None:
                    twilio_fix.send_to_all(test_img_name, [num])
                    patch_send_sing.assert_not_called()
                    patch_time.assert_not_called()
                else:
                    twilio_fix.send_to_all(test_img_name, [num])
                    patch_send_sing.assert_called_once_with(f'{ngrok_url}/{test_img_name}', num, time)
                    patch_time.assert_called_once()

    @pytest.mark.parametrize('error', [TwilioRestException(0, ''), ])
    def test_send_single(self, twilio_fix: TwilioClient, error: typing.Any) -> None:
        """

        """
        twilio_fix._client = MagicMock()
        twilio_fix._phone_number = '111'
        with patch.object(twilio_fix._client.messages, 'create') as patch_create:
            patch_create.side_effect = error
            twilio_fix.send_single('image_url', '123', '2024-07-09 14:00')
            patch_create.assert_called_once_with(body='2024-07-09 14:00',
                                                 from_='111',
                                                 to='123',
                                                 media_url=['image_url'],
                                                 send_as_mms=True)

    def test_get_time(self, twilio_fix: TwilioClient) -> None:
        """

        """
        time = twilio_fix.get_time()
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$'
        matches = re.match(pattern, time)
        assert matches[0]

    def test_ngrok_url_getter(self, twilio_fix: TwilioClient) -> None:
        """

        """
        assert twilio_fix._ngrok_url is twilio_fix.ngrok_url
        assert isinstance(twilio_fix.ngrok_url, str)

    @pytest.mark.parametrize('new_url', ["u", "r", "l"])
    def test_ngrok_url_setter(self, twilio_fix: TwilioClient, new_url: str) -> None:
        """

        """
        twilio_fix.ngrok_url = new_url
        assert twilio_fix._ngrok_url is new_url


if __name__ == "__main__":
    pass
