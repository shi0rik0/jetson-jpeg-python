#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <NvJpegEncoder.h>
#include <NvBuffer.h>
#include <memory>

using namespace std;
namespace py = pybind11;


class JpegEncoder {
public:
    JpegEncoder() {
        encoder = unique_ptr<NvJPEGEncoder>(NvJPEGEncoder::createJPEGEncoder("jpenenc"));
    }

    py::array_t<uint8_t> encode(py::array_t<uint8_t> image, int width, int height, int quality) {
        if (image.ndim() != 1) {
            throw std::runtime_error("Input image must be a 1D array");
        }
        py::buffer_info buf_info = image.request();
        ssize_t len = buf_info.size;
        NvBuffer buffer(V4L2_PIX_FMT_YUV420M, width, height, 0);
        buffer.allocateMemory();
        ssize_t j = 0;
        for (uint32_t i = 0; i < buffer.n_planes; ++i)
        {
            NvBuffer::NvBufferPlane &plane = buffer.planes[i];
            uint32_t bytes_per_pixel = plane.fmt.bytesperpixel;
            uint32_t width = plane.fmt.width;
            uint32_t height = plane.fmt.height;
            plane.bytesused = width * height * bytes_per_pixel;
            if (len - j < plane.bytesused) {
                throw std::runtime_error("Not enough data in the input image to fill the buffer");
            }
            uint8_t *data = plane.data;
            auto r = image.unchecked<1>();
            for (uint32_t k = 0; k < plane.bytesused; ++k) {
                data[k] = r(j + k);
            }
            j += plane.bytesused;
        }

        unsigned long out_buf_size = width * height * 3 / 2;
        uint8_t *out_buf = new uint8_t[out_buf_size];
        encoder->encodeFromBuffer(buffer, JCS_YCbCr, &out_buf, out_buf_size, quality);

        return py::array_t<uint8_t>(out_buf_size, out_buf);
    }

private:
    unique_ptr<NvJPEGEncoder> encoder = nullptr;
};


PYBIND11_MODULE(jetson_jpeg, m) {
    py::class_<JpegEncoder>(m, "JpegEncoder")
        .def(py::init<>())
        .def("encode", &JpegEncoder::encode);
}
