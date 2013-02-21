#ifndef MPC_REDSHIFT_H_
#define MPC_REDSHIFT_H_

#include "mpc/Module.h"

#include <vector>

namespace mpc {

/**
 @class SimpleRedshift
 @brief Redshift and adiabatic energy loss using Hubble's law and the distance to an observer.

 Using Hubble's law v = H0*D and the the small redshift approximation v ~ c*z, the redshift is calculated as z ~ H0*D/c.
 It is assumed that the particle starts with a redshift z, that corresponds to its distance to the observer.
 This redshift is reduced with shrinking distance to the observer, and the particle loses energy accordingly.
 Redshift and particle energy are not changed if the distance to the observer grows.
 */
class SimpleRedshift: public Module {
private:
	Vector3d observer; // observer position (z = 0)
	double h; // dimension-free Hubble constant, H0 = h * 100 km/s/Mpc

public:
	SimpleRedshift(Vector3d observer, double h = 0.7);
	void process(Candidate *candidate) const;
	std::string getDescription() const;
};

/**
 @class Redshift
 @brief Calculation of cosmological redshift and adiabatic energy loss

 This module implements the calculation of cosmological redshift for a flat universe.
 It provides two functionalities:
 1) In a simulation chain it reduces the candidate's redshift according to the propagation step and applies the adiabatic energy loss.
 2) It provides translations from redshift to comoving distance and vice versa.
 */
class Redshift: public Module {
private:
	double H0; // Hubble rate at z=0 in [1/s], H0 = h * 100 km/s/Mpc
	double omegaM; // matter density parameter
	double omegaL; // vacuum energy parameter

	static const int n = 1000;
	static const double zmin = 0.0001;
	static const double zmax = 100;

	std::vector<double> Z; // redshift
	std::vector<double> Dc; // comoving distance [m]
	std::vector<double> Dl; // luminosity distance [m]
	std::vector<double> Dt; // light travel distance [m]

public:
	/** Constructor
	 @param	h		dimension-free Hubble constant, H0 = h * 100 km/s/Mpc
	 @param omegaM	matter density parameter
	 @param omegaL	vacuum energy parameter
	 */
	Redshift(double h = 0.7, double omegaM = 0.3, double omegaL = 0.7);
	void process(Candidate *candidate) const;
	std::string getDescription() const;

	/**
	 Hubble rate at given redshift
	 H(z) = H0 * sqrt(omegaM * (1 + z)^3 + omegaL)
	 */
	double hubbleRate(double redshift) const;
	/**
	 Dimensionless Hubble parameter at given redshift
	 E(z) = sqrt(omegaM * (1 + z)^3 + omegaL)
	 */
	double hubbleParameter(double redshift) const;

	/**
	 Redshift of a comoving object at a given comoving distance to an observer at z = 0.
	 d_comoving(z) = c/H0 * int_0^z dz' / E(z')
	 */
	double comovingDistance2Redshift(double distance) const;
	/**
	 Comoving distance between an observer at z = 0 and a comoving object at z.
	 d_comoving(z) = c/H0 * int_0^z dz' / E(z')
	 */
	double redshift2ComovingDistance(double redshift) const;

	/**
	 Redshift of a comoving object at a given luminosity distance to an observer at z = 0.
	 d_luminosity(z) = (1 + z) * d_comoving(z)
	 */
	double luminosityDistance2Redshift(double distance) const;
	/**
	 Luminosity distance between an observer at z = 0 and a comoving object at z.
	 d_luminosity(z) = (1 + z) * d_comoving(z)
	 */
	double redshift2LuminosityDistance(double redshift) const;

	/**
	 Redshift of a comoving object at a given light travel distance to an observer at z = 0.
	 d_lighttravel(z) = c/H0 * int_0^z dz' / ((1 + z')  *  E(z'))
	 */
	double lightTravelDistance2Redshift(double distance) const;
	/**
	 Light travel distance between an observer at z = 0 and a comoving object at z.
	 d_lighttravel(z) = c/H0 * int_0^z dz' / ((1 + z')  *  E(z'))
	 */
	double redshift2LightTravelDistance(double redshift) const;
};

} // namespace mpc

#endif /* MPC_REDSHIFT_H_ */
