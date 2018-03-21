import json
import pytest

import os
from collections import OrderedDict
from datetime import datetime


def pytest_addoption(parser):
    group = parser.getgroup('reporting')
    group.addoption('--jinja2-template', action='store', dest='jinja2_template',
                    metavar='path', default=None,
                    help='location of the report template.')
    group.addoption('--jinja2-output', action='store', dest='jinja2_output',
                    metavar='path', default=None,
                    help='filename of the report output.')

def pytest_configure(config):
    templatepath = config.option.jinja2_template
    # TODO- check if the template exists at configure time
    outputpath = config.option.jinja2_output
    # prevent opening htmlpath on slave nodes (xdist)
    if templatepath and not hasattr(config, 'slaveinput'):
        config._jinjareport = JinjaReport(templatepath, outputpath, config)
        config.pluginmanager.register(config._jinjareport)

def pytest_unconfigure(config):
    jinjareport = getattr(config, '_jinjareport', None)
    if jinjareport:
        del config._jinjareport
        config.pluginmanager.unregister(jinjareport)


class JinjaReport(object):
    def __init__(self, template, outputpath, config):
        outputpath = os.path.expanduser(os.path.expandvars(outputpath))
        self.outputpath = os.path.abspath(outputpath)
        templatepath = os.path.expanduser(os.path.expandvars(template))
        self.templatepath = os.path.abspath(templatepath)
        self.config = config
        self.errors = self.failed = 0
        self.passed = self.skipped = 0
        self.xfailed = self.xpassed = 0
        has_rerun = config.pluginmanager.hasplugin('rerunfailures')
        self.rerun = 0 if has_rerun else None
        self.items = OrderedDict()
        self.testrun_info = {}

    def _metadata(self, session):
        mapping = {
            "_metadata": "metadata"
        }

        _meta = {}
        for elem in ["args", "_metadata", "env"]:
            if hasattr(session.config, elem):
                key = mapping.get(elem, elem)
                _meta[key] = getattr(session.config, elem)
        return _meta

    def pytest_runtest_logreport(self, report):
        if report.passed:
            if report.when == "call":
                if hasattr(report, "wasxfail"):
                    report.state = "xpassed"
                    self.xpassed += 1
                else:
                    report.state = "passed"
                    self.passed += 1
            else:
                report.state = "passed"
        elif report.failed:
            if report.when == "call":
                if hasattr(report, "wasxfail"):
                    report.state = "xpassed"  # pytest < 3.0 marked xpasses as failures
                    self.xpassed += 1
                else:
                    report.state = "failed"
                    self.failed += 1
            else:
                report.state = "error"
                self.errors += 1
        elif report.skipped:
            if hasattr(report, "wasxfail"):
                report.state = "xfailed"
                self.xfailed += 1
            else:
                report.state = "skipped"
                self.skipped += 1
        else:
            report.state = "rerun"
            self.rerun += 1

        if report.nodeid not in self.items:
            self.items[report.nodeid] = []
        self.items[report.nodeid].append(report)

    def pytest_sessionstart(self, session):
        self.start_time = datetime.now()
        self.testrun_info["Start"] = self.start_time

    def pytest_sessionfinish(self, session):
        self.duration = datetime.now() - self.start_time
        self.testrun_info["Duration"] = self.duration.total_seconds()

        # render only if there was a test run
        if not self.config.option.collectonly:

            dir_name = os.path.dirname(self.outputpath)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            #debug
            # from pprint import pprint
            # pprint(self._metadata(session))

            # render template
            import jinja2
            jinja = jinja2.Environment(
                loader=jinja2.FileSystemLoader(os.path.dirname(self.templatepath)),
                # autoescape=select_autoescape(['html', 'xml'])
            )
            template = jinja.get_template(os.path.basename(self.templatepath))
            rendered_content = template.render(items=self.items, metadata=self._metadata(session), testrun=self.testrun_info)

            with open(self.outputpath, "w", encoding="utf-8") as of:
                of.write(rendered_content)

    def pytest_terminal_summary(self, terminalreporter):
        if not self.config.option.collectonly:
            terminalreporter.write_sep('-', f"generated report file: {self.outputpath}")
