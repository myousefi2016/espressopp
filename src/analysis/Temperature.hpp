#ifndef _ANALYSIS_TEMPERATURE_HPP
#define _ANALYSIS_TEMPERATURE_HPP

#include "types.hpp"
#include "Observable.hpp"

namespace espresso {
  namespace analysis {
    /** Class to compute the temperature. */
    class Temperature : public Observable {
    public:
      Temperature(shared_ptr< storage::Storage > storage) : Observable(storage) {}
      ~Temperature() {}
      virtual real compute() const;
      //virtual real time_average() const;
    };
  }
}

#endif