# GADGET_INCLUDE_DIR = path to gadget directory
# GADGET_LIBRARY = libGadget.a
# GADGET_FOUND = true if gadget is found

find_path(GADGET_INCLUDE_DIR gadget/SmoothParticle.hpp)
find_library(GADGET_LIBRARY Gadget)

set(GADGET_FOUND FALSE)
if(GADGET_INCLUDE_DIR AND GADGET_LIBRARY)
    set(GADGET_FOUND TRUE)
endif()

mark_as_advanced(GADGET_INCLUDE_DIR GADGET_LIBRARY GADGET_FOUND)

#MESSAGE("GADGET_FOUND=${GADGET_FOUND}\n"
#    "GADGET_LIBRARY=${GADGET_LIBRARY}\n"
#    "GADGET_INCLUDE_DIR=${GADGET_INCLUDE_DIR}")