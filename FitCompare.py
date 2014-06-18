from pymultinest import Analyzer
import numpy as np


class FitCompare(object):
    '''
    Compare evidences from mnfit chains
    '''
    def __init__(self,fits):
        '''
        Loads the fits and creates an array of analyzers
        to compare with

        '''

        analyzers = []
        modelnames = []
        parameters = []

        # Loop over the loaded chains and fit files
        for f in fits:

            self._LoadData(f) #method should attach self.modelnames and self.parameters

            anal = Analyzer(n_params=self.n_params,outputfiles_basename=self.basename)
            analyzers.append(anal)  #Gather the analyzers
            modelnames.append(self.modName)  #Gather the model names
            parameters.append(self.parameters)  #Gather the parameter names of the models


        self.analyzers = analyzers
        self.modelnames = modelnames
        self.parameters = parameters

        #Call the private functions
        self._Evidence() #Compute logZ for each model
        self._SortModels()  # Sort the models based on logZ
        self._EvidenceMatrix() # Calculate the bayes factors
        self._PrintResults()
        
    def _Evidence(self):
        '''
        Compute evidence for loaded models
        '''
        self.logZ = [] 
        
        for a in self.analyzers:


            s = a.get_stats()
            logZ = s['global evidence']/np.log(10.)
            self.logZ.append(logZ)



    
    
    def _SortModels(self):
        '''
        Sort the models based on the logZ
        '''

        results = zip(self.modelnames, self.parameters, self.analyzers, self.logZ)
        modelnames  = self.modelnames
        parameters  = self.parameters
        analyzers   = self.analyzers
        logZ        = self.logZ

        #results = sorted(results, key=lambda (self.modelnames, self.parameters, self.analyzers, self.logZ): self.logZ)
        results = sorted(results, key=lambda (modelnames, parameters, analyzers, logZ): logZ)

        self.results = results


    def _EvidenceMatrix(self):
        '''
        Create a matrix of the Bayes factors betweent eh various
        loaded models
        '''

        deltaZ = []
        for i in range(len(self.results)):

            hiZ=self.results[i][3]

            for j in range(i):

                loZ = self.results[j][3]

                dZ  = hiZ - loZ
                deltaZ.append(dZ)

        self.deltaZ = deltaZ

    def _PrintResults(self):

        #First print best models
        print
        print
        print
        print "_"*73
        print "_"*30 + "Model Rankings"+"_"*30
        print
        print "Model:\tlogZ:"
        print "------\t-----"
        for i in range(len(self.results) -1):
            print "%s\t%.2f"%(self.results[i][0],self.results[i][3])
        print "%s\t%.2f\t<---- BEST MODEL"%(self.results[-1][0],self.results[-1][3])

        print

        print "_"*30 + "Bayes Factors"+"_"*30
        print
        k=0
        rows = []
        maxNameLength = max(map(len,self.modelnames))

        for res in self.results:
            name=res[0]
            space = maxNameLength-len(name)
            rows.append(name+" "*space+"|")

        s=" "*(maxNameLength+1)
        for i in range(len(self.results)):
            s+=self.results[i][0]+"\t"
            for j in range(len(self.results)):
                if i > j:
                    rows[j]+="%.1f\t"%self.deltaZ[k]
                    k+=1
                else:
                    rows[j]+='-\t'
        print s
        print " "*(maxNameLength+1)+"-"*len(s)
        for r in rows:
            print r
        print
        print "_"*73