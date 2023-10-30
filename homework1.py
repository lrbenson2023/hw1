import math
from flask import Flask, render_template, request, make_response, jsonify
app = Flask(__name__)
@app.route('/')

def in2cm():
	return render_template('inch2cm.html')

@app.route('/inch2cm_action')
def inch2cm_action():
	inches = request.args.get("inches")
	cm = float(inches) * 2.54
	return str(inches) + " inches = " + str(cm) + " cm"

@app.route('/feet2m')
def ft2m():
	return render_template('feet2m.html')

@app.route('/feet2m_action')
def feet2m_action():
	feet = request.args.get("feet")
	m = float(feet) * 0.3048
	return str(feet) + " feet = " + str(m) + " m"

@app.route('/miles2km')
def miles2km():
	return render_template('miles2km.html')

@app.route('/miles2km_action')
def miles2km_action():
	miles = request.args.get("miles")
	km = float(miles) * 1.60934
	return str(miles) + " miles = " + str(km) + " km"

@app.route('/factorial')
def factorial():
	return render_template('factorial.html')

@app.route('/factorial_action')
def factorial_action():
	num = int(request.args.get("num"))
	fac = 1
 
	for i in range(1, num + 1):
		fac = fac * i
	return "The factorial of " + str(num) + " = " + str(fac)

usestat2 = 0
@app.route('/statapp1')
def statapp():
	global usestat2
	usestat2 = 0
	return render_template('statapp.html')

@app.route('/statapp_action')
def statapp_action():
	
	#get the data 
	input_line = request.args.get("input_line")
	scores=input_line.split(",")
	for i in range(len(scores)):
 		scores[i]=int(scores[i])
	
	#calculate statistics
	mean = sum(scores) / len(scores)
	res = sum((x - mean) ** 2 for x in scores) / len(scores)
	sd = math.sqrt(res)

	#calculate the median
	if usestat2 == 1:
		no = len(scores)
		scores.sort()
		if no % 2 == 0:
		    median1 = scores[no//2]
		    median2 = scores[no//2 - 1]
		    median = (median1 + median2)/2
		else:
		    median = scores[no//2]

		response = make_response("The input data: " + input_line + \
		"\n\nThe mean of list is : " + str(mean) + \
		"\nThe variance of list is : " + str(res) + \
		"\nThe sd of list is : " + str(sd) + \
		"\nThe median of the list is " + str(median))
	
	#create the histogram
	elif usestat2 == 2:
		plot_response = horizontal_histogram(scores,0,100,10)

		result_string = "\n".join(str(element) for element in plot_response)
		response = make_response("The input data: " + input_line + \
		"\n\nThe mean of list is : " + str(mean) + \
		"\nThe variance of list is : " + str(res) + \
		"\nThe sd of list is : " + str(sd) + "\n\nHistogram:\n" + result_string)
		
	else:
		response = make_response("The input data: " + input_line + \
		"\n\nThe mean of list is : " + str(mean) + \
		"\nThe variance of list is : " + str(res) + \
		"\nThe sd of list is : " + str(sd))
	
	response.mimetype = "text/plain"
	return response
	
@app.route('/statapp2')
def statapp2():
	global usestat2
	usestat2 = 1
	return render_template('statapp.html')

# method horizontal_histogram draws a histogram according to scores, with bounds from lb to ub
@app.route('/statapp3')
def statapp3():
	global usestat2
	usestat2 = 2
	return render_template('statapp.html')

def horizontal_histogram(scores,lb,ub,inc):
	from io import StringIO
	import sys

	buffer = StringIO()
	sys.stdout = buffer

	scores.sort()
	hist = []

	j = 0
	i = lb
	while (i <= ub):
	    count = 0
	    while (j < len(scores) and scores[j] >= i and scores[j] < i+inc):
	      count=count+1
	      j=j+1
	    print('{0:3}'.format(i),"*"*count)
	    print_output = buffer.getvalue()
	    i=i+inc
	hist.append(print_output)
	# restore stdout to default for print()
	sys.stdout = sys.__stdout__
		
	return hist
	
if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)

