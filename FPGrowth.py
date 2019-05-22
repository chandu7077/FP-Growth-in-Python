import pandas as pd
import  operator
class fptree:
    def __init__(self,ide,cnt,parent):
        self.ide=ide
        self.cnt=cnt
        self.parent=parent
        self.link=None
        self.child={}
    def increm(self,cnt):
        self.cnt+=cnt
def genFi(data,minsp,dic=False):
    kdc={}
    fi,sfi=[],[]
    nnewdata={}
    for dat in data:
        if len(dat)>0:
            for i in range(0,len(dat)):
                if dat[i] not in kdc:
                    kdc[dat[i]]=1
                elif dat[i] in dat[0:i]:
                    continue
                else:
                    kdc[dat[i]]+=1
    dis=[]
    for k,v in kdc.items():
        if v<minsp:
            dis.append(k)
    for it in dis:
        del kdc[it]
    sfi=kdc
    kdc=sorted(kdc,key=kdc.get,reverse=True)
    for it in sfi:
        sfi[it]=[sfi[it],None]
    rem=[]
    for i in range(len(data)):
        if len(data[i])>0: 
            newdata=[]
            for it in kdc:
                if it in data[i]:
                    newdata.append(it)
            data[i]=newdata
        else:
            rem.append(i)
    for it in rem:
        del data[it]
    kdc=sfi
    for it in data:
        if tuple(it) not in nnewdata: 
            nnewdata[tuple(it)]=1
        else:
            nnewdata[tuple(it)]+=1
    null=fptree("null",1,None)
    for dat,cnt in nnewdata.items():
        genTree(dat,cnt,null,kdc)
    return null,kdc
def genTree(data,cnt,null,kdc):
    if len(data)<0:
        return
    if data[0] not in null.child:
        null.child[data[0]]=fptree(data[0],cnt,null)
        if kdc[data[0]][1]==None:
            kdc[data[0]][1]=null.child[data[0]]
        else:
#adding one more path where node present in other path
            updateNull(kdc[data[0]][1],null.child[data[0]])
    else:
        null.child[data[0]].increm(cnt)
    if len(data)>1:
        genTree(data[1:],cnt,null.child[data[0]],kdc)
#nodes with same names but in different paths
def updateNull(alr_pre_node,same_new):
    while(alr_pre_node.link!=None):
        alr_pre_node=alr_pre_node.link
    alr_pre_node.link=same_new
def gen_cond_pattern_bases(node):
    patterns={}
    while node!=None:
        prefix=[]
        bottom_up(node,prefix)
        if len(prefix)>1:
            patterns[tuple(prefix[1:])]=node.cnt
        node=node.link
    return patterns
def bottom_up(node,prefix):
    if node.parent!=None:
        prefix.append(node.ide)
        bottom_up(node.parent,prefix)
def cond_tree(null,kdc,minsup,prefix,freq_items,sup={},sing_sup={}):
    List=[v[0] for v in sorted(kdc.items(),key=operator.itemgetter(0))]
    for it in List:
        new_freq_items=prefix.copy()
        dic={}
        dic[it]=0
        for k,v in sup.items():
            if it in k:
                dic[it]+=v
        new_freq_items.add(it)
        if dic[it]!=0:
            freq_items.append((new_freq_items,dic[it]))
        else:
            freq_items.append((new_freq_items,sing_sup[it][0]))
        patterns=gen_cond_pattern_bases(kdc[it][1])
        da=[]
        for k,v in patterns.items():
            for i in range(0,v):
                if len(list(k))>0:
                    da.append(list(k))
        if len(da)!=0:
            new_null,new_kdc=genFi(da,msp)
        else:
            new_null=None
        if new_null!=None:
            cond_tree(new_null,new_kdc,minsup,new_freq_items,freq_items,patterns,sing_sup)
msp=2
htable=genFi(dats,msp)
freq_itemss=[]
cond_tree(htable[0],htable[1],msp,set([]),freq_itemss,{},htable[1])
freq_itemss
data=pd.DataFrame(columns=["items","support"])
its=[]
sps=[]
for i in range(0,len(freq_itemss)):
    its.append(list(freq_itemss[i][0]))
    sps.append(freq_itemss[i][1])
data["items"]=its
data["support"]=sps
print(data.sort_values(ascending=False,by="support"))
