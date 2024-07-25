# import json
from flask import json, redirect, render_template, request, url_for
from stiffness import app

from stiffness.services import calcul_stiffness, interpolation

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/new-page')
# def new_page():
#     return '''
#         <h1>New Page</h1>
#         <p>This is the new page.</p>
#         <p><a href="/">Go back to home page</a></p>
    # '''

@app.route('/stiffness')
def stiffness():
    # page_id = request.args.get('page_id')
    datacalc = request.args.get('datacalc')
    if datacalc:
        datacalc = json.loads(datacalc)
    return render_template('index.html',page_html='stiffness', datacalc=datacalc)

@app.route('/dashboard')
def dashboard():
    chart_data = interpolation.get_interpolation_data()
    return render_template('index.html', page_html='dashboard', chart_data=chart_data)


@app.route('/handle_data', methods=['POST']) 
def handle_data():
    data_j = calcul_stiffness.stiffness_calculation(request.form['soilDensity'],request.form['watertable'],                       
                            float(request.form['pipeOutside']), float(request.form['depth']),
                            float(request.form['pipeCoating']), float(request.form['phi']),float(request.form['gamma']))
    # return render_template('index.html', page_html='stiffness', datacalc=calc)
     # Encode the dictionary as a JSON string
    calc_json = json.dumps(data_j)
    return redirect(url_for('stiffness', page_id='stiffness', datacalc=calc_json))

