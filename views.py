from flask import Flask
from flask import Flask, request, render_template, make_response
import re
import numpy.polynomial.polynomial as P
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import StringIO

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",title='home')

@app.route('/about_us')
def profile():
  return render_template("about_us.html",title='about us')

@app.route('/akash')
def akash():
   return render_template("akash.html",title='akash')

@app.route('/ishank')
def ishank():
   return render_template("ishank.html",title='ishank')

@app.route('/shiv')
def shiv():
    return render_template("shivendra.html",title='shivendra')


@app.route("/average", methods=['GET', 'POST'])
def calculation():
    rest = 0.0
    if request.method=='POST':
        first = request.form['first']
        exp=r"[0-9.]*"
        val=re.findall(exp,first)
        l=[]
        for i in val:
            if(i!=''):
                l.append(float(i))

        rest=(sum(l)/(len(l)))

    return render_template('mean.html',result=rest)


@app.route('/plot',methods=['GET','POST'])
def hello_world():
    if request.method=='GET':
        return render_template('get.html')
    elif request.method=='POST':
        points=request.form['points']
        return render_template('post.html',source='/plot/'+points,old_points=points)
    else:
        return 'Invalid Request'


@app.route('/plot/<points>')
def plot(points):

    s,X,F=points[:],[],[]
    while(s!=''):
        i=s.index('(')
        j=s.index(',',i)
        X.append(float(s[i+1:j]))
        k=s.index(')',j)
        F.append(float(s[j+1:k]))
        s=s[k+2:]

    fig=plt.figure()
    plt.clf()
    sub=fig.add_subplot(111)
    X1=np.arange(min(X)-2,max(X)+2,0.1)
    num_plots=len(X)
    colormap = plt.cm.gist_ncar
    plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0.2, 0.9, num_plots)])
    x=[1.0]
    for i in range(len(X)):
        x=P.polymul(x,[-1*X[i],1])
    b=[0.0]
    for i in range(len(X)):
        a=P.polydiv(x,[-1*X[i],1])
        b=P.polyadd(P.polymul((P.polydiv(a[0],P.polyval(X[i],a[0])))[0],[F[i]]),b)
        Y=P.polyval(X1,P.polymul((P.polydiv(a[0],P.polyval(X[i],a[0])))[0],[F[i]]))
        sub.plot(X1,Y)

    Y=P.polyval(X1,b)
    Y1=P.polyval(np.arange(min(X),max(X)+0.1,0.1),b)
    interpol_obj=sub.plot(X1,Y,'k',linewidth=2)
    sub.plot(X,F,'ro',markersize=8)

    plt.grid(True)
    fig.legend(interpol_obj,['Interpolating Polynomial'],fancybox=True,shadow=True,loc='upper left')
    plt.axis([min(X)-3,max(X)+3,min(Y1)-2,max(Y1)+2])
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.title('Interpolate')
    #plt.show()

    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


@app.route('/algo')
def algo():
    return render_template("algo.html",title='algo')


if __name__ == '__main__':
    app.run(debug=True)
