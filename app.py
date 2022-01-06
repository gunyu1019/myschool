import app

_app = app.create_app()
_app.run(host="0.0.0.0", port=4012, debug=True)
