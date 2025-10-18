from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_lambda as _lambda,
)
from constructs import Construct


class ApiGatewayPracticeStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, environment: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.authorizer_lambda = _lambda.Function(
            self,
            "AuthorizerLambda",
            function_name="authorizer",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda/authorizer"),
        )
        self.entrypoint_lambda = _lambda.Function(
            self,
            "EntrypointLambda",
            function_name="entrypoint",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda/entrypoint"),
        )

        self.entrypoint = apigateway.RestApi(
            self,
            "Entrypoint",
            rest_api_name="entrypoint",
            description="Entrypoint API",
            deploy_options=apigateway.StageOptions(
                stage_name="dev",  # why do we need this?
                metrics_enabled=True,  # don't really know what this is for
                logging_level=apigateway.MethodLoggingLevel.INFO,  # where is this logged? API-Gateway-Execution-Logs_*
                # data_trace_enabled=True,  # turn off in production, as it logs everything; still shows partial header though
                tracing_enabled=True,  # X-ray tracing
            ),
            endpoint_types=[apigateway.EndpointType.REGIONAL],
            # api_key_source_type=apigateway.ApiKeySourceType.HEADER,
        )  # look at API's dashboard to see number of API calls, latency, error rates, etc.
        self.entrypoint_resource = self.entrypoint.root.add_resource("entrypoint")
        self.entrypoint_integration = apigateway.LambdaIntegration(
            self.entrypoint_lambda
        )

        self.authorizer = apigateway.RequestAuthorizer(
            self,
            "Authorizer",
            authorizer_name="request-authorizer",
            handler=self.authorizer_lambda,
            results_cache_ttl=Duration.seconds(60),
            identity_sources=[apigateway.IdentitySource.header("api_key")],
        )
        self.entrypoint_resource.add_method(
            http_method="POST",
            integration=self.entrypoint_integration,
            authorizer=self.authorizer,
        )

        self.role = iam.Role(
            self,
            "ApiGatewayRole",
            role_name="api-gateway-logging-role",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
        )
        self.role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AmazonAPIGatewayPushToCloudWatchLogs"
            )
        )
        apigateway.CfnAccount(  # seems to be a setting for a whole region
            self,
            "ApiGatewayAccountSetting",
            cloud_watch_role_arn=self.role.role_arn,
        )
