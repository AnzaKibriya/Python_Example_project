# Integration Test Overview


#### Setup and use:
* recommended use through pycharm
* can also run through the commandline:
    ```
    behave <feature-file name>
    ```

#### General best practices:
* cover success scenarios first

#### Process of writing a test
1. Feature file calls step class (it knows which is needed by name)
1. Step class calls page class
1. Page class calls base page (specific wrapper on selenium scripts)


#### Feature File Best Practices
* try to create steps that have multiple actions (makes step file shorter)
    * you can have a feature file step call a single function in the page class that will call other lower level functions
* `Scenario` for a single scenario and `Scenario Outline` if you are doing the test with multiple pieces of example data


#### Selector use strategy:
When building selectors, priority:
* specific data tag/id that will not change
* relative xpath


#### Page class strategies
* Try to create unit step methods (smaller ones)
* Then you can combine these unit steps into higher level steps that call these methods (this is better for abstration) 


#### Environment.py
* Configuration of the framework itself-- basically general lifecycle methods for your test
* Linear Execution (would be first running in Chrome/Firefox) - unsure if it's supported (same with parallel execution)


#### Installing Allure Report
* `allure-behave` plugin needed for Jenkins

#### Regression Testing Tools 
* ghostinspector
* ParrotQA