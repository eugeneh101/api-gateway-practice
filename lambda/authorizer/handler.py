def generate_policy(principal_id: str, effect: str, resource: str) -> dict:
    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
            ],
        },
    }


def lambda_handler(event, context) -> dict:
    """
    Args:
        event: API Gateway authorizer event
        context: Lambda context object

    Returns:
        dict: IAM policy document that allows the request
    """
    print(f"event: {event}")
    # Extract the method and resource ARN from the event
    method_arn = event["methodArn"]
    if event["headers"].get("api_key") == "super_secret_api_key":
        return generate_policy(principal_id="user", effect="Allow", resource=method_arn)
    else:
        return generate_policy(principal_id="user", effect="Deny", resource=method_arn)


### how to test these APIs other than running it in dev? Run in Docker
### what parts of the event to log?
### what are stages?
