# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics
# Name:  John Kautzner
# Collaborators:  None
# Time:  3:15

import numpy
import random
import pylab

'''
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        return random.random() <= self.clearProb


    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        if(random.random() <= self.maxBirthProb*(1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        raise NoChildException


class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop


    def getTotalPop(self):

        """
        Gets the current total virus population.
        returns: The total virus population (an integer)
        """

        return len(self.viruses)



    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.
        - The current population density is calculated. This population density
          value is used until the next call to update()
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """

        for v in self.viruses:
            if v.doesClear():
                self.viruses.remove(v)

        popDensity = float(self.getTotalPop())/float(self.maxPop)

        for v in self.viruses:
            try:
                self.viruses.append(v.reproduce(popDensity))
            except NoChildException:
                pass

        return self.viruses



#
# PROBLEM 2
#
# def simulationWithoutDrug():
#
#     """
#     Run the simulation and plot the graph for problem 2 (no drugs are used,
#     viruses do not have any drug resistance).
#     Instantiates a patient, runs a simulation for 300 timesteps, and plots the
#     total virus population as a function of time.
#     """
#
#     # TODO


#
# PROBLEM 3 (apparently)
#

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    sumTrials = [0]*300

    for i in range(numTrials):
        thisTrial = runSimulation(numViruses, maxPop, maxBirthProb, clearProb)
        # Sets thisTrial to a list of int.  Each int represents the number of viruses at the given step.

        for j in range(300):
            sumTrials[j] += thisTrial[j]

    avgPop = [0]*300
    for i in range(300):
        avgPop[i] = sumTrials[i]/float(numTrials)

    plot("Average Virus Population Per Time Step", avgPop, "Time Steps", "Number of Viruses")
    return avgPop


def runSimulation (numViruses, maxPop, maxBirthProb, clearProb):
    """ helper function for doing one simulation run
        Returns list of virus population at the end of every step """

    viruses = [SimpleVirus(maxBirthProb, clearProb)]*numViruses

    patient = SimplePatient(viruses, maxPop)

    virusesEachStep = [numViruses]

    for i in range(300):
        virusesEachStep.append(len(patient.update()))

    return virusesEachStep


def plot(title, yVals, xAxis, yAxis):

    pylab.title(title)
    pylab.xlabel(xAxis)
    pylab.ylabel(yAxis)

    pylab.plot(yVals)
    pylab.show()

#runSimulation(100, 10000, .1, .05)
#simulationWithoutDrug(100, 10000, .1, .05, 5)
#plot("Title Here", [50]*300, "X-Axis", "Y-Axis")

#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb


    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        self.resistances(drug)


    def isResistantToAll (self, drugList):
        """ Helper function that checks if virus is resistant to all the drugs
            in drugList """

        for drug in drugList:
            if(self.resistances(drug) == False):
                return False

        return True


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability (1 - mutProb) of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait on in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        newResistances = {}

        if(not self.isResistantToAll(activeDrugs)):
            raise NoChildException

        else:
            if(random.random() > self.maxBirthProb * (1 - popDensity)):
                raise NoChildException

            else:

                for drug in self.resistances:
                    if(random.random() <= self.mutProb):
                        newResistances[drug] = not self.resistances[drug]

                    else:
                        newResistances[drug] = self.resistances[drug]

                child = ResistantVirus(self.maxBirthProb, self.clearProb, newResistances, self.mutProb)
                return child



class TreatedPatient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop
        self.activeDrugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.activeDrugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        pop = 0

        for v in self.viruses:
            if v.isResistantToAll(drugResist):
                pop += 1

        return pop


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        children = []

        # Removes viruses that don't survive.
        for v in self.viruses:
            if not v.isResistanttoAll(self.activeDrugs):
                self.viruses.remove(v)

        popDensity = float(len(self.viruses))/float(self.maxPop)

        # Appends children to the list of viruses.
        for v in self.viruses:
            try:
                children += [v.reproduce(popDensity, self.activeDrugs)]
            except NoChildException:
                pass

        self.viruses += children

        return len(self.viruses)


#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTrials: number of simulation runs to execute (an integer)

    """

    # TODO


def runDrugSimulation (numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numStepsBeforeDrugApplied, totalNumSteps):
    """ Helper function for doing one actual simulation run with drug applied """

    # TODO
