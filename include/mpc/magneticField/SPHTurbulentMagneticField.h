#ifndef MPC_SPHTURBULENTMAGNETICFIELD_H_
#define MPC_SPHTURBULENTMAGNETICFIELD_H_

#include "mpc/magneticField/TurbulentMagneticField.h"

namespace mpc {

/**
 @class SPHTurbulentMagneticField
 @brief Random turbulent magnetic field on a cubic grid modulated with large scale structure.
 */
class SPHTurbulentMagneticField: public TurbulentMagneticField {
public:
	SPHTurbulentMagneticField(Vector3d origin, size_t samples, double spacing) :
			TurbulentMagneticField(origin, samples, spacing) {
	}
	void modulate(const std::string filename);
};

} // namespace mpc

#endif /* MPC_SPHTURBULENTMAGNETICFIELD_H_ */
