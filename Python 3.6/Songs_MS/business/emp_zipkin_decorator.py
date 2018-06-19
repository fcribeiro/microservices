from py_zipkin.zipkin import zipkin_span
from py_zipkin.stack import ThreadLocalStack
from business.htt_transport import HttpTransport


def emp_zipkin_decorator(service_name, span_name, port, binary_annotations=None, transport_handler=HttpTransport(),
                         sample_rate=100, zipkin_attrs=None, max_span_batch_size=None, annotations=None,
                         add_logging_annotation=False, report_root_timestamp=False, use_128bit_trace_id=False,
                         host=None, context_stack=None, firehose_handler=None):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            z_attrs = ThreadLocalStack().get()
            if z_attrs is None:
                with zipkin_span(
                        service_name=service_name,
                        span_name=span_name,
                        transport_handler=transport_handler,
                        port=port,
                        sample_rate=sample_rate,
                        binary_annotations=binary_annotations,
                        zipkin_attrs=zipkin_attrs,
                        max_span_batch_size=max_span_batch_size,
                        annotations=annotations,
                        add_logging_annotation=add_logging_annotation,
                        report_root_timestamp=report_root_timestamp,
                        use_128bit_trace_id=use_128bit_trace_id,
                        host=host,
                        context_stack=context_stack,
                        firehose_handler=firehose_handler
                ):
                    result = function(*args, **kwargs)
                    return result
            else:
                with zipkin_span(
                        service_name=service_name,
                        span_name=span_name,
                        binary_annotations=binary_annotations,
                        zipkin_attrs=zipkin_attrs,
                        max_span_batch_size=max_span_batch_size,
                        annotations=annotations,
                        add_logging_annotation=add_logging_annotation,
                        report_root_timestamp=report_root_timestamp,
                        use_128bit_trace_id=use_128bit_trace_id,
                        host=host,
                        context_stack=context_stack,
                        firehose_handler=firehose_handler):
                    result = function(*args, **kwargs)
                    return result
        return wrapper
    return real_decorator
