# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import market_pb2 as market__pb2


class MarketStub(object):
    """Define the Market service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterSeller = channel.unary_unary(
                '/Market/RegisterSeller',
                request_serializer=market__pb2.SellerInfo.SerializeToString,
                response_deserializer=market__pb2.SuccessResponse.FromString,
                )
        self.SellItem = channel.unary_unary(
                '/Market/SellItem',
                request_serializer=market__pb2.ItemDetails.SerializeToString,
                response_deserializer=market__pb2.SuccessResponse.FromString,
                )
        self.UpdateItem = channel.unary_unary(
                '/Market/UpdateItem',
                request_serializer=market__pb2.UpdateItemRequest.SerializeToString,
                response_deserializer=market__pb2.SuccessResponse.FromString,
                )
        self.DeleteItem = channel.unary_unary(
                '/Market/DeleteItem',
                request_serializer=market__pb2.DeleteItemRequest.SerializeToString,
                response_deserializer=market__pb2.SuccessResponse.FromString,
                )
        self.DisplaySellerItems = channel.unary_unary(
                '/Market/DisplaySellerItems',
                request_serializer=market__pb2.SellerInfo.SerializeToString,
                response_deserializer=market__pb2.DisplayItems.FromString,
                )
        self.SearchItem = channel.unary_unary(
                '/Market/SearchItem',
                request_serializer=market__pb2.SearchRequest.SerializeToString,
                response_deserializer=market__pb2.DisplayItems.FromString,
                )
        self.BuyItem = channel.unary_unary(
                '/Market/BuyItem',
                request_serializer=market__pb2.BuyRequest.SerializeToString,
                response_deserializer=market__pb2.SuccessResponse.FromString,
                )
        self.AddToWishList = channel.unary_unary(
                '/Market/AddToWishList',
                request_serializer=market__pb2.AddToWishListRequest.SerializeToString,
                response_deserializer=market__pb2.SuccessResponse.FromString,
                )
        self.RateItem = channel.unary_unary(
                '/Market/RateItem',
                request_serializer=market__pb2.RateItemRequest.SerializeToString,
                response_deserializer=market__pb2.SuccessResponse.FromString,
                )


class MarketServicer(object):
    """Define the Market service
    """

    def RegisterSeller(self, request, context):
        """Seller functions
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SellItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisplaySellerItems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchItem(self, request, context):
        """Buyer functions
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuyItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddToWishList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RateItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MarketServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterSeller': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterSeller,
                    request_deserializer=market__pb2.SellerInfo.FromString,
                    response_serializer=market__pb2.SuccessResponse.SerializeToString,
            ),
            'SellItem': grpc.unary_unary_rpc_method_handler(
                    servicer.SellItem,
                    request_deserializer=market__pb2.ItemDetails.FromString,
                    response_serializer=market__pb2.SuccessResponse.SerializeToString,
            ),
            'UpdateItem': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateItem,
                    request_deserializer=market__pb2.UpdateItemRequest.FromString,
                    response_serializer=market__pb2.SuccessResponse.SerializeToString,
            ),
            'DeleteItem': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteItem,
                    request_deserializer=market__pb2.DeleteItemRequest.FromString,
                    response_serializer=market__pb2.SuccessResponse.SerializeToString,
            ),
            'DisplaySellerItems': grpc.unary_unary_rpc_method_handler(
                    servicer.DisplaySellerItems,
                    request_deserializer=market__pb2.SellerInfo.FromString,
                    response_serializer=market__pb2.DisplayItems.SerializeToString,
            ),
            'SearchItem': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchItem,
                    request_deserializer=market__pb2.SearchRequest.FromString,
                    response_serializer=market__pb2.DisplayItems.SerializeToString,
            ),
            'BuyItem': grpc.unary_unary_rpc_method_handler(
                    servicer.BuyItem,
                    request_deserializer=market__pb2.BuyRequest.FromString,
                    response_serializer=market__pb2.SuccessResponse.SerializeToString,
            ),
            'AddToWishList': grpc.unary_unary_rpc_method_handler(
                    servicer.AddToWishList,
                    request_deserializer=market__pb2.AddToWishListRequest.FromString,
                    response_serializer=market__pb2.SuccessResponse.SerializeToString,
            ),
            'RateItem': grpc.unary_unary_rpc_method_handler(
                    servicer.RateItem,
                    request_deserializer=market__pb2.RateItemRequest.FromString,
                    response_serializer=market__pb2.SuccessResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Market', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Market(object):
    """Define the Market service
    """

    @staticmethod
    def RegisterSeller(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Market/RegisterSeller',
            market__pb2.SellerInfo.SerializeToString,
            market__pb2.SuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SellItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Market/SellItem',
            market__pb2.ItemDetails.SerializeToString,
            market__pb2.SuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Market/UpdateItem',
            market__pb2.UpdateItemRequest.SerializeToString,
            market__pb2.SuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Market/DeleteItem',
            market__pb2.DeleteItemRequest.SerializeToString,
            market__pb2.SuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DisplaySellerItems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Market/DisplaySellerItems',
            market__pb2.SellerInfo.SerializeToString,
            market__pb2.DisplayItems.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SearchItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Market/SearchItem',
            market__pb2.SearchRequest.SerializeToString,
            market__pb2.DisplayItems.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BuyItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Market/BuyItem',
            market__pb2.BuyRequest.SerializeToString,
            market__pb2.SuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddToWishList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Market/AddToWishList',
            market__pb2.AddToWishListRequest.SerializeToString,
            market__pb2.SuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RateItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Market/RateItem',
            market__pb2.RateItemRequest.SerializeToString,
            market__pb2.SuccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class NotificationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NotifyClient = channel.unary_unary(
                '/NotificationService/NotifyClient',
                request_serializer=market__pb2.Notification.SerializeToString,
                response_deserializer=market__pb2.NotifyResponse.FromString,
                )


class NotificationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def NotifyClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NotificationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'NotifyClient': grpc.unary_unary_rpc_method_handler(
                    servicer.NotifyClient,
                    request_deserializer=market__pb2.Notification.FromString,
                    response_serializer=market__pb2.NotifyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'NotificationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NotificationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def NotifyClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/NotificationService/NotifyClient',
            market__pb2.Notification.SerializeToString,
            market__pb2.NotifyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
