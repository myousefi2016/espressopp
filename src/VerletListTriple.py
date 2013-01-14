from espresso import pmi
import _espresso 
import espresso
from espresso.esutil import cxxinit

class VerletListTripleLocal(_espresso.VerletListTriple):
    'The (local) verlet triple list'

    def __init__(self, system, cutoff, exclusionlist=[]):
        'Local construction of a verlet triple list'
        if pmi.workerIsActive():
          '''
          cxxinit(self, _espresso.VerletListTriple, system, cutoff, True)
          if (exclusionlist != []):
            print 'Warning! Exclusion list is not yet implemented to the triple verlet \
                  list. Nothing happend to exclusion list'
          '''

          if (exclusionlist == []):
            # rebuild list in constructor
            cxxinit(self, _espresso.VerletListTriple, system, cutoff, True)
          else:
            # do not rebuild list in constructor
            cxxinit(self, _espresso.VerletListTriple, system, cutoff, False)
            # add exclusions
            for pid in exclusionlist:
                self.cxxclass.exclude(self, pid)
            # now rebuild list with exclusions
            self.cxxclass.rebuild(self)
            
    def totalSize(self):
        'count number of triples in VerletListTriple, involves global reduction'
        if pmi.workerIsActive():
            return self.cxxclass.totalSize(self)
        
    def localSize(self):
        'count number of triples in local VerletListTriple'
        if pmi.workerIsActive():
            return self.cxxclass.localSize(self)
        
    def exclude(self, exclusionlist):
        """
        Each processor takes the broadcasted exclusion list
        and adds it to its list.
        if pmi.workerIsActive():
          print 'Warning! Exclusion list is not yet implemented to the triple verlet \
                list. Nothing happend'
        """
        for pid in exclusionlist:
            self.cxxclass.exclude(self, pid)
        # rebuild list with exclusions
        self.cxxclass.rebuild(self)
            
    def getAllTriples(self):
        'return the triples of the local verlet list'
        if pmi.workerIsActive():
            triples=[]
            ntriples=self.localSize()
            for i in range(ntriples):
              triple=self.cxxclass.getTriple(self, i+1)
              triples.append(triple)
            return triples


if pmi.isController:
  class VerletListTriple(object):
    __metaclass__ = pmi.Proxy
    pmiproxydefs = dict(
      cls = 'espresso.VerletListTripleLocal',
      pmiproperty = [ 'builds' ],
      pmicall = [ 'totalSize', 'exclude', 'connect', 'disconnect', 'getVerletCutoff' ],
      pmiinvoke = [ 'getAllTriples' ]
    )
