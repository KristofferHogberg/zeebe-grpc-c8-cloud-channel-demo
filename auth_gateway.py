import grpc


class AuthGateway(grpc.AuthMetadataPlugin):
    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, context, callback):
        callback((("authorization", f"Bearer {self.access_token}"),), None)
