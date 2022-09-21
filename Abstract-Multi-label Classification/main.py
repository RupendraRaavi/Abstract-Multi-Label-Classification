### Integrate HTML With Flask
### HTTP verb GET And POST

##Jinja2 template engine
'''
{%...%} conditions,for loops
{{    }} expressions to print output
{#....#} this is for comments
'''

import pickle
from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

model = pickle.load(open('Research_abstract.pkl', 'rb'))

@app.route('/')
def welcome():
    return render_template('index.html')
      


### Result checker submit html page
@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        abstract=request.form['science']

        abstract_list = para_sentences(abstract)

        prediction = model.predict(abstract_list)
        final = output(prediction,abstract_list)

    return render_template('extend.html', output = final, mylist = 'This is my list {}'.format(abstract_list))




def para_sentences(para):
    my_list = []
    a = str(len(para))[0:2] + '00'
    b = int(a)
    count = 0
    i = 1
    while i <len(para):
        if i == b:
            my_list.append(para[b:])
        
        elif i % 100 == 0:
            print('count:',count)
            f = para[count:i]
            my_list.append(f)
            count = i 
           
            #print('my_list:',my_list, 'i:', i, 'count:',count )
            
        i+=1
    return my_list

def output(my_pred,values):

    my_dict = {'Results':[], 'Conclusion':[], 'Methods':[], 'Background':[], 'Objective':[]}

    for i, m in enumerate(my_pred):

        if m == 0:

            my_dict['Background'].append(values[i])

        elif m == 1:

            my_dict['Conclusion'] .append(values[i])

        elif m == 2:

            my_dict['Methods'] .append(values[i])

        elif m == 3:

            my_dict['Objective'].append(values[i])

        elif m == 4:

            my_dict['Results'] .append(values[i])

    my_dict['Results'] = ' '.join(my_dict['Results'])

    my_dict['Background'] = ' '.join(my_dict['Background'])

    my_dict['Conclusion'] = ' '.join(my_dict['Conclusion'])

    my_dict['Objective'] = ' '.join(my_dict['Objective'])

    my_dict['Methods'] = ' '.join(my_dict['Methods'])
    
    
    return my_dict


    



if __name__=='__main__':
    app.run(debug=True)