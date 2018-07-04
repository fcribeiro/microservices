from py_zipkin.util import generate_random_64bit_string
from py_zipkin.zipkin import zipkin_span, ZipkinAttrs
from py_zipkin.stack import ThreadLocalStack
from tracing.kafka_transport import KafkaTransport
from flask import request


def emp_zipkin_decorator(service_name, span_name, port, binary_annotations=None, transport_handler=KafkaTransport(),
                         sample_rate=100, zipkin_attrs=None, max_span_batch_size=None, annotations=None,
                         add_logging_annotation=False, report_root_timestamp=False, use_128bit_trace_id=False,
                         host=None, context_stack=None, firehose_handler=None):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            z_attrs = ThreadLocalStack().get()
            if z_attrs is None:
                headers = request.headers
                if headers.__contains__('X-B3-Traceid'):
                    trace_id = request.headers['X-B3-Traceid']
                    parent_id = request.headers['X-B3-Parentspanid']
                    attrs = ZipkinAttrs(
                        trace_id=trace_id,
                        parent_span_id=parent_id,
                        span_id=generate_random_64bit_string(),
                        flags=0,
                        is_sampled=True,
                    )
                    with zipkin_span(
                            service_name=service_name,
                            span_name=span_name,
                            transport_handler=transport_handler,
                            port=port,
                            binary_annotations=binary_annotations,
                            zipkin_attrs=attrs,
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
                else:
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
                        transport_handler=transport_handler,
                        port=port,
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
