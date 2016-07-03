Testing Guide
=============
For PhoenixNow, we use py.test for testing. To run tests, just enter in 

.. code-block:: shell
    
    $ py.test

What we'll do is go through testing a simple Flask app in the recommended way
that this project uses.

Example Test
-----------------
All tests go in the ``tests/`` folder and have ``test_`` prepended to the file name and
to the function inside the ``test_TESTNAME.py`` file, so that pytest can see and
execute it.

When we decide to write some new code or change a feature, we use a test first.
Then we write the most basic code that makes the test pass and then revise the
code to be more efficient.

Here's an example test. I named mine ``test_hello.py``

.. code-block:: python

    import pytest
    import PhoenixNow

    @pytest.fixture
    def app():
        return PhoenixNow.app.test_client()

    def test_hello(app):
        rv = app.get('/')
        assert b"hello" in rv.data

``pytest.fixture`` is a decorator that you put above a function that usually sets
up the environment for a test. The function can be passed to a test that has the
function name as an argument.

``rv = app.get('/')`` uses the ``test_client()`` function from the ``flask`` library
to make a test request to ``/``.

We use ``assert`` to assert that ``hello`` is in the data returned from the test
request. A ``b`` is put in front of the string to match the format of
``rv.data``,
which is also binary.

If you run this (with py.test in the commandline), you should get:

.. code-block:: shell

    nicholas@mercury:~/src/PhoenixNownicholas ~/src/PhoenixNow ]$ py.test
    =================================================== test session starts ===================================================
    platform linux -- Python 3.5.1, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
    rootdir: /home/nicholas/src/PhoenixNow, inifile: 
    plugins: cov-2.2.1, xdist-1.14

    collected 1 items 

    tests/test_hello.py E

    ========================================================= ERRORS ==========================================================
    ______________________________________________ ERROR at setup of test_hello _______________________________________________

        @pytest.fixture
        def app():
    >       return PhoenixNow.app.test_client()
    E       AttributeError: module 'PhoenixNow' has no attribute 'app'

    tests/test_hello.py:6: AttributeError

    ================================================= 1 error in 0.02 seconds =================================================

Example Flask App
-----------------

All this means is that we have no code in the PhoenixNow module, so let's make
the ``__init__.py`` file and paste this into it:

.. code-block:: python

    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "hello"

This code basically means, when something requests ``/`` on the webpage, it
returns ``"hello"`` as the data in the request sent.

Now when we run ``py.test``, we should see that all tests have passed:

.. code-block:: shell

    nicholas@mercury:~/src/PhoenixNownicholas ~/src/PhoenixNow ]$ py.test
    =================================================== test session starts ===================================================
    platform linux -- Python 3.5.1, pytest-2.9.2, py-1.4.31, pluggy-0.3.1
    rootdir: /home/nicholas/src/PhoenixNow, inifile: 
    plugins: cov-2.2.1, xdist-1.14

    collected 1 items 

    tests/test_hello.py .

    ================================================ 1 passed in 0.12 seconds =================================================

    nicholas@mercury:~/src/PhoenixNownicholas ~/src/PhoenixNow ]$ exit

Refactoring
-----------

Since our code is very simple, we don't have to refine the code, but we would
rewrite the code to be better and more efficient after passing the test.
