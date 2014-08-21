from mnfit.mnSpecFit.Model import Model
from numpy import exp, power, zeros
from mnfit.priorGen import *








class BB(Model):

   def __init__(self):




      def bb(x,logA,kT):
         
         val = power(10.,logA)*power(x,2.)*power( exp(x/float(kT)) -1., -1.)
         return val



      self.paramsRanges = [[1.E-6,1.E3,"J"],[1.E2,1.E5,"U"],[-2.,1.,"U"],[-10.,-2,"U"]]
     



      def BBPrior(params, ndim, nparams):

         for i in range(ndim):
            params[i] = priorLU[self.paramsRanges[i][-1]](params[i],self.paramsRanges[i][0],self.paramsRanges[i][1])
     

      
      self.modName = "blackbody"
      self.model=bb
      self.prior=BBPrior
      self.n_params = 2
      self.parameters = [r"logN$_{\rm BB}$","kT"]

      self._modelDict = {"params":self.parameters,\
                         "model":bb\
      }
      self._composite = False
