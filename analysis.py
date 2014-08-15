import numpy as np
import os
from psychopy import data
import matplotlib.pyplot as plt
import csv
import xlrd

filenameRoot='_2013_Feb_22_1431'
if not os.path.isdir('data/Processed Data (Test)/'+filenameRoot):
    os.makedirs('data/Processed Data (Test)/'+filenameRoot) #if this fails (e.g. permissions) we will get error
D = data.importConditions('data/' + filenameRoot + '.csv')

#all trials graph
trnum = []
FD = []
incorrects = {'6':{'trnum':[], 'FD': []},'12':{'trnum':[], 'FD':[]}}
corrects = {'6':{'trnum':[], 'FD': []},'12':{'trnum':[], 'FD':[]}}
for i in D:
    trnum.append(i['TrialNumber'])
    FD.append(i['frame_displayed'])
    if i['correct_response']:
        corrects[str(i['duration'])]['trnum'].append(i['TrialNumber'])
        corrects[str(i['duration'])]['FD'].append(i['frame_displayed'])
    else:
        incorrects[str(i['duration'])]['trnum'].append(i['TrialNumber'])
        incorrects[str(i['duration'])]['FD'].append(i['frame_displayed'])
plt.figure(figsize=(10,6), dpi=100)
Fig1 = plt.subplot(111)
Fig1.plot(corrects['6']['trnum'],corrects['6']['FD'],'bo',label = '6s Correct')
Fig1.plot(corrects['12']['trnum'],corrects['12']['FD'],'go',label = '12s Correct')
Fig1.plot(incorrects['6']['trnum'],incorrects['6']['FD'],'bx',label = '6s Incorrect')
Fig1.plot(incorrects['12']['trnum'],incorrects['12']['FD'],'gx',label = '12s Incorrect')
Fig1.plot(trnum,FD,'k-',color = '0.5', label = '_nolegend_')
handles, labels = Fig1.get_legend_handles_labels()
display = (0,1,2,3)
#simArtist1 = plt.Line2D((0,1),(0,0), color='k', marker='o', linestyle='', label = 'Correct')
#simArtist2 = plt.Line2D((0,1),(0,0), color='k', marker='x', linestyle='', label = 'Incorrect')
#simArtist3 = plt.Line2D((0,1),(0,0), color='b', marker='D', linestyle='', label = '6s')
#simArtist4 = plt.Line2D((0,1),(0,0), color='g', marker='D', linestyle='', label = '12s')
box = Fig1.get_position()
Fig1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#Fig1.legend([handle for i,handle in enumerate(handles) if i in display]+[simArtist1, simArtist2, simArtist3, simArtist4], [label for i,label in enumerate(labels) if i in display]+['Correct', 'Incorrect', '6s','12s'], loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)
Fig1.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)
plt.xlabel('Trial Number')
plt.ylabel('Frame Displayed')
plt.title('All Trial Summary')
plt.axvline(x=8.5, ls='-.', color='0.5')
plt.axvline(x=24.5, ls='-.', color='0.5')
plt.axvline(x=40.5, ls='-.', color='0.5')
plt.axvline(x=56.5, ls='-.', color='0.5')
plt.ylim([0,63])
plt.xlim([0,74])
plt.savefig('data/Processed Data (Test)/'+filenameRoot+'/Trial_Summary.png')

ex1 = list(D)
for i in range(len(ex1))[::-1]:
	if ex1[i]['response_rate']<1 or ex1[i]['response_rate']>12 or ex1[i]['frame_displayed']<5 or ex1[i]['block']==0:
		del ex1[i]
pc_data = {'Half': {'H1':[],'H2':[]}, 'Exemplar': {'af1': [], 'af4': [], 'am1': [], 'am2': []}, 'Gender': {'F': [], 'M': []}, 'Block': {'B1': [], 'B2': [], 'B3': [], 'B4':[]}, 'Duration': {'6s': [], '12s': []}, 'Emotion': {'happy': [], 'sad': [], 'mad': [], 'scared': []}, 'Total':{'Total':[]}}
pc_vals = {'Half': {'H1':[],'H2':[]}, 'Exemplar': {'af1': [], 'af4': [], 'am1': [], 'am2': []}, 'Gender': {'F': [], 'M': []}, 'Block': {'B1': [], 'B2': [], 'B3': [], 'B4':[]}, 'Duration': {'6s': [], '12s': []}, 'Emotion': {'happy': [], 'sad': [], 'mad': [], 'scared': []}, 'Total':{'Total':[]}}
for i in range(len(ex1)):
	pc_data['Total']['Total'].append(ex1[i]['correct_response'])
	pc_data['Exemplar'][ex1[i]['exemplar']].append(ex1[i]['correct_response'])
	pc_data['Gender'][str(ex1[i]['Gender']).capitalize()].append(ex1[i]['correct_response'])
	pc_data['Block']['B' + str(ex1[i]['block'])].append(ex1[i]['correct_response'])
	pc_data['Duration'][str(ex1[i]['duration'])+'s'].append(ex1[i]['correct_response'])
	pc_data['Emotion'][''.join(list(ex1[i]['File_Extension'])[1::])].append(ex1[i]['correct_response'])

pc_data['Half']['H1'].extend(pc_data['Block']['B1'] + pc_data['Block']['B2'])
pc_data['Half']['H2'].extend(pc_data['Block']['B3'] + pc_data['Block']['B4'])

for dim in pc_data:
	for cat in pc_data[dim]:
		pc_vals[dim][cat]=100*np.mean(pc_data[dim][cat])

ex2 = list(ex1)
for i in range(len(ex2))[::-1]:
	if ex2[i]['correct_response']==0: 
		del ex2[i]
mfd_data = {'simple':{'Half': {'H1':[],'H2':[]}, 'Exemplar': {'af1': [], 'af4': [], 'am1': [], 'am2': []}, 
    'Gender': {'F': [], 'M': []}, 'Block': {'B1': [], 'B2': [], 'B3': [], 'B4':[]}, 'Duration': {'6s': [], '12s': []}, 
    'Emotion': {'happy': [], 'sad': [], 'mad': [], 'scared': []}, 'Total':{'Total':[]}}, 
    'complex': {'Duration_Block':{'6s_B1': [], '6s_B2': [], '6s_B3': [], '6s_B4': [], '12s_B1': [], '12s_B2': [], '12s_B3': [], '12s_B4': []}, 
    'Duration_Emotion':{'6s_happy': [], '6s_sad': [], '6s_mad': [], '6s_scared': [], 
    '12s_happy': [], '12s_sad': [], '12s_mad': [], '12s_scared': []}, 
    'Block_Emotion':{'B1_happy': [], 'B1_sad': [], 'B1_mad': [], 'B1_scared': [], 
    'B2_happy': [], 'B2_sad': [], 'B2_mad': [], 'B2_scared': [], 'B3_happy': [], 'B3_sad': [], 'B3_mad': [], 'B3_scared': [], 
    'B4_happy': [], 'B4_sad': [], 'B4_mad': [], 'B4_scared': []}, 
    'Block_Emotion_Duration': {'B1_happy_6s': [], 'B1_sad_6s': [], 'B1_mad_6s': [], 'B1_scared_6s': [], 
    'B2_happy_6s': [], 'B2_sad_6s': [], 'B2_mad_6s': [], 'B2_scared_6s': [], 
    'B3_happy_6s': [], 'B3_sad_6s': [], 'B3_mad_6s': [], 'B3_scared_6s': [], 
    'B4_happy_6s': [], 'B4_sad_6s': [], 'B4_mad_6s': [], 'B4_scared_6s': [], 
    'B1_happy_12s': [], 'B1_sad_12s': [], 'B1_mad_12s': [], 'B1_scared_12s': [], 
    'B2_happy_12s': [], 'B2_sad_12s': [], 'B2_mad_12s': [], 'B2_scared_12s': [], 
    'B3_happy_12s': [], 'B3_sad_12s': [], 'B3_mad_12s': [], 'B3_scared_12s': [], 
    'B4_happy_12s': [], 'B4_sad_12s': [], 'B4_mad_12s': [], 'B4_scared_12s': []},
    'Half_Emotion_Duration': {'H1_happy_6s': [], 'H1_sad_6s': [], 'H1_mad_6s': [], 'H1_scared_6s': [], 
    'H1_happy_12s': [], 'H1_sad_12s': [], 'H1_mad_12s': [], 'H1_scared_12s': [], 
    'H2_happy_6s': [], 'H2_sad_6s': [], 'H2_mad_6s': [], 'H2_scared_6s': [], 
    'H2_happy_12s': [], 'H2_sad_12s': [], 'H2_mad_12s': [], 'H2_scared_12s': []},
    'Half_Emotion': {'H1_happy': [], 'H1_sad': [], 'H1_mad': [], 'H1_scared': [], 
    'H2_happy': [], 'H2_sad': [], 'H2_mad': [], 'H2_scared': []},
    'Half_Duration':{'H1_6s':[],'H1_12s':[],'H2_6s':[],'H2_12s':[]}}}
mfd_vals = {'simple':{'Half': {'H1':[],'H2':[]}, 'Exemplar': {'af1': [], 'af4': [], 'am1': [], 'am2': []}, 
    'Gender': {'F': [], 'M': []}, 'Block': {'B1': [], 'B2': [], 'B3': [], 'B4':[]}, 'Duration': {'6s': [], '12s': []}, 
    'Emotion': {'happy': [], 'sad': [], 'mad': [], 'scared': []}, 'Total':{'Total':[]}}, 
    'complex': {'Duration_Block':{'6s_B1': [], '6s_B2': [], '6s_B3': [], '6s_B4': [], '12s_B1': [], '12s_B2': [], '12s_B3': [], '12s_B4': []}, 
    'Duration_Emotion':{'6s_happy': [], '6s_sad': [], '6s_mad': [], '6s_scared': [], 
    '12s_happy': [], '12s_sad': [], '12s_mad': [], '12s_scared': []}, 
    'Block_Emotion':{'B1_happy': [], 'B1_sad': [], 'B1_mad': [], 'B1_scared': [], 
    'B2_happy': [], 'B2_sad': [], 'B2_mad': [], 'B2_scared': [], 'B3_happy': [], 'B3_sad': [], 'B3_mad': [], 'B3_scared': [], 
    'B4_happy': [], 'B4_sad': [], 'B4_mad': [], 'B4_scared': []}, 
    'Block_Emotion_Duration': {'B1_happy_6s': [], 'B1_sad_6s': [], 'B1_mad_6s': [], 'B1_scared_6s': [], 
    'B2_happy_6s': [], 'B2_sad_6s': [], 'B2_mad_6s': [], 'B2_scared_6s': [], 
    'B3_happy_6s': [], 'B3_sad_6s': [], 'B3_mad_6s': [], 'B3_scared_6s': [], 
    'B4_happy_6s': [], 'B4_sad_6s': [], 'B4_mad_6s': [], 'B4_scared_6s': [], 
    'B1_happy_12s': [], 'B1_sad_12s': [], 'B1_mad_12s': [], 'B1_scared_12s': [], 
    'B2_happy_12s': [], 'B2_sad_12s': [], 'B2_mad_12s': [], 'B2_scared_12s': [], 
    'B3_happy_12s': [], 'B3_sad_12s': [], 'B3_mad_12s': [], 'B3_scared_12s': [], 
    'B4_happy_12s': [], 'B4_sad_12s': [], 'B4_mad_12s': [], 'B4_scared_12s': []},
    'Half_Emotion_Duration': {'H1_happy_6s': [], 'H1_sad_6s': [], 'H1_mad_6s': [], 'H1_scared_6s': [], 
    'H1_happy_12s': [], 'H1_sad_12s': [], 'H1_mad_12s': [], 'H1_scared_12s': [], 
    'H2_happy_6s': [], 'H2_sad_6s': [], 'H2_mad_6s': [], 'H2_scared_6s': [], 
    'H2_happy_12s': [], 'H2_sad_12s': [], 'H2_mad_12s': [], 'H2_scared_12s': []},
    'Half_Emotion': {'H1_happy': [], 'H1_sad': [], 'H1_mad': [], 'H1_scared': [], 
    'H2_happy': [], 'H2_sad': [], 'H2_mad': [], 'H2_scared': []},
    'Half_Duration':{'H1_6s':[],'H1_12s':[],'H2_6s':[],'H2_12s':[]}}}
for i in range(len(ex2)):
	mfd_data['simple']['Total']['Total'].append(ex2[i]['frame_displayed'])
	mfd_data['simple']['Exemplar'][ex2[i]['exemplar']].append(ex2[i]['frame_displayed'])
	mfd_data['simple']['Gender'][str(ex2[i]['Gender']).capitalize()].append(ex2[i]['frame_displayed'])
	mfd_data['simple']['Block']['B' + str(ex2[i]['block'])].append(ex2[i]['frame_displayed'])
	mfd_data['simple']['Duration'][str(ex2[i]['duration'])+'s'].append(ex2[i]['frame_displayed'])
	mfd_data['simple']['Emotion'][''.join(list(ex1[i]['File_Extension'])[1::])].append(ex2[i]['frame_displayed'])
	mfd_data['complex']['Duration_Block'][str(ex2[i]['duration'])+'s'+'_'+'B'+str(ex2[i]['block'])].append(ex2[i]['frame_displayed'])
	mfd_data['complex']['Duration_Emotion'][str(ex2[i]['duration'])+'s'+'_'+''.join(list(ex1[i]['File_Extension'])[1::])].append(ex2[i]['frame_displayed'])
	mfd_data['complex']['Block_Emotion']['B' + str(ex2[i]['block'])+'_'+''.join(list(ex1[i]['File_Extension'])[1::])].append(ex2[i]['frame_displayed'])
	mfd_data['complex']['Block_Emotion_Duration']['B' + str(ex2[i]['block'])+'_'+''.join(list(ex1[i]['File_Extension'])[1::])+'_'+str(ex2[i]['duration'])+'s'].append(ex2[i]['frame_displayed'])

emotions=['happy','sad','mad','scared']
durations=['6s','12s']
mfd_data['simple']['Half']['H1'].extend(mfd_data['simple']['Block']['B1'] + mfd_data['simple']['Block']['B2'])
mfd_data['simple']['Half']['H2'].extend(mfd_data['simple']['Block']['B3'] + mfd_data['simple']['Block']['B4'])
for emotion in emotions:
    for duration in durations:
        mfd_data['complex']['Half_Emotion_Duration']['H1_%s_%s' %(emotion, duration)].extend(mfd_data['complex']['Block_Emotion_Duration']['B1_%s_%s' %(emotion, duration)] + mfd_data['complex']['Block_Emotion_Duration']['B2_%s_%s' %(emotion, duration)])
        mfd_data['complex']['Half_Emotion_Duration']['H2_%s_%s' %(emotion, duration)].extend(mfd_data['complex']['Block_Emotion_Duration']['B3_%s_%s' %(emotion, duration)] + mfd_data['complex']['Block_Emotion_Duration']['B4_%s_%s' %(emotion, duration)])
for emotion in emotions:
    mfd_data['complex']['Half_Emotion']['H1_%s' % emotion].extend(mfd_data['complex']['Block_Emotion']['B1_%s' % emotion] + mfd_data['complex']['Block_Emotion']['B2_%s' % emotion])
    mfd_data['complex']['Half_Emotion']['H2_%s' % emotion].extend(mfd_data['complex']['Block_Emotion']['B3_%s' % emotion] + mfd_data['complex']['Block_Emotion']['B4_%s' % emotion])
for duration in durations:
    mfd_data['complex']['Half_Duration']['H1_%s' % duration].extend(mfd_data['complex']['Duration_Block']['%s_B1' % duration] + mfd_data['complex']['Duration_Block']['%s_B2' % duration])
    mfd_data['complex']['Half_Duration']['H2_%s' % duration].extend(mfd_data['complex']['Duration_Block']['%s_B3' % duration] + mfd_data['complex']['Duration_Block']['%s_B4' % duration])


for level in mfd_data:
    for dim in mfd_data[level]:
        for cat in mfd_data[level][dim]:
            mfd_vals[level][dim][cat]=np.median(mfd_data[level][dim][cat])
            if 'Half' in dim: 
                print cat, 'is', mfd_vals[level][dim][cat]

#MFD_keys = {'simple':dict(Exemplar=['af1','af4','am1','am2'], Gender=['M','F'], Block=['B1','B2','B3','B4'], Duration=['6s','12s'], Emotion=['_happy','_sad','_mad','_scared'], Total=['Total']), 'complex':dict(Duration_Block=['6s_B1','6s_B2','6s_B3','6s_B4','12s_B1','12s_B2','12s_B3','12s_B4'], Duration_Emotion=['6s_happy','6s_sad','6s_mad','6s_scared','12s_happy','12s_sad','12s_mad','12s_scared'], Block_Emotion=['B1_happy','B1_sad','B1_mad','B1_scared','B2_happy','B2_sad','B2_mad','B2_scared','B3_happy','B3_sad','B3_mad','B3_scared','B4_happy','B4_sad','B4_mad','B4_scared'], Block_Emotion_Duration=['B1_happy_6s','B1_sad_6s','B1_mad_6s','B1_scared_6s','B2_happy_6s','B2_sad_6s','B2_mad_6s','B2_scared_6s','B3_happy_6s','B3_sad_6s','B3_mad_6s','B3_scared_6s','B4_happy_6s','B4_sad_6s','B4_mad_6s','B4_scared_6s','B1_happy_12s','B1_sad_12s','B1_mad_12s','B1_scared_12s','B2_happy_12s','B2_sad_12s','B2_mad_12s','B2_scared_12s','B3_happy_12s','B3_sad_12s','B3_mad_12s','B3_scared_12s','B4_happy_12s','B4_sad_12s','B4_mad_12s','B4_scared_12s'])}
#MFD_vals = {'simple':dict(Exemplar=[], Gender=[], Block=[], Duration=[], Emotion=[], Total=[]), 'complex':dict(Duration_Block=[],Duration_Emotion=[],Block_Emotion=[],Block_Emotion_Duration=[])}
#for type in MFD_keys:
#	for dim in MFD_keys[type]:
#		for cat in MFD_keys[type][dim]:
#			MFD_vals[type][dim].append(numpy.median(dims2[dim][cat]))


#bar graph- PC vs each variable
plt.figure(figsize=(12,6), dpi=100)
groups, rect_labels, n_labels = ([],[],[])
dim_order=['Exemplar','Gender','Block','Duration','Emotion','Total']
cat_order=dict(Exemplar=['af1','af4','am1','am2'], Gender=['M','F'], Block=['B1','B2','B3','B4'], Duration=['6s','12s'], Emotion=['happy','sad','mad','scared'], Total=['Total'])
for dim in dim_order:
    groups.append([])
    for cat in cat_order[dim]:
        groups[-1].append(pc_vals[dim][cat])
        n_labels.append(len(pc_data[dim][cat]))
group_labels = dim_order
rect_labels=['af1','af4','am1','am2','M','F','B1','B2','B3','B4','6s','12s','Ha','Sa','Ma','Sc','']
value_labels = [x for sublist in groups for x in sublist]
margin = 0.10
width = 0.4
#plot the bar graph
s = plt.subplot(1,1,1)
totdist, group_pos, rect_pos_array, rects = [width-margin,[],[],[]]
for num, vals in enumerate(groups):
    ind = np.arange(len(vals))*width
    xdata = ind + margin + totdist
    totdist = xdata[-1] + width + margin
    group_pos.append((xdata[0] + xdata[-1] + width)/2.)
    rect_pos_array.append(list(xdata+(width/2)))
    rects.append(s.bar(xdata, vals, width))
rect_pos = [x for sublist in rect_pos_array for x in sublist]
#label the individual plots
s.text(0.2, 2, 'N =', ha='center',size='x-small', color='black')
n = 0
for rect in rects:
    for rec in rect:
        height = rec.get_height()
        #s.text(rec.get_x() + rec.get_width()/2., 0.95*height, rect_labels[n], ha='center', va='bottom', color='white', size='small')
        s.text(rec.get_x() + rec.get_width()/2., 1.05*height, '%.2f' %value_labels[n], ha='center', va='bottom',size='x-small')
        s.text(rec.get_x() + rec.get_width()/2., 2, n_labels[n], ha='center',size='x-small', color='white')
        n+=1
n=0
for group in group_labels:
    s.text(group_pos[n], 0-max(value_labels)*0.08, group_labels[n], ha='center', size='small')
    n+=1
#label the axes
s.set_xticks(rect_pos)
s.set_xticklabels(rect_labels, size='small')
#plt.xlabel('Category')
plt.ylabel('Percent Correct')
plt.title('Percent Correct by Each Variable')
plt.ylim([0,max(value_labels)*1.1])
plt.xlim([0,rects[-1][-1].get_x()+rects[-1][-1].get_width()+margin])
plt.savefig('data/Processed Data (Test)/'+filenameRoot+'/PC_Summary.png')


#bar graph- simple MFD vs each variable
plt.figure(figsize=(11,6), dpi=100)
groups, rect_labels, n_labels = ([],[],[])
dim_order=['Exemplar','Gender','Block','Duration','Emotion','Total']
cat_order=dict(Exemplar=['af1','af4','am1','am2'], Gender=['M','F'], Block=['B1','B2','B3','B4'], Duration=['6s','12s'], Emotion=['happy','sad','mad','scared'], Total=['Total'])
for dim in dim_order:
    groups.append([])
    for cat in cat_order[dim]:
        groups[-1].append(mfd_vals['simple'][dim][cat])
        n_labels.append(len(mfd_data['simple'][dim][cat]))
group_labels = dim_order
rect_labels=['af1','af4','am1','am2','M','F','B1','B2','B3','B4','6s','12s','Ha','Sa','Ma','Sc','']
value_labels = [x for sublist in groups for x in sublist]
margin = 0.10
width = 0.4
#plot the bar graph
s = plt.subplot(1,1,1)
totdist, group_pos, rects = [width-margin,[],[]]
for num, vals in enumerate(groups):
    ind = np.arange(len(vals))*width
    xdata = ind + margin + totdist
    totdist = xdata[-1] + width + margin
    group_pos.append((xdata[0] + xdata[-1] + width)/2.)
    rects.append(plt.bar(xdata, vals, width))
#label the individual plots
plt.text(0.2, 2, 'N =', ha='center',size='x-small', color='black')
n = 0
for rect in rects:
    for rec in rect:
        height = rec.get_height()
        plt.text(rec.get_x() + rec.get_width()/2., 0.95*height, rect_labels[n], ha='center', va='bottom', color='white',size='small')
        plt.text(rec.get_x() + rec.get_width()/2., 1.05*height, '%.2f' %value_labels[n], ha='center', va='bottom',size='x-small')
        plt.text(rec.get_x() + rec.get_width()/2., 2, n_labels[n], ha='center',size='x-small', color='white')
        n+=1
#label the axes
s.set_xticks(group_pos)
s.set_xticklabels(group_labels)
#plt.xlabel('Variable')
plt.ylabel('Median Frame Displayed')
plt.title('Median Frame by Each Variable')
plt.ylim([0,max(value_labels)*1.1])
plt.xlim([0,rects[-1][-1].get_x()+rects[-1][-1].get_width()+margin])
plt.savefig('data/Processed Data (Test)/'+filenameRoot+'/MFD_Summary.png')


#bar graph- duration x emotion vs MFD
plt.figure(figsize=(7,7), dpi=100)
dim_order=['6s','12s']
cat_order=['happy', 'sad', 'mad', 'scared']
rect_labels = ['Happy', 'Sad', 'Mad', 'Scared', 'Happy', 'Sad', 'Mad', 'Scared']
groups,n_labels=([],[])
for dim in dim_order:
    groups.append([])
    for cat in cat_order:
        groups[-1].append(mfd_vals['complex']['Duration_Emotion'][dim+'_'+cat])
        n_labels.append(len(mfd_data['complex']['Duration_Emotion'][dim+'_'+cat]))
group_labels = dim_order
value_labels = [x for sublist in groups for x in sublist]
margin = 0.10
width = 0.4
#plot the bar graph
s = plt.subplot(1,1,1)
totdist, group_pos, rects = [width-margin,[],[]]
for num, vals in enumerate(groups):
    ind = np.arange(len(vals))*width
    xdata = ind + margin + totdist
    totdist = xdata[-1] + width + margin
    group_pos.append((xdata[0] + xdata[-1] + width)/2.)
    rects.append(plt.bar(xdata, vals, width, color=['y','b','r','g']))
#label the individual plots
n = 0
plt.text(0.2, 2, 'N =', ha='center',size='x-small', color='black')
for rect in rects:
    for rec in rect:
        height = rec.get_height()
        plt.text(rec.get_x() + rec.get_width()/2., 0.95*height, rect_labels[n], ha='center', color='white',size='small')
        plt.text(rec.get_x() + rec.get_width()/2., 1.05*height, '%.2f' %value_labels[n], ha='center', va='bottom',size='x-small')
        plt.text(rec.get_x() + rec.get_width()/2., 2, n_labels[n], ha='center',size='small', color='white')
        n+=1
#label the axes
s.set_xticks(group_pos)
s.set_xticklabels(group_labels)
plt.xlabel('Category')
plt.ylabel('Median Frame Diplayed')
plt.ylim([0,max(value_labels)*1.1])
plt.xlim([0,rects[-1][-1].get_x()+rects[-1][-1].get_width()+margin])
plt.title('Median Frame Displayed by Emotion and Duration')
plt.savefig('data/Processed Data (Test)/'+filenameRoot+'/MFD_Emotion_Duration.png')


#line graphs

#Block x Duration vs MFD
blocks = ['B1','B2','B3','B4']
plt.figure(figsize=(8,6), dpi=100)
Fig2 = plt.subplot(111)
line1,line2=([],[])
for block in blocks:
    if mfd_vals['complex']['Duration_Block']['6s_%s'%block] == []:
        line1.append(None)
    else: line1.append(mfd_vals['complex']['Duration_Block']['6s_%s'%block])
    if mfd_vals['complex']['Duration_Block']['12s_%s'%block] == []:
        line2.append(None)
    else: line2.append(mfd_vals['complex']['Duration_Block']['12s_%s'%block])

Fig2.plot([1,2,3,4],line1,'bo-',label='6s')
Fig2.plot([1,2,3,4],line2,'go-',label='12s')
handles, labels = Fig2.get_legend_handles_labels()
display = (0,1)
box = Fig2.get_position()
Fig2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
Fig2.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)
Fig2.set_xticks([1,2,3,4])
Fig2.set_xticklabels(blocks)
plt.xlim([0.5,4.5])
plt.ylim([(min(line1+line2))*0.9,(max(line1+line2))*1.1])
plt.xlabel('Blocks')
plt.ylabel('Median Frame Displayed')
plt.title('Median Frame Displayed by Block and Duration')
plt.savefig('data/Processed Data (Test)/'+filenameRoot+'/MFD_Block_Duration.png')

#Block x Emotion vs MFD (all)
plt.figure(figsize=(8,6), dpi=100)
blocks = ['B1','B2','B3','B4']
Fig3 = plt.subplot(111)
lines = dict(happy=[],sad=[],mad=[],scared=[])
for block in blocks:
    for emotion in lines.keys():
        if mfd_vals['complex']['Block_Emotion']['%s_%s'%(block,emotion)] == []:
            lines[emotion].append(None)
        else: lines[emotion].append(mfd_vals['complex']['Block_Emotion']['%s_%s'%(block,emotion)])
Fig3.plot([1,2,3,4],lines['happy'],'yo-',label='Happy')
Fig3.plot([1,2,3,4],lines['sad'],'bo-',label='Sad')
Fig3.plot([1,2,3,4],lines['mad'],'ro-',label='Mad')
Fig3.plot([1,2,3,4],lines['scared'],'go-',label='Scared')
handles, labels = Fig3.get_legend_handles_labels()
display = (0,1,2,3)
box = Fig3.get_position()
Fig3.set_position([box.x0, box.y0, box.width * 0.8, box.height])
Fig3.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)
Fig3.set_xticks([1,2,3,4])
Fig3.set_xticklabels(blocks)
plt.xlim([0.5,4.5])
plt.ylim([0.9*min([x for sublist in lines.values() for x in sublist]),1.1*max([x for sublist in lines.values() for x in sublist])])
plt.xlabel('Blocks')
plt.ylabel('Median Frame Displayed')
plt.title('Median Frame Displayed by Block and Emotion')
plt.savefig('data/Processed Data (Test)/'+filenameRoot+'/MFD_Block_Emotion_all.png')

#Block x Emotion vs MFD (6s trials)
plt.figure(figsize=(8,6), dpi=100)
blocks = ['B1','B2','B3','B4']
Fig3 = plt.subplot(111)
lines = dict(happy=[],sad=[],mad=[],scared=[])
for block in blocks:
    for emotion in lines.keys():
        if mfd_vals['complex']['Block_Emotion_Duration']['%s_%s_6s'%(block,emotion)] == []:
            lines[emotion].append(None)
        else: lines[emotion].append(mfd_vals['complex']['Block_Emotion_Duration']['%s_%s_6s'%(block,emotion)])
Fig3.plot([1,2,3,4],lines['happy'],'yo-',label='Happy')
Fig3.plot([1,2,3,4],lines['sad'],'bo-',label='Sad')
Fig3.plot([1,2,3,4],lines['mad'],'ro-',label='Mad')
Fig3.plot([1,2,3,4],lines['scared'],'go-',label='Scared')
handles, labels = Fig3.get_legend_handles_labels()
display = (0,1,2,3)
box = Fig3.get_position()
Fig3.set_position([box.x0, box.y0, box.width * 0.8, box.height])
Fig3.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)
Fig3.set_xticks([1,2,3,4])
Fig3.set_xticklabels(blocks)
plt.xlim([0.5,4.5])
plt.ylim([0.9*min([x for sublist in lines.values() for x in sublist]),1.1*max([x for sublist in lines.values() for x in sublist])])
plt.xlabel('Blocks')
plt.ylabel('Median Frame Displayed')
plt.title('Median Frame Displayed by Block and Emotion- 6s trials')
plt.savefig('data/Processed Data (Test)/'+filenameRoot+'/MFD_Block_Emotion_6s.png')

#Block x Emotion vs MFD (6s trials)
plt.figure(figsize=(8,6), dpi=100)
blocks = ['B1','B2','B3','B4']
Fig3 = plt.subplot(111)
lines = dict(happy=[],sad=[],mad=[],scared=[])
for block in blocks:
    for emotion in lines.keys():
        if mfd_vals['complex']['Block_Emotion_Duration']['%s_%s_12s'%(block,emotion)] == []:
            lines[emotion].append(None)
        else: lines[emotion].append(mfd_vals['complex']['Block_Emotion_Duration']['%s_%s_12s'%(block,emotion)])
Fig3.plot([1,2,3,4],lines['happy'],'yo-',label='Happy')
Fig3.plot([1,2,3,4],lines['sad'],'bo-',label='Sad')
Fig3.plot([1,2,3,4],lines['mad'],'ro-',label='Mad')
Fig3.plot([1,2,3,4],lines['scared'],'go-',label='Scared')
handles, labels = Fig3.get_legend_handles_labels()
display = (0,1,2,3)
box = Fig3.get_position()
Fig3.set_position([box.x0, box.y0, box.width * 0.8, box.height])
Fig3.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1)
Fig3.set_xticks([1,2,3,4])
Fig3.set_xticklabels(blocks)
plt.xlim([0.5,4.5])
plt.ylim([0.9*min([x for sublist in lines.values() for x in sublist]),1.1*max([x for sublist in lines.values() for x in sublist])])
plt.xlabel('Blocks')
plt.ylabel('Median Frame Displayed')
plt.title('Median Frame Displayed by Block and Emotion- 12s trials')
plt.savefig('data/Processed Data (Test)/'+filenameRoot+'/MFD_Block_Emotion_12s.png')

pc_out={}
pc_cols = ['PC_Total', 'PC_am1', 'PC_am2', 'PC_af1','PC_af4', 'PC_happy', 
    'PC_sad', 'PC_mad', 'PC_scared', 'PC_M', 'PC_F', 'PC_6s','PC_12s', 
    'PC_B1', 'PC_B2', 'PC_B3', 'PC_B4', 'PC_H1', 'PC_H2']
for key in pc_vals.keys():
    for dim in pc_vals[key].keys():
        pc_out['PC_' + dim] = pc_vals[key][dim]

mfd_out={}
mfd_cols=['MFD_Total', 'MFD_happy', 'MFD_sad', 'MFD_mad', 'MFD_scared', 
    'MFD_M', 'MFD_F',
    'MFD_am1', 'MFD_am2', 'MFD_af1', 'MFD_af4', 
    'MFD_6s', 'MFD_12s',
    'MFD_B1', 'MFD_B2','MFD_B3','MFD_B4', 
    'MFD_6s_B1','MFD_6s_B2','MFD_6s_B3','MFD_6s_B4', 
    'MFD_12s_B1','MFD_12s_B2','MFD_12s_B3', 'MFD_12s_B4', 
    'MFD_B1_happy', 'MFD_B1_sad', 'MFD_B1_mad','MFD_B1_scared',
    'MFD_B2_happy','MFD_B2_sad','MFD_B2_mad','MFD_B2_scared',
    'MFD_B3_happy', 'MFD_B3_sad', 'MFD_B3_mad','MFD_B3_scared', 
    'MFD_B4_happy', 'MFD_B4_sad',  'MFD_B4_mad','MFD_B4_scared',
    'MFD_12s_happy','MFD_12s_sad', 'MFD_12s_mad', 'MFD_12s_scared',
    'MFD_6s_happy', 'MFD_6s_sad', 'MFD_6s_mad', 'MFD_6s_scared', 
    'MFD_B1_happy_6s', 'MFD_B1_happy_12s', 'MFD_B1_sad_6s', 'MFD_B1_sad_12s', 
    'MFD_B1_mad_6s', 'MFD_B1_mad_12s', 'MFD_B1_scared_6s', 'MFD_B1_scared_12s', 
    'MFD_B2_happy_6s', 'MFD_B2_happy_12s', 'MFD_B2_sad_6s', 'MFD_B2_sad_12s', 
    'MFD_B2_mad_6s', 'MFD_B2_mad_12s', 'MFD_B2_scared_6s', 'MFD_B2_scared_12s', 
    'MFD_B3_happy_6s', 'MFD_B3_happy_12s', 'MFD_B3_sad_6s', 'MFD_B3_sad_12s', 
    'MFD_B3_mad_6s', 'MFD_B3_mad_12s', 'MFD_B3_scared_6s', 'MFD_B3_scared_12s', 
    'MFD_B4_happy_6s', 'MFD_B4_happy_12s', 'MFD_B4_sad_6s', 'MFD_B4_sad_12s', 
    'MFD_B4_mad_6s', 'MFD_B4_mad_12s', 'MFD_B4_scared_6s', 'MFD_B4_scared_12s',
    'MFD_H1', 'MFD_H2', 'MFD_H1_happy_6s', 'MFD_H1_happy_12s', 'MFD_H1_sad_6s', 
    'MFD_H1_sad_12s', 'MFD_H1_mad_6s', 'MFD_H1_mad_12s', 'MFD_H1_scared_6s', 
    'MFD_H1_scared_12s', 'MFD_H2_happy_6s', 'MFD_H2_happy_12s', 'MFD_H2_sad_6s', 
    'MFD_H2_sad_12s', 'MFD_H2_mad_6s', 'MFD_H2_mad_12s', 'MFD_H2_scared_6s', 
    'MFD_H2_scared_12s', 'MFD_H1_happy', 'MFD_H1_sad', 'MFD_H1_mad', 'MFD_H1_scared', 
    'MFD_H2_happy', 'MFD_H2_sad', 'MFD_H2_mad', 'MFD_H2_scared', 'MFD_H1_6s', 'MFD_H1_12s',
    'MFD_H2_6s', 'MFD_H2_12s']
for level in mfd_vals.keys():
    for key in mfd_vals[level].keys():
            for dim in mfd_vals[level][key].keys():
                mfd_out['MFD_' + dim] = mfd_vals[level][key][dim]

#get data from rankings
wb = xlrd.open_workbook('data/'+filenameRoot+'.xlsx')
ws = wb.sheet_by_name('emotion_ranking')
rankings,rank_cols = ({},[])
for col,exemplar in enumerate(ws.row_values(0)[1::]):
    for row,emotion in enumerate(ws.col_values(0)[1::]):
        rankings['Rank_'+str(exemplar)[0:3]+'_'+str(emotion)] = ws.cell_value(row+1,col+1)
        rank_cols.append('Rank_'+str(exemplar)[0:3]+'_'+str(emotion))

#compile output data
out = dict(pc_out, **mfd_out)
out.update(rankings)
out['Subject'] = filenameRoot

#create or append summary file with data
if len(open('data/Processed Data (Test)/summary_test.csv','r').read())==0:
    f = open('data/Processed Data (Test)/summary_test.csv','w') #'w' to write a new file, 'a' to append an old one
    newfile = True
else: 
    f = open('data/Processed Data (Test)/summary_test.csv','a')
    newfile = False
fieldnames = ['Subject'] + pc_cols + mfd_cols + rank_cols
headers = dict((n,n) for n in fieldnames)
myWriter = csv.DictWriter(f,fieldnames=fieldnames)
if newfile: myWriter.writerow(headers)
myWriter.writerow(out)
f.close()

#create subject data file
subjectfile = open('data/Processed Data (Test)/' + filenameRoot + '/subject_data.csv', 'wb')
myWriter = csv.DictWriter(subjectfile,fieldnames=fieldnames)
myWriter.writerow(headers)
myWriter.writerow(out)
subjectfile.close()