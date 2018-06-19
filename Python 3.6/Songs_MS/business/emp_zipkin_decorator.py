from py_zipkin.zipkin import zipkin_span
from py_zipkin.stack import ThreadLocalStack
from business.htt_transport import HttpTransport


def emp_zipkin_decorator(service_name, span_name, port, binary_annotations=None, transport_handler=HttpTransport(),
                         sample_rate=100):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            zipkin_attrs = ThreadLocalStack().get()
            if zipkin_attrs is None:
                with zipkin_span(
                        service_name=service_name,
                        span_name=span_name,
                        transport_handler=transport_handler,
                        port=port,
                        sample_rate=sample_rate,
                        binary_annotations=binary_annotations,
                ):
                    result = function(*args, **kwargs)
                    return result
            else:
                with zipkin_span(service_name=service_name, span_name=span_name):
                    result = function(*args, **kwargs)
                    return result
        return wrapper
    return real_decorator
