import json


def lambda_handler(event, context) -> dict:
    """
    Entrypoint Lambda function handler.

    Args:
        event: API Gateway event object
        context: Lambda context object

    Returns:
        dict: API Gateway response
    """
    print(f"Entrypoint event: {event}")

    # Parse the HTTP method and path
    http_method = event.get("httpMethod", "GET")
    path = event.get("path", "/")

    # Simple response for now
    response_body = {
        "message": f"Hello from entrypoint! Method: {http_method}, Path: {path}",
        "event": event,
    }

    return {
        "statusCode": 200,  ### try different status codes
        "headers": {
            "Content-Type": "application/json",
            # 'Access-Control-Allow-Origin': '*',
            # 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            # 'Access-Control-Allow-Headers': 'Content-Type, Authorization, api_key'
        },
        "body": json.dumps(response_body),
    }


### use different status codes
### logs go to individual Lambdas as well as API Gateway
