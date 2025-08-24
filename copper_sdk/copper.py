import sys
import os
from datetime import datetime
import requests
from retry import retry
from json import JSONDecodeError

from copper_sdk.pipeline_stages import PipelineStages
from copper_sdk.pipelines import Pipelines
from copper_sdk.users import Users
from copper_sdk.leads import Leads
from copper_sdk.account import Account
from copper_sdk.activities import Activities
from copper_sdk.companies import Companies
from copper_sdk.people import People
from copper_sdk.opportunities import Opportunities
from copper_sdk.customer_sources import CustomerSources
from copper_sdk.loss_reasons import LossReasons
from copper_sdk.custom_field_definitions import CustomFieldDefinitions
from copper_sdk.tags import Tags
from copper_sdk.tasks import Tasks
from copper_sdk.exception import TooManyRequests
from copper_sdk.webhooks import Webhooks

BASE_URL = 'https://api.copper.com/developer_api/v1'


class Copper:

    # Constructor - authentication details
    def __init__(self, token, email, base_url=BASE_URL, debug=False, session=None):
        self.token = token
        self.email = email
        self.base_url = base_url
        self.debug = debug
        self.num_50x = 0
        self.num_429 = 0
        self.num = 0

        # init request
        if not session:
            session = requests.Session()

        self.session = session
        self.session.headers = {
            'X-PW-AccessToken': self.token,
            'X-PW-Application': 'developer_api',
            'X-PW-UserEmail': self.email,
            # 'Content-Type': 'application/json',
        }

    def get(self, endpoint):
        return self.api_call('get', endpoint)

    def post(self, endpoint, opts):
        return self.api_call('post', endpoint, opts)

    def put(self, endpoint, opts):
        return self.api_call('put', endpoint, opts)

    def delete(self, endpoint, json_body=None):
        return self.api_call('delete', endpoint, json_body=json_body)


    def print_api(self, start_time, end_time, method, endpoint, code):
        if os.environ.get('COPPER_API_TRACE') is not None:
            elapsed = end_time - start_time
            print(f"COPPER_API_TRACE: {method}/{endpoint} -> {code} ({elapsed.seconds}.{elapsed.microseconds})", file=sys.stderr)


    @retry(exceptions=(TooManyRequests, JSONDecodeError, requests.exceptions.HTTPError), delay=1, backoff=5, max_delay=10, tries=100)
    def api_call(self, method, endpoint, json_body=None):
        self.num = self.num + 1
        if self.debug:
            print("json_body:", json_body)

        start_time = datetime.now()

        # dynamically call method to handle status change
        try:
            response = self.session.request(method, self.base_url + endpoint, json=json_body)
        except:
            self.print_api(start_time, datetime.now(), method, endpoint, "exception")
            raise

        self.print_api(start_time, datetime.now(), method, endpoint, response.status_code)

        if response.status_code == 429:
            self.num_429 = self.num_429 + 1
            raise TooManyRequests('429 Server Rate Limit', response=response, json_body=json_body)

        if self.debug:
            print(response.text)

        try:
            body = response.json()
        except requests.JSONDecodeError as exc:
            self.num_50x = self.num_50x + 1
            print(f"COPPER ERROR: copper {method} - {endpoint} - {exc} -- {self.num_50x} 50x errors, {self.num_429} 429 errors")
            print(f"COPPER ERROR: copper {response.status_code}: {exc}")
            print(f"COPPER ERROR: copper {response.content.decode('utf-8')}: {exc}")
            print(f"COPPER ERROR: {response} is not JSON")
            body = None
            response.close()
            raise requests.exceptions.HTTPError(endpoint, 500, f"Internal copper error {response.content.decode('utf-8')}", None, None)
        except JSONDecodeError as exc:
            self.num_50x = self.num_50x + 1
            print(f"COPPER ERROR: copper {method} - {endpoint} - {exc} -- {self.num_50x} 50x errors, {self.num_429} 429 errors")
            print(f"COPPER ERROR: copper {response.status_code}: {exc}")
            print(f"COPPER ERROR: copper {response.content.decode('utf-8')}: {exc}")
            print(f"COPPER ERROR: {response} is not JSON")
            body = None
            response.close()
            raise requests.exceptions.HTTPError(endpoint, 500, f"Internal copper error {response.content.decode('utf-8')}", None, None)

        if body is not None and "success" in body and body["success"] == False and "status" in body and body["status"] == 500:
            response.close()
            raise requests.exceptions.HTTPError(endpoint, 500, "Internal copper error", None, None)

        return response.json()

    @property
    def users(self):
        return Users(self)

    @property
    def leads(self):
        return Leads(self)

    @property
    def account(self):
        return Account(self)

    @property
    def activities(self):
        return Activities(self)

    @property
    def opportunities(self):
        return Opportunities(self)

    @property
    def people(self):
        return People(self)

    @property
    def companies(self):
        return Companies(self)

    @property
    def customersources(self):
        return CustomerSources(self)

    @property
    def lossreasons(self):
        return LossReasons(self)

    @property
    def tags(self):
        return Tags(self)

    @property
    def tasks(self):
        return Tasks(self)

    @property
    def customfielddefinitions(self):
        return CustomFieldDefinitions(self)

    @property
    def webhooks(self):
        return Webhooks(self)

    @property
    def pipelines(self):
        return Pipelines(self)

    @property
    def pipelinestages(self):
        return PipelineStages(self)
