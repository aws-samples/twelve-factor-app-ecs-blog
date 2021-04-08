import os

from config_helper import AppConfigHelper

from flask import Flask
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Attempt to refresh config every 1 hour
CONFIG_REFRESH_TIME = 3600

appconfig = AppConfigHelper(
    os.environ['ConfigApp'],
    os.environ['ConfigEnv'],
    os.environ['ConfigProfile'],
    CONFIG_REFRESH_TIME,  
    os.environ['ConfigClient']
)


@app.route('/')
def health():
    """
    Health check endpoint for the load balancer to poll
    """
    return "All good !"


@app.route('/hello')
def hello_world():
    """
    Display hello message using the information from the Dynamo table
    """
    ddb_client = boto3.client(
        'dynamodb', region_name=os.environ['AWS_DEFAULT_REGION'])
    TABLE_NAME = get_table_name()
    try:
        response = ddb_client.get_item(
            TableName=TABLE_NAME,
            Key={'Application': {'S': 'TwelveFactorApp'}})
        return f"<html><body style=\"background-color"\
            f":{response['Item']['BgColor']['S']};text-align:center\">"\
            f"<p><strong>Hello from {response['Item']['Name']['S']}!</strong></p>"\
            f"<p>Developed with {response['Item']['Language']['S']},"\
            f" deployed with {response['Item']['Platform']['S']}"\
            "</p></body></html>"
    except ClientError as e:
        return response['Error']['Message']


def get_table_name():
    """
     Get table name from App Config
    """
    appconfig.update_config()
    return appconfig.config["TableName"]


@app.route('/table-name')
def table_name():
    """
     Return table name using API
    """
    return get_table_name()


@app.route('/refresh-config')
def refresh():
    """
     Force refresh config using the API endpoint
    """
    result = "Config Refreshed" if appconfig.update_config(
        force=True) else "Nothing to refresh"
    return result

# Bind the Flask application to port 80 of the runtime environment
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
