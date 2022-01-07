import copy
import math

# Bayesian Belief Networks

class BBN:

    def __init__(self, a, b, c, d, e):
        self.nodes = a   # a Bayes háló csúcsai
        self.evidences = b    # ismert értékek, evidenciák
        self.target = c # a célváltozó indexe
        self.choices = d # lehetséges döntések száma
        self.utility = e #  a lehetséges célváltozó-érték és döntés kombinációkhoz tartozó hasznosság értékeket tartalmazza
        self.varies = [] # az egyes lehetséges variációk és esélyeik
        self.sum = 0 # alfa

    def recursion(self, start):
        
        if(start.n == [] or start.need == True):
            start.needed()
            return        

        for i in start.n:
            self.recursion(self.nodes[int(i)])

        start.needed()


    def important(self):
        for key in self.evidences:
            self.recursion(self.nodes[int(key)])

        self.recursion(self.nodes[self.target])

    def parent_prob(self, startnode, startnode_value, parent_value):
        
        # ha nincs szülő, akkor simán az érték
        if self.nodes[startnode].n == []:
            
            return self.nodes[startnode].probabilities["non"][startnode_value]
        
        # ha van szülő, akkor itt összefűzi és kiszámolja
        
        return self.nodes[startnode].probabilities[",".join(str(v) for v in parent_value)][startnode_value]

    def vari(self):
        vari = []
        for i in range(len(self.nodes)):
            if self.nodes[i].need == False:
                continue
            if(i in self.evidences):
                vari.append([i,1])
                continue
            vari.append([i,self.nodes[i].k])

        return vari
            
    def iterate(self):

        temp = self.vari()
        print(temp)
        list = [i[1] for i in temp]
        print(list)
        length = len(list)
        one = []

        for i in range(length):
            one.append([temp[i][0], 0, 0])

        ended = False

        for i in range(length):
            if list[i] <= 0:
                ended = True
                break        

        while not ended:
            
            help = []

            for i in range(len(one)):
               
                t = []

                if(one[i][0] in self.evidences):
                    one[i][1] = self.evidences[one[i][0]]

                for j in range(len(self.nodes[one[i][0]].n)):

                    for k in range(len(one)):
                        if one[k][0] == int(self.nodes[one[i][0]].n[j]):
                            t.append(one[k][1])

                r = self.parent_prob(one[i][0], one[i][1], t)
                help.append(r)
                continue

            for i in range(len(one)):
                one[i][2] = help[i]

            new = copy.deepcopy(one)
            self.varies.append(new)
            print(self.varies)
            ended = True
            
            for i in range(length):
                one[i][1] += 1
                if one[i][1] < list[i]:
                    ended = False
                    break
                one[i][1] = 0
        
        for i in self.varies:
            
            sum_temp = 1
            for j in i:
                sum_temp *= j[2]
            self.sum += sum_temp

    def final(self):
        self.iterate()

        answers = [0] * self.nodes[self.target].k
        
        for i in self.varies:   
            product = 1
            index = -1
            for j in i:
                
                if(j[0]==self.target):
                    index =  j[1]            
                product *= j[2]
            
            answers[index] += product

        for i in range(len(answers)):
            
            answers[i] = answers[i]/self.sum
            
        print("\n".join(str(round(x, 4)) for x in answers))

        solution = [0]*self.choices

        for key in self.utility:
            temp = key.split(",")
            solution[int(temp[1])] += answers[int(temp[0])] * self.utility[key]
        
        print(solution.index(max(solution)))


# nodes of BBN

class Node:

    def __init__(self, a, b, c):
        self.k = a   # az adott változó által felveheto diszkrét értékek száma
        self.n = b    # szülők indexei (tömbben)
        self.probabilities = c # valószínűségek a szülők által felvett értékekre
        self.need = False # jelöli, hogy szükséges-e a csúcs a számoláshoz

    def needed(self):
        self.need = True

def main():
    
    #beolvasás

    nodes = []
    n = int(input())
    
    for i in range(n):
        parents = []
        prob = {}
        sz = input()
        sz = sz.split("\t")
        for j in range(int(sz[1])):
            parents.append(sz[2+j])

        for j in range(2+int(sz[1]), len(sz)):
            if(int(sz[1])!=0):
                p = sz[j].split(":")
                temp = p[1].split(",")
                
                
                for e in range(len(temp)):
                    temp[e] = float(temp[e])
                prob[p[0]] = temp
            else:
                p = sz[j].split(",")
                for e in range(len(p)):
                    p[e] = float(p[e])
                prob['non'] = p

        node = Node(int(sz[0]), parents, prob)
        
        nodes.append(node)

    evid_num = int(input())
    evidences = {}

    for i in range(evid_num):
        e = input()
        e = e.split("\t")
        evidences[int(e[0])] = int(e[1])

    target = int(input())
    choices_num = int(input())

    utilities = {}

    for i in range(nodes[target].k*choices_num):
        sz = input()
        sz = sz.split("\t")
        utilities[sz[0]+","+sz[1]] = float(sz[2])

    # Bayes háló felvétele és a megfelelő értékek megadása

    bbn = BBN(nodes,evidences,target,choices_num,utilities)
    
    
    # számoláshoz fontos node-ok kigyűjtése
    bbn.important()
    bbn.final()
   
main()


