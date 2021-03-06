from mnfit.mnfit import mnfit
from mnfit.mnPulseFit.PulseModel import PulseModel
from mnfit.mnPulseFit.LightCurve import LightCurve
from mnfit.mnSpecFit.pgstat import pgstat
from mnfit.mnPulseFit.chi2 import chi2


from numpy import array
from astropy.table import Table
import json

class mnPulseFit(mnfit):


    def LoadData(self,lightcurveFile):
        '''
        This member loads a light curve object. The lightcurve object
        is either built from TTE data or from flux points. depending on 
        which, a statistics is chosen. Chi2 for flux data and pgstat for 
        TTE data.

        '''
        self._customTI = False

        #Load the LC object and check is type
        self.lightcurve = LightCurve()
        self.lightcurve.ReadData(lightcurveFile)


        
        #Choose a statistic
        if self.lightcurve.lcType == "TTE":
            self.stat = pgstat()
        else:
            self.stat = chi2()


        self._dataLoaded = True #Mark that data are loaded

        pass




    


    



            


    def SetSaveFile(self,savefile):
        '''
        Set the name of the json file to be created
        after the fit is made

        ____________________________________________________________
        arguments:
        savefile: str() file name


        '''
        self.savefile = savefile
        self._saveFileSet = True

    def SetPulseModel(self, model):
        '''
        Pass a model class which will be instantiated
        

        _____________________________________________________________
        arguments:
        model: a derived Model class

        '''
        self.pModel = model()
        
        self.n_params = self.pModel.n_params

        pass



    def SetTimeInterval(self,tmin,tmax):

        self.tmin = tmin
        self.tmax = tmax
        self._customTI = True

        
        

    def ConstructLikelihood(self):
        '''
        Provides a likelihood function based off the data and
        model provided. This function is fed to MULTINEST.

        '''

        # The Likelihood function for MULTINEST

        if self._customTI:
            self.lightcurve.SetTimeInterval(self.tmin,self.tmax)
        def likelihood(cube, ndim, nparams):


            params = array([cube[i] for i in range(ndim)])
            logL = 0. # This will be -2. * log(L)

            self.pModel.SetTimes(self.lightcurve.GetTimeBins())
            #Calculates the model counts based off the params
            self.pModel.SetParams(params)

            self.stat.SetModelCounts(self.pModel.GetModelCounts())
            

            if self.lightcurve.lcType == "TTE":

                self.stat.SetCounts(self.lightcurve.GetCounts()+self.lightcurve.GetBkg())
                self.stat.SetBackGround(self.lightcurve.GetBkg(),self.lightcurve.GetBkgErr())
                binWidths = self.lightcurve.binStop-self.lightcurve.binStart

                #######THIS IS TMP
                self.stat.ts = binWidths[0]
                self.stat.tb = binWidths[0]
                
            else:
                self.stat.SetCounts(self.lightcurve.GetCounts())
                self.stat.SetErrors(self.lightcurve.GetErr())
                
            logL = self.stat.ComputeLikelihood()


            
            #calculate the statistic
            
            

            
            jointLH = -0.5*(logL)
            #jointLH = logL    
            return jointLH
        
        # Becuase this is inside a class we want to create a
        # likelihood function that does not have an object ref
        # as an argument, so it is created here as a callback

        self.likelihood = likelihood  #likelihood callback
        self.prior = self.pModel.prior  #prior callback



    def _WriteFit(self):
        '''
        Private function that is called after running MULTINEST.
        It saves relevant information from the fits

        '''


        dof = len(self.lightcurve.GetTimeBins())-self.n_params

        # need to subtract off the number of fit params

        
        
       # Construct the dictionary that will be read by
       # SpecFitView.
        out = {"outfiles":self.outfilesDir,\
               "basename":self.basename,\
               "duration":self.lightcurve.duration,\
               "params":self.pModel.parameters,\
               "lightCurve":self.lightcurve.fileName,\
               "model":self.pModel.modName,\
               "stat":self.stat.statName,\
               "dof":dof,\
               "emin":self.lightcurve.emin,\
               "emax":self.lightcurve.emax,\
               "tmin":self.tmin,\
               "tmax":self.tmax\
        }

        f = open(self.outfilesDir+self.savefile,'w')
        
        json.dump(out,f) # Write to a JSON file
        print
        print "Wrote "+self.outfilesDir+self.savefile
        print
        print
        
        f.close()

        

    def _PreFitInfo(self):

        print "Starting fit of model:"
        print "\t%s"%self.pModel.modName
        print

