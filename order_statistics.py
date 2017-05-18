import numpy as np
import math as m




def weighted_rand_int(stype):
    u=np.random.random_sample()
    n,y,l1=stype,2**stype,range(stype+1)
    weights=[float(m.factorial(n))/(m.factorial(i)*m.factorial(n-i)*y) for i in l1]
    intervals=[sum(weights[:i]) for i in l1[1:]]+[1]
    count=0
    while u>intervals[count]:
        count+=1
    return count


   
# who_plays_who_three_times[num] is a list of the teams num plays three times... set it up
def make2(num,m1,m2,who_plays_who_three_times,index):
    for opponent in who_plays_who_three_times[num]:
        # Find the matchup index that corresponds to when opponent played num
        if opponent>num:
            matchup_index=index[num][opponent-1]
        else:
            matchup_index=index[num][opponent]
        x=weighted_rand_int(3)
        m1=m1[:matchup_index]+[x]+m1[matchup_index+1:]
        m2=m2[:matchup_index]+[3-x]+m2[matchup_index+1:]
    return m1,m2



# Now for all other teams, you should be able to assign them np.random.randints of height 3, or 5 now come one
# Ok, first the easy step. For each team i in 0-14, make them play each team j 15-29 twice.
def make3(num,m1,m2,index):
    if num < 15:
        for i in range(15,30):
            matchup_index=index[num][i-1]
            x=weighted_rand_int(2)
            m1=m1[:matchup_index]+[x]+m1[matchup_index+1:]
            m2=m2[:matchup_index]+[2-x]+m2[matchup_index+1:]
    return m1,m2

# Now do all the 10 other teams that they face four times. For that, we will need to do
# two seperate things for both conferences. Lets start with conference 1, say teams 0-14 represent the west.
# We want to find the keys for teams inside their conference whom arent in the who_plays_who_three_times list..
def make4(i,j,m1,m2,teams_three_times,index):
    if j not in teams_three_times:
        matchup_index=index[i][j-1]
        x=weighted_rand_int(4)
        m1=m1[:matchup_index]+[x]+m1[matchup_index+1:]
        m2=m2[:matchup_index]+[4-x]+m2[matchup_index+1:]
    return m1,m2







def make_matchups(who_plays_who_three_times,index):
    matchup_vec=[0]*435 
    matchup_vec_transpose = [0]*435
    for num in range(30):
        matchup_vec,matchup_vec_transpose=make2(num,matchup_vec,matchup_vec_transpose,who_plays_who_three_times,index)
    for num in range(15):
        matchup_vec,matchup_vec_transpose=make3(num,matchup_vec,matchup_vec_transpose,index)
    for i in range(14):
        for j in range(i+1,15):
            matchup_vec,matchup_vec_transpose=make4(i,j,matchup_vec,matchup_vec_transpose,who_plays_who_three_times[i],index)
    for i in range(15,29):
        for j in range(i+1,30):
            matchup_vec,matchup_vec_transpose=make4(i,j,matchup_vec,matchup_vec_transpose,who_plays_who_three_times[i],index)
    return matchup_vec,matchup_vec_transpose















# Create a list of lists called index. For each i,
# the list index[i] stores the indexes of the games involving 
#team i in the matchup_outcomes (alias is Game in Games) vector from the file dontknow3.py
ranges=range(30)[::-1]
ranges=[sum(ranges[:i]) for i in range(30)]
index=[]
for i in range(30):
    index.append([])
for i in range(29):
    for ind in range(ranges[i],ranges[i+1]):
        index[i].append(ind)
for i in range(1,30):
    for j,num in enumerate(ranges[:i]):
        index[i].append(num+i-j-1)
for i in range(30):
    index[i]=sorted(index[i])















# Find a season configuration you want.
# Decide which teams play each other three times.
# Make a for loop that assigns a rand int to every one of the matchups that involve teams that only play each other three times.
# One graph I know for sure works can be represented by the 3 10 cycles given by
# [1,7,3,9,5,10,4,8,2,6],[1,12,3,14,5,15,4,13,2,11],[6,12,8,14,10,15,9,13,7,11]
c1 = [i-1 for i in [1,7,3,9,5,10,4,8,2,6]]
c2=[i-1 for i in [1,12,3,14,5,15,4,13,2,11]]
c3=[i-1 for i in [6,12,8,14,10,15,9,13,7,11]]
c4,c5,c6=[i+15 for i in c1],[i+15 for i in c2],[i+15 for i in c3]
who_plays_who_three_times={}
for i in range(30):
    who_plays_who_three_times[i]=[]
def make(ci):
    for num in ci:
        p = ci.index(num)
        partners1,partners2=ci[p-1],ci[(p+1)%10]
        who_plays_who_three_times[num].append(partners1)
        who_plays_who_three_times[num].append(partners2)
make(c1)
make(c2)
make(c3)
make(c4)
make(c5)
make(c6)
for i in range(30):
    who_plays_who_three_times[i]=sorted(who_plays_who_three_times[i])

# Now the dictionary who_plays_who_three_times has teams as keys, and as values has a list of the four teams that that team is
# playing three
# times




# So now I need to a assign a np.random.randint(0,high=4) to each one of the matchups that correspond to these two teams.
# For this, I need to remember what index corresponds to what matchup. This isn't hard.
# The first 29 indexes correspond to the games team 0 plays against teams 1-29.
# For team i , the index[i] is a list of indexes for the matchups that team i is involved in.
# For each i, the first i terms in index[i] correspond to matchups played against teams 0,..,i-1






matchup_vec,matchup_vec_transpose=make_matchups(who_plays_who_three_times,index)










# depending on how many games team i won against team j, for all pairs of teams i,j
# and return a list of length n whose elements correspond to the number of games won by each team
def win_distribution(S,n):
    tri=np.zeros((n,n))
    tri[np.triu_indices(n,1)]=np.array(S[0])
    tri.T[np.triu_indices(n,1)]=np.array(S[1])
    return np.sum(tri,axis=1).astype(int)
# Generate M random samples and return as a list. N is the total number of games. n is the number of teams
def generate(M,N,n,who_plays_who_three_times,index):
    Season_Outcomes=[]
    for i in range(M):
        S=make_matchups(who_plays_who_three_times,index)
        Season_Outcomes.append(S)
    Win_Dist=[]
    for S in Season_Outcomes:
        Win_Dist.append(win_distribution(S,n))
    return np.sort(np.array(Win_Dist))
# Make a vector of the unique values of the vector Win_Dist. 
def make_unique_vector(a):
    b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, idx = np.unique(b, return_index=True)
    return a[idx]
def round_robin(n,M,who,index):
    # n is the number of teams
    # N is the number of games played. Since each team plays each other team exactly once, there are 
    N = (n*(n-1))/2
    Win_Distribution=generate(M,N,n,who,index)
    unique_Win_Dist=make_unique_vector(Win_Distribution).tolist()
    Win_Distribution=Win_Distribution.tolist()
    mydict={}
    for i,d in enumerate(unique_Win_Dist):
        c=Win_Distribution.count(d)
        mydict[i]=c
    list_of_pairs=[]
    for key, value in sorted(mydict.iteritems(), key=lambda (k,v): (v,k)):
        list_of_pairs.append( [Win_Distribution[key], value] )
    return list_of_pairs        








monte_carlo_sims = round_robin(30,1000,who_plays_who_three_times,index)
for i in range(1000):
    print monte_carlo_sims[i][0], monte_carlo_sims[i][1]



def get_overall_max_min(monte):
    minees=[]
    maxees=[]
    for i in range(len(monte)):
        minees.append(monte[i][0][0])
        maxees.append(monte[i][0][-1])
    return maxees,minees



maxees,minees= get_overall_max_min(monte_carlo_sims)
for i in range(len(maxees)):
    print minees[i], maxees[i]



































