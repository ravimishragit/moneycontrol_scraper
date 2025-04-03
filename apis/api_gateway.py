import boto3
from config.settings import AWS_REGION, LAMBDA_FUNCTION_NAME, API_GATEWAY_NAME


def create_api_gateway():
    """Create API Gateway and integrate with Lambda"""

    apigateway = boto3.client('apigateway', region_name=AWS_REGION)

    # Create REST API
    api_response = apigateway.create_rest_api(
        name=API_GATEWAY_NAME,
        description="MoneyControl Scraper API"
    )

    api_id = api_response['id']

    # Create resource
    resources = apigateway.get_resources(restApiId=api_id)
    root_id = resources['items'][0]['id']

    resource = apigateway.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='scraper'
    )

    # Lambda integration
    apigateway.put_method(
        restApiId=api_id,
        resourceId=resource['id'],
        httpMethod='GET',
        authorizationType='NONE'
    )

    lambda_arn = f"arn:aws:lambda:{AWS_REGION}:123456789012:function:{LAMBDA_FUNCTION_NAME}"

    apigateway.put_integration(
        restApiId=api_id,
        resourceId=resource['id'],
        httpMethod='GET',
        type='AWS_PROXY',
        integrationHttpMethod='POST',
        uri=f"arn:aws:apigateway:{AWS_REGION}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
    )

    # Deploy API
    apigateway.create_deployment(
        restApiId=api_id,
        stageName='prod'
    )

    print(f"API Gateway deployed: https://{api_id}.execute-api.{AWS_REGION}.amazonaws.com/prod/scraper")
