# se-workshop-project

Commerce System project in the 'SE Workshop' course

## Set up

1. make sure you have python at least 3.7 and node.js installed on your computer.
2. make sure you are in the project main directory `se-workshop-project`
   and install the required python dependencies with `pip install -r requirements.txt`
3. cd into the gui folder [commerce_system_gui](./commerce_system_gui) and install node modules:
    ```shell
    cd commerce_system_gui
    npm install
    ```
4. after all installation are finished you are ready to run the project.

## Running

1. run the backend by running [run.py](./run.py) with two optional arguments
    - configuration file path
    - initialization file path

   both will be discussed later.
   ```shell
   python run.py ./input-config.json ./init.json
   ```
    ```shell
    usage: run.py [-h] [-c CONFIG] [-i INIT]
    
    Commerce System
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            configuration file path for the system
      -i INIT, --init INIT  initialization file for the system
    
    ```
2. run the frontend (GUI) by cd into the gui folder and running `npm start`
    ```shell
   cd commerce_system_gui
   npm start
    ```
3. a tab in your browser will be opened on `localhost:3000` (if it doesn't then do it yourself).

## Configuration File

When running the system some of its attributes such as external systems, database connection admin credentials, etc. are
determined by the configuration file. There is a default configuration stored in
[config](./config/config.py). to override or add additional options write your own configuration file and pass its path
to the [run.py](./run.py) script.
<br/>
The configuration file is a json file with the following fields, where all fields are optional. you can find an example
in [input-config.json](./input-config.json) or follow the following template. (your config file doesn't have to contain
all the fields mentioned below)

```json
{
  "payment_system_url": "<url>",
  "delivery_system_url": "<url>",
  "payment_facade": "<facade-type>",
  "delivery_facade": "<facade-type>",
  "database_url": "<db-string>",
  "database_credentials": {
    "username": "<db-username>",
    "password": "<db-password>"
  },
  "admin_credentials": {
    "username": "<admin-username>",
    "password": "<admin-password>"
  },
  "certificate_path": {
    "cert": "<cert-path>",
    "key": "<key-path>"
  },
  "port": "<server-port>",
  "ws_port": "<web-socket-port>"
}
```

## Initialization File

The initialization file describes a series of actions to be executed when the system goes up. The initialization file is
a json file in the following format

```json
{
  "users": [
    <user-id-1>,
    <user-id-2>,
    ...
  ],
  "actions": [
    <action-1>,
    <action-2>,
    <action-3>,
    ...
  ]
}
```

1. `users`: the users list is used to declare ids for the users that will be executing the actions in the `actions`
   list. later we will see that each action has a `user` key which declares which user is the one performing the action.
2. `actions`: the actions list describes action to be performed in the order they are written each action is in the
   following format.
    ```json
    {
      "user": "<id-of-user-performing-action>",
      "action": "<service-function-name>",
      "params": {
        "<param-name>": "<param-value>"
      }
    }
    ```

sometimes we would like to use return values of one action as a param value of another action. in this case we can use
refs. the following examples illustrates refs:

```json
[
  {
    "action": "open_shop",
    "user": "u1",
    "params": {
      "shop_name": "shop1",
      "description": "the one and only shop in the entire commerce system"
    },
    "ref_id": "s1"
  },
  {
    "action": "add_product_to_shop",
    "user": 1,
    "params": {
      "shop_id": {
        "ref": "s1"
      },
      "product_name": "Bamba",
      "description": "Its Osem",
      "categories": [
        "snacks"
      ],
      "price": 30,
      "quantity": 20
    },
    "ref_id": "p1"
  }
]
```

when an action has a `ref_id`, the return value of the action is bound to the given `ref_id`. for example the return
value of the `open_shop` (a shop id) will be bound to the key `s1`, which we can later use by using the ref dictionary,
as in the `add_product_to_shop_action`.

for a full example look at the example [init file](./init.json).

There is also a convenient and safer way for creating the initialization files through python by using the 
[init_generator](./init_generator.py) module. a usage example is in [init_1](./init_1.py)

## Testing Framework

All Tests (acceptance, integration and unit) will all be written using the
[unittest](https://docs.python.org/3/library/unittest.html) framework

### Acceptance Testing

The system has a well-defined interface in the `service` package through which the acceptance tests are accessing the
system functions. since the acceptance tests are written independently of the development of the system we define a
proxy for the earlier mentioned system facade which acts as a dummy as long as the system is not ready.
<br/>

- #### Running Acceptance Tests
  Run the [acceptance tests module](./acceptance_tests/acceptance_tests.py) preferably through an IDE such as pycharm

### Unit and Integration Testing

- Every component in the [domain](./domain) will contain a `tests` folder which will contain all unit tests for the
  component. testing each class/module separately.
- each test file should begin with the word `test` so we can run an entire directory of tests.
  (this is for the unittest package to identify test files in a directory)
- Please use [mocks](https://docs.python.org/3/library/unittest.mock.html) for other classes when unit testing classes.
  use mocks for other components when making integration testing.
