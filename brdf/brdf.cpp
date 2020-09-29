#define POWITACQ_IMPLEMENTATION 1
#include "powitacq_rgb.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

POWITACQ_NAMESPACE_BEGIN
//using namespace powitacq_rgb;
PYBIND11_MODULE(brdf, m) {
    py::class_<BRDF>(m, "BRDF")
        .def(py::init<const std::string &>())
        .def("eval", &BRDF::eval);
    py::class_<Vector3f>(m, "vec3f")
        .def(py::init<>());
}
POWITACQ_NAMESPACE_END
