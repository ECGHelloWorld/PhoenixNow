Running
=======

To run this program, you have to use the builtin `flask run` command. To use the
`flask run` command, we have to run this first: 

.. code-block:: shell

    export FLASK_APP=run.py
    
This is so that the `flask run` command will know where the program is to run it. 

After we run that, we can finally run the program:

.. code-block:: shell
    
    flask run

In our `run.py` file we have:

.. code-block:: python

    from PhoenixNow.config import ProductionConfig
    from PhoenixNow import create_app

    app = create_app(ProductionConfig)

This pulls from `__init__.py`, so let's see what's in there:

.. code-block:: python

    from flask import Flask

    def create_app(config_object):
        """
        Sets up a Flask app variable based on a config object -- see config.py. We
        do this so that we can use `flask run` and integrate into things like uwsgi
        better and testing. 
        """

        app = Flask(__name__)
        app.config.from_object(config_object)

        from PhoenixNow.model import db
        db.init_app(app)

        from PhoenixNow.views import regular
        app.register_blueprint(regular)
        
        return app

All this does is make testing and running Flask under different servers easier.
When you call the function `create_app`, it returns an `app` variable that
initializes Flask and the related libraries.

You'll notice that we're using blueprints instead of regular views. We do this
so that we can use a `create_app` function.
