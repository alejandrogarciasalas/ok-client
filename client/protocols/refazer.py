from client.protocols.common import models
from client.utils import auth
import client

import json
import logging
import urllib.error
import urllib.request
import webbrowser

log = logging.getLogger(__name__)


class RefazerProtocol(models.Protocol):
    # Timeouts are specified in seconds.
    SHORT_TIMEOUT = 10
    API_ENDPOINT = '{prefix}://{server}'
    ALLOW_QUESTIONS = [] #TODO: beta testing with accumulate

    def run(self, messages):
        if not self.args.refazer:
            log.info("Refazer not enabled.")
            return
        elif self.args.local:
            log.info("Refazer requires network access.")
            return

        if not messages.get('analytics'):
            log.warning("Refazer needs to be after analytics")
            return
        if not messages.get('grading'):
            log.warning("Refazer needs to be after grading")
            return
        if not self.args.question:
            log.warning("Refazer requires a specific question")
            return
        messages['refazer'] = {}

        grading = messages['grading']

        if not self.args.question:
            log.info("-q flag was not specified")
            print("To use Refazer you must specify the -q flag!")
            return

        # TODO: question filtering
        # for question in self.args.question:
        #     if question not in RefazerProtocol.ALLOW_QUESTIONS:
        #         log.info("Not a Refazer question")
        #         print("Make sure the question you are using is an Refazer question!")
        #         return

        messages['analytics']['identifier'] = auth.get_identifier()
        # Send data to refazer

        response_url = self.send_messages(messages, self.SHORT_TIMEOUT) #TODO: web api must return url for python tutor

        #TODO: error handling
        # Parse response_url
        # if response_url:
        #     webbrowser.open_new(response_url)
        # else:
        #     log.error("There was an error with Refazer. Please try again later!")

    def send_messages(self, messages, timeout):
        """Send messages to server, along with user authentication."""

        data = {
            'assignment': self.assignment.endpoint,
            'messages': messages,
            'submit': self.args.submit
        }

        print(data)
        serialized_data = json.dumps(data).encode(encoding='utf-8')
        server = '' #TODO: placeholder w/ azure server

        """"
        address = self.API_ENDPOINT.format(server=server, prefix='http' if self.args.insecure else 'https')
        address_params = {
            'client_name': 'ok-client',
            'client_version': client.__version__,
        }

        #TODO: construct address
        #address += '?'
        #address += '&'.join('{}={}'.format(param, value) for param, value in address_params.items())

        log.info('Sending messages to %s', address)
        try:
            request = urllib.request.Request(address)
            request.add_header("Content-Type", "application/json")
            response = urllib.request.urlopen(request, serialized_data, timeout)
            response_dict = json.loads(response.read().decode('utf-8'))
            return response_dict['url'] #TODO: make sure C# server returns url

        except (urllib.error.URLError, urllib.error.HTTPError,
                json.decoder.JSONDecodeError) as ex:
            log.warning('%s: %s', ex.__class__.__name__, str(ex))
        return
        """

protocol = RefazerProtocol
