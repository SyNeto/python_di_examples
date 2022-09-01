# Dependecy injection

This repo intends to be a series of examples of how to implement Dependency injection with various examples.


## [example 01](/example_01/)

This example shows how to decouple an example application, on the [main_before.py](/example_01/main_before.py) file you can see how the app is
structured with coupled dependencies.

The second file in this example ([main_di.py](/example_01/main_di.py)) shows how to decouple the dependencies from
the first example and increment the cohesion preparing our sample application to implement a dependency injector.

## example 02

This example shows how to implement a dependency injector.

First we declare a container that will be provide help with the objects asselmbly to be injected

This example also shows how to override dependencies, note that you can override a provider with another provider