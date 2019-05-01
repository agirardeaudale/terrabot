.. highlight:: shell

============
Contributing
============

Reporting Bugs
--------------

Report bugs at https://github.com/agirardeaudale/terrabot/issues.

When reporting a bug please include:

* Detailed steps to reproduce the bug.
* Any details about your local setup that might be helpful in troubleshooting.

Development
-----------

1. Clone the repo locally::

    $ git clone git@github.com:agirardeaudale/terrabot.git

2. Make a virtualenv. With virtualenvwrapper::

    $ mkvirtualenv terrabot
    $ cd terrabot/
    $ python setup.py develop

3. Create a local git branch

4. Check flake8 and tests::

    $ flake8 terrabot tests
    $ python setup.py test or py.test
    $ tox

5. Commit changes and push to GitHub::

    $ git add .
    $ git commit -m "<description>"
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request on GitHub.

Deploying to PyPI
-----------------

$ bumpversion patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.

Tips
----

To run a subset of tests::

$ py.test tests.test_sim
