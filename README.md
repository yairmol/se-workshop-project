# se-workshop-project
project in the 'SE Workshop' course

## Testing Framework
All Tests (acceptance, integration and unit) will all be written using the 
[unittest](https://docs.python.org/3/library/unittest.html) framework 
### Acceptance Testing
The system has a well-defined interface in the `service` package
through which the acceptance tests are accessing the system functions.
since the acceptance tests are written independently of the development of the system
we define a proxy for the earlier mentioned system facade which acts as a dummy as long as the system is not ready.
<br/>
 - #### Running Acceptance Tests
    1. when the system is ready, do to the [facade proxy module](./acceptance_tests/facade_proxy.py) and change the 
       function the `real` field to be the real system facade.
    2. Run the [acceptance tests module](./acceptance_tests/acceptence_tests.py) preferably through an IDE 
       such as pycharm

### Unit and Integration Testing
 - Every component in the [domain](./domain) will contain a `tests` folder which will contain all unit tests for
   the component. testing each class/module separately.
 - Please use [mocks](https://docs.python.org/3/library/unittest.mock.html) for other classes when unit testing classes.
   use mocks for other components when making integration testing.
