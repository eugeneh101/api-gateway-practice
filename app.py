import aws_cdk as cdk

from api_gateway_practice import ApiGatewayPracticeStack


app = cdk.App()
environment = app.node.try_get_context("environment")
ApiGatewayPracticeStack(
    app,
    "api-gateway-practice",
    env=cdk.Environment(region=environment["AWS_REGION"]),
    environment=environment,
)
app.synth()
