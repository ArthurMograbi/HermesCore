import matplotlib.pyplot as plt
import pandas as pd
import json
import pytz


f = open("sentmessages.txt",'r',encoding='utf8')
txt = f.read()

f.close()

ol = txt.split("{\"_data")


nol = ["{\"_data"+i for i in ol[1:]] #skip the first cuz its empty

jl = [json.loads(i) for i in nol]



def plot_time(l):
    timestamps = [d['_data']['t'] for d in l]
    bodies = [d['body'] for d in l]

    # Convert timestamps to datetime objects and convert to Brazil time
    timestamps = [pd.Timestamp(t, unit='s', tz='UTC').tz_convert('America/Sao_Paulo') for t in timestamps]

    # Create a pandas DataFrame with the timestamps and message bodies
    df = pd.DataFrame({'timestamp': timestamps, 'body': bodies})

    # Set the timestamp column as the index of the DataFrame
    df = df.set_index('timestamp')

    print(df)


    # Resample the DataFrame by hour and count the number of messages per hour, with a rolling window of 24 hours
    df_resampled = df.resample('H').count().rolling(window=12).sum()

    # Plot the time series graph
    plt.plot(df_resampled.index, df_resampled['body'])

    #return df_resampled

    plt.xlabel('Horário') 
    plt.ylabel('Mensagens')
    plt.show()





a = [i for i in jl if i['ack']==1]

b = [i for i in jl if i['ack']==0]

print(f'{len(jl)} messages sent with {len(a)} errors and {len(b)} sucesses! ({len(b)/(len(a)+len(b))}%)')



c =plot_time(b)

plt.pie([len(b),len(a)],labels=[f'Sucessos ({len(b)})',f'Erros ({len(a)})'])

plt.show()


import matplotlib.animation as animation

labels = [f'Sucessos ({len(b)})', f'Erros ({len(a)})']
sizes = [len(b), len(a)]

pcts = [s/sum(sizes) for s in sizes]

# Define the parameters for the animation
frames = 50
start_angle_range = (-180, 0)  # range of starting angles to animate
explode_range = (0, 0.2)  # range of explode values to animate

# Define the figure and the initial pie chart
# Define the figure and the initial pie chart
fig, ax = plt.subplots()
pie = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=start_angle_range[0])

from math import pi,sin

ax.set_aspect('equal')

#pie[0][0].set_width(pcts[0]*360)
#pie[0][1].set_width(pcts[1]*360)
tF = 1

def init():
    pie[0][0].animated = True
    pie[0][1].animated = True

# Define the update function for the animation
def update(frame):
    # Calculate the current starting angle and explode values based on the current frame
    r = 1 + 0.1*sin(2*pi*tF*frame/frames)
    pie[0][1].set(radius=r)
    # Update the pie chart with the current starting angle and explode values
    #pie[0][0].set_theta1(start_angle)
    #pie[0][0].set_theta2(start_angle+pcts[0]*360)
    #pie[0][1].set_theta1(start_angle+pcts[0]*360)
    #pie[0][1].set_theta2(start_angle+360)
    #pie[0][1].set_explode(explode)
    
    # Return the updated pie chart
    #return pie[0]

# Create the animation and save it to a video file
ani = animation.FuncAnimation(fig, update, frames=frames,init_func=init)
ani.save('pie_chart_animation.gif', fps=30)
