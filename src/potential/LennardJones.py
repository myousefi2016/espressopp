from espresso import pmi
from espresso.esutil import *

from espresso.potential.CentralPotential import *
from _espresso import potential_LennardJones

class LennardJonesLocal(CentralPotentialLocal, potential_LennardJones):
    'The (local) Lennard-Jones potential.'
    def __init__(self, epsilon=1.0, sigma=1.0, cutoff=2.0) :
        """Initialize the local Lennard Jones object."""
        cxxinit(self, potential_LennardJones, epsilon, sigma, cutoff)

if pmi.IS_CONTROLLER:
    pmi.exec_('import espresso.potential')
    class LennardJones(CentralPotential):
        'The Lennard-Jones potential.'
        pmiproxydefs = CentralPotential.pmiproxydefs
        pmiproxydefs['class'] = 'espresso.potential.LennardJonesLocal'
        pmiproxydefs['pmiproperty'] = [ 'epsilon', 'sigma', 'cutoff' ]
