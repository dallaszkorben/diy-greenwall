#! /usr/bin/python3

import flask

print(__name__)

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/config', methods=['GET'])
def home():
    return """
{
  'sensors': [
    {
      'id': '1',
      'name': 'lamp',
      'type': 'integer',
      'min': 0,
      'max': 100,
      'actual': 25
    }
  ],
  'actuators': [
  ]
}"""


app.run()

