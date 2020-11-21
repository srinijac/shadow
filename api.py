from flask import Flask, request, render_template,jsonify

app = Flask(__name__)

def do_something(name,handle):
   name = name.upper()
   handle = handle.upper()
   combine = name + handle
   return combine

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    name = request.form['name']
    word = request.args.get('name')
    handle = request.form['handle']
    combine = do_something(name,handle)
    result = {
        "output": combine
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)

