from Model import Model
from numpy import exp, power









class PL2BB(Model):

   def __init__(self):



      

      def pl2bb(x,logA1,kT1,logA2,kT2,logA3,index):




          #BB1
          val = power(10.,logA1)*power(x,2)*power( exp(x/float(kT1)) -1.,-1.)

          val += power(10.,logA2)*power(x,2)*power( exp(x/float(kT2)) -1.,-1.)

          val += power(10.,logA3)*power(x/300.,index)
          
          return val
        
        



      def PL2BBPrior(params, ndim, nparams):
         
         params[0] = -8*params[0]
         params[1] = 1.99E3*params[1]+1E1 #keV
         params[2] = -8*params[2]
         params[3] = 1.99E3*params[3]+1.E0 #keV
         params[4] = -8.*params[4]
         params[5] = 5.*params[5]-3.
         pass

       

      self.modName = "PL2BB"
      self.model=pl2bb
      self.prior=PL2BBPrior
      self.n_params = 6
      self.parameters = [r"logN$_{\rm BB1}",r"kT1",r"logN$_{\rm BB2}",r"kT",r"logN$_{\rm PL}","index"]