import requests
import logging
from typing import List
from ..config import Config
from ..exceptions.exceptions import InvalidUnspent

log = logging.getLogger(__name__)


class Unspent:

    @staticmethod
    def get_unspent_outputs(address: str, confirmations=None) -> List:
        """
        Get unspent outputs for a single address.
            :param str address: address(xpub or base58) to look up
            :param int confirmations: minimum confirmations to include (optional)
            :return: an array of :class:`UnspentOutput` objects
        """
        try:
            log.info(f'Fetching unspent for address {address}...')

            params = {'active': address}
            if confirmations is not None:
                params['confirmations'] = str(confirmations)
            r = requests.get(url=Config.API_URL + '/unspent', params=params)

            if not r.ok:
                raise InvalidUnspent("invalid unspent: " + str(r.json()))

            json = r.json()
            unspent = json["unspent_outputs"][::-1]

            log.info(f'{len(unspent)} unspent found for address {address}')

            return unspent
        except Exception as e:
            raise InvalidUnspent("invalid unspent: " + str(e))
