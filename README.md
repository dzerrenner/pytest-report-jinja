pytest-report-jinja
===================

This pytest plugin uses the Jinja2 template engine to produce HTML reports. 
You'll have to provide your own templates, but it should be easy to create them.

## Usage

After installing the plugin into your test env, it adds two additional command line options to pytest:
* ``--jinja2-template`` filename of the jinja2 template to use
* ``--jinja2-output`` output filename

You can use relative or absolute paths for both of them. 

You are not bound to a single file for your template, 
it is possible to use the full Jinja2 functionality
including temlpate inheritance etc. This means, if you
have some kind of base template which fits to your project,
just use it.

The plugin provides the following context variables to the templete:

| Name | Description |
| ---- | ----------- |
| ``items`` | list of all test which ran during the testrun | 
| ``metadata`` | some additional information, including data provided by the ``pytest-metadata`` plugin if installed| 
| ``testrun`` | information about the testrun itself, such as start time and duration|

The ``items`` element is an ``OrderedDict`` (order of execution), which keys are the Node-Ids (Tests) and values are the ``report`` objects (startup, execution and teardown) of that test.


