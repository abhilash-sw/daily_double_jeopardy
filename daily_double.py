#####################################################
# @Author: Abhilash Sarwade
# @Date:   2018-07-31 09:40:31
# @email: sarwade@isac.gov.in
# @File Name: daily_double.py
# @Project: None

# @Last Modified time: 2018-07-31 18:11:15
#####################################################
import urllib3
from bs4 import BeautifulSoup
import numpy as np
import heatmap_matplotlib
import matplotlib.pyplot as plt

http = urllib3.PoolManager()

j_dd_pos_all = []
dj_dd_pos_all =[]

#season = 34
for season in range(1,35):
    print('Season - '+str(season))
    url = 'http://j-archive.com/showseason.php?season='+str(season)

    response = http.request('GET', url,retries=10)

    soup = BeautifulSoup(response.data)

    t = soup.find('table')
    trs = t.find_all('tr')
    game_url = []

    for tr in trs:
        game_url.append(tr.find('a').get('href'))

    j_dd_pos = []
    dj_dd_pos = []

    for gu in game_url:
        print(gu)
        response = http.request('GET', gu,retries=10)
        soup = BeautifulSoup(response.data)
        clue_tables = soup.find_all('table',{'class':'clue_header'})
        for ct in clue_tables:
            if ct.find('td',{'class':'clue_value_daily_double'}):
                clue_no = ct.find('td',{'class':'clue_unstuck'}).get('id')
                clue_no_array = clue_no.split('_')
                if clue_no_array[1] == 'J':
                    tmp_pos_x = int(clue_no_array[2])
                    tmp_pos_y = int(clue_no_array[3])
                    tmp_pos = np.array((tmp_pos_x,tmp_pos_y))
                    j_dd_pos.append(tmp_pos)
                    j_dd_pos_all.append(tmp_pos)
                elif clue_no_array[1] == 'DJ':
                    tmp_pos_x = int(clue_no_array[2])
                    tmp_pos_y = int(clue_no_array[3])
                    tmp_pos = np.array((tmp_pos_x,tmp_pos_y))
                    dj_dd_pos.append(tmp_pos)
                    dj_dd_pos_all.append(tmp_pos)

    j_dd_pos = np.array(j_dd_pos)
    dj_dd_pos = np.array(dj_dd_pos)


    xticks = ['Category1','Category2','Category3','Category4','Category5','Category6']
    yticks_j = ['$200','$400','$600','$800','$1000']
    yticks_dj = ['$400','$800','$1200','$1600','$2000']


    hs_j = np.histogram2d(j_dd_pos[:,0]-0.5,j_dd_pos[:,1]-0.5,bins=[6,5],range=[[0,6],[0,5]])

    fig, ax = plt.subplots()
    fig.set_size_inches(9,9)
    #ax.set_facecolor('blue')
    im,cbar = heatmap_matplotlib.heatmap(hs_j[0].T,yticks_j,xticks,cmap='Blues')
    ax.set_title('Jeopardy! Round\n\n\n',fontweight='bold',fontsize=20)
    ax.set_xlabel('Daily Double Heatmap',fontweight='bold',fontsize=18)
    #fig.tight_layout()
    fig.savefig('jeopardy_'+str(season)+'.png',dpi=300,bbox_inches='tight')


    hs_dj = np.histogram2d(dj_dd_pos[:,0]-0.5,dj_dd_pos[:,1]-0.5,bins=[6,5],range=[[0,6],[0,5]])

    fig, ax = plt.subplots()
    fig.set_size_inches(9,9)
    #ax.set_facecolor('blue')
    im,cbar = heatmap_matplotlib.heatmap(hs_dj[0].T,yticks_dj,xticks,cmap='Blues')
    ax.set_title('Double Jeopardy! Round\n\n\n',fontweight='bold',fontsize=20)
    ax.set_xlabel('Daily Double Heatmap',fontweight='bold',fontsize=18)
    #fig.tight_layout()
    fig.savefig('double_jeopardy_'+str(season)+'.png',dpi=300,bbox_inches='tight')


j_dd_pos_all = np.array(j_dd_pos_all)
dj_dd_pos_all = np.array(dj_dd_pos_all)


xticks = ['Category1','Category2','Category3','Category4','Category5','Category6']
yticks_j = ['$200','$400','$600','$800','$1000']
yticks_dj = ['$400','$800','$1200','$1600','$2000']


hs_j = np.histogram2d(j_dd_pos_all[:,0]-0.5,j_dd_pos_all[:,1]-0.5,bins=[6,5],range=[[0,6],[0,5]])

fig, ax = plt.subplots()
fig.set_size_inches(9,9)
#ax.set_facecolor('blue')
im,cbar = heatmap_matplotlib.heatmap(hs_j[0].T,yticks_j,xticks,cmap='Blues')
ax.set_title('Jeopardy! Round\n\n\n',fontweight='bold',fontsize=20)
ax.set_xlabel('Daily Double Heatmap',fontweight='bold',fontsize=18)
heatmap_matplotlib.annotate_heatmap(im,im.get_array()/j_dd_pos_all.shape[0]*100,valfmt="{x:.2f}%")
#fig.tight_layout()
fig.savefig('jeopardy_'+'all'+'.png',dpi=300,bbox_inches='tight')


hs_dj = np.histogram2d(dj_dd_pos_all[:,0]-0.5,dj_dd_pos_all[:,1]-0.5,bins=[6,5],range=[[0,6],[0,5]])

fig, ax = plt.subplots()
fig.set_size_inches(9,9)
#ax.set_facecolor('blue')
im,cbar = heatmap_matplotlib.heatmap(hs_dj[0].T,yticks_dj,xticks,cmap='Blues')
ax.set_title('Double Jeopardy! Round\n\n\n',fontweight='bold',fontsize=20)
ax.set_xlabel('Daily Double Heatmap',fontweight='bold',fontsize=18)
#fig.tight_layout()
heatmap_matplotlib.annotate_heatmap(im,im.get_array()/dj_dd_pos_all.shape[0]*100,valfmt="{x:.2f}%")
fig.savefig('double_jeopardy_'+'all'+'.png',dpi=300,bbox_inches='tight')