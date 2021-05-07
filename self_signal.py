import django.dispatch
my_signal = django.dispatch.Signal(providing_args=["argument1", "argument2"])

