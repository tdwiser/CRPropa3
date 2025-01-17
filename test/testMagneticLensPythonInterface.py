import sys

try:
    import unittest
except:
    print("***********************************************************")
    print("* WARNING!! Couldn't import python unittesting framework! *")
    print("* No python tests have been executed                      *")
    print("***********************************************************")
    sys.exit(0)

try:
    import crpropa
except Exception as e:
    print("*** CRPropa import failed")
    print(type(e), str(e))
    sys.exit(-1)

from crpropa import EeV


class testPixelizationConsistency(unittest.TestCase):
    def testPixelizationInterface(self):
        p = crpropa.Pixelization(4)
        rd = p.pix2Direction(42)
        pix = p.direction2Pix(*rd)
        self.assertEqual(pix, 42)

        for i in range(p.getNumberOfPixels()):
            rd = p.getRandomDirectionInPixel(i)
            pix = p.direction2Pix(*rd)
            self.assertEqual(pix, i)

    def testConsistencyWithHealpy(self):
        try:
            import healpy
        except ImportError:
            print("Consistency with healpy not tested as healpy is not "
                  "available")
            return
        p = crpropa.Pixelization(4)
        from numpy import linspace
        from math import pi
        for theta in linspace(0, pi):
            for phi in linspace(-pi, pi):
                crpropaIdx = p.direction2Pix(phi, pi / 2 - theta)
                hpIdx = healpy.ang2pix(2 ** 4, theta, phi)
                self.assertEqual(crpropaIdx, hpIdx)


class testParticleMapsContainer(unittest.TestCase):
    def setUp(self):
        self.maps = crpropa.ParticleMapsContainer()

    def testAddParticle(self):
        self.maps.addParticle(12, 1 * EeV, 0, 0)
        try:
            import numpy as np
        except:
            print("Cannot import numpy. Not testing testAddParticles!")
            return

        self.assertEqual(len(self.maps.getParticleIds()), 1)
        self.assertEqual(self.maps.getParticleIds()[0], 12)
        self.assertEqual(len(self.maps.getEnergies(12)), 1)

    def testAddParticlesNumpyInterface(self):
        try:
            import numpy as np
        except:
            print("Cannot import numpy. Not testing testAddParticlesNumpyInterface!")
            return


        N = 13
        ids = np.ones(N, dtype='i')
        lats = np.random.rand(N) * np.pi - np.pi/2.
        lons = np.random.rand(N) * np.pi * 2. - np.pi
        energy = 10 ** (18 + np.random.rand(N) * 3.) * crpropa.eV
        weights = np.ones(N) / N
        self.maps.addParticles(ids, energy, lons, lats, weights )

        crMap = np.zeros(49152)
        for pid in self.maps.getParticleIds():
            energies = self.maps.getEnergies(int(pid))
            for i, energy in enumerate(energies):
                crMap += self.maps.getMap(int(pid), energy * crpropa.eV)
        self.assertAlmostEqual(sum(crMap), 1.)


    def testAddParticlesNumpyInterfaceIDType(self):
        try:
            import numpy as np
        except:
            print("Cannot import numpy. Not testing testAddParticlesNumpyInterface!")
            return

        N = 13
        lats = np.random.rand(N) * np.pi - np.pi/2.
        lons = np.random.rand(N) * np.pi * 2. - np.pi
        energy = 10 ** (18 + np.random.rand(N) * 3.) * crpropa.eV
        weights = np.ones(N) / N

        # raise on flaot
        ids = np.ones(N, dtype='f')
        self.assertRaises(Exception, self.maps.addParticles, ids, energy, lons, lats, weights )

        # accept int32 and int64
        ids = np.ones(N, dtype='int32')
        self.maps.addParticles(ids, energy, lons, lats, weights )
        self.assertEqual(self.maps.getParticleIds()[0], ids[0])

        ids = np.ones(N, dtype='int64')
        self.maps.addParticles(ids, energy, lons, lats, weights)
        self.assertEqual(self.maps.getParticleIds()[0], ids[0])

    def testAddParticleVectorInterface(self):
        try:
            import numpy as np
        except:
            print("Cannot import numpy. Not testing AddParticleVectorInterface!")
            return

        self.maps.addParticle(12, 1 * EeV, crpropa.Vector3d(1, 0, 0))
        self.assertEqual(len(self.maps.getParticleIds()), 1)
        self.assertEqual(self.maps.getParticleIds()[0], 12)
        self.assertEqual(len(self.maps.getEnergies(12)), 1)

    def testGetRandomParticlesInterface(self):
        try:
            import numpy as np
        except:
            print("Cannot import numpy. Not testing RandomParticlesInterface!")
            return


        self.maps.addParticle(12, 1 * EeV, 0, 0)
        ids, energies, lons, lats = self.maps.getRandomParticles(10)
        self.assertEqual(len(ids), 10)
        self.assertEqual(len(energies), 10)
        self.assertEqual(len(lons), 10)
        self.assertEqual(len(lats), 10)

    def testGetRandomparticlesStatistic(self):
        msg = "Note that this is a statistical test. It might fail by chance "
        "with a probabilty O(0.0027)! You should rerun the test to make "
        "sure there is a bug."

        try:
            import numpy as np
        except:
            print("Cannot import numpy. Not testing RandomParticles!")
            return

        self.maps.addParticle(12, 1*EeV, 0, 0, 1)
        self.maps.addParticle(12, 10*EeV, 0, 0, 1000)
        self.maps.addParticle(2, 1*EeV, 0, 0, 1000)
        self.maps.addParticle(2, 10*EeV, 0, 0, 1)

        Ntot = 10000
        ids, energies, lons, lats = self.maps.getRandomParticles(Ntot)

        n12 = len(np.where(ids == 12))
        n2 = len(np.where(ids == 2))

        # we expect n12 = n2 = Ntot/2, with uncertainty sqrt(Ntot/2)
        self.assertTrue(np.abs(n12 - n2) < 3. * np.sqrt(Ntot/2.), msg=msg)

        # half of the sample should be with E = 1
        nle = len(np.where(energies < 5E18)[0])
        self.assertTrue(np.abs(nle - Ntot / 2.) < 3. * np.sqrt(Ntot / 2.),
                        msg=msg)

    def testNumpyMapAccess(self):
        try:
            import numpy as np
        except:
            print("Cannot import numpy. Not testing NumpyMapAccess!")
            return

        self.maps.addParticle(12, 1*EeV, 0, 0, 1)
        self.maps.addParticle(12, 10*EeV, 0, 0, 1000)
        self.maps.addParticle(2, 1*EeV, 0, 0, 1000)
        self.maps.addParticle(2, 10*EeV, 0, 0, 1)
        # stack all maps
        crMap = np.zeros(49152)
        for pid in self.maps.getParticleIds():
            energies = self.maps.getEnergies(int(pid))
            for i, energy in enumerate(energies):
                crMap += self.maps.getMap(int(pid), energy * crpropa.eV)
        self.assertTrue(isinstance(crMap, np.ndarray))

if __name__ == '__main__':
    unittest.main()
