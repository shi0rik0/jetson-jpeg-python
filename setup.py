# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [
    Pybind11Extension(
        name="jetson_jpeg",
        sources=[
            "src/main.cpp",
            '/usr/src/jetson_multimedia_api/samples/common/classes/NvJpegEncoder.cpp',
            '/usr/src/jetson_multimedia_api/samples/common/classes/NvBuffer.cpp',
            '/usr/src/jetson_multimedia_api/samples/common/classes/NvElement.cpp',
            '/usr/src/jetson_multimedia_api/samples/common/classes/NvElementProfiler.cpp',
            '/usr/src/jetson_multimedia_api/samples/common/classes/NvLogging.cpp',
        ],
        include_dirs=[
            '/usr/src/jetson_multimedia_api/include',
            '/usr/src/jetson_multimedia_api/include/libjpeg-8b',
            '/usr/src/jetson_multimedia_api/samples/common/algorithm/cuda',
            '/usr/src/jetson_multimedia_api/samples/common/algorithm/trt',
            '/usr/local/cuda/include', '/usr/include/aarch64-linux-gnu',
            '/usr/include/libdrm', '/usr/include/opencv4'
        ],
        library_dirs=['/usr/lib/aarch64-linux-gnu/tegra'],
        libraries=['nvjpeg'],
    ),
]

setup(
    name="jetson_jpeg",
    version='0.0.1',
    author="shi0rik0",
    url="https://github.com/shi0rik0/jetson-jpeg-python",
    description="A Jetson JPEG API Python binding using pybind11.",
    long_description="",
    ext_modules=ext_modules,
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
)
