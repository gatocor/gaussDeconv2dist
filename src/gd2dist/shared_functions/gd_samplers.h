#ifndef GD_SAMPLERS
#define GD_SAMPLERS

#include <vector>
#include <random>

//Samplers autofluorescence
std::vector<double> sample_autofluorescence(std::vector<std::vector<double>>&, int, int, int);
std::vector<double> sample_autofluorescence(std::vector<std::vector<double>>&, int, int, std::vector<double>&, int);

//Samplers deconvolution
std::vector<double> sample_deconvolution(std::vector<std::vector<double>>&, int, int, int);
std::vector<double> sample_deconvolution(std::vector<std::vector<double>>&, int, int, std::vector<double>&, int);

//Samplers convolution
std::vector<double> sample_convolution(std::vector<std::vector<double>>&, int, int, int);
std::vector<double> sample_convolution(std::vector<std::vector<double>>&, int, int, std::vector<double>&, int);

//Samplers autofluorescence
std::vector<double> sample_autofluorescence_single(std::vector<std::vector<double>>&, int, int, int, int);
std::vector<double> sample_autofluorescence_single(std::vector<std::vector<double>>&, int, int, std::vector<double>&, int, int);

//Samplers deconvolution
std::vector<double> sample_deconvolution_single(std::vector<std::vector<double>>&, int, int, int, int);
std::vector<double> sample_deconvolution_single(std::vector<std::vector<double>>&, int, int, std::vector<double>&, int, int);

//Samplers convolution
std::vector<double> sample_convolution_single(std::vector<std::vector<double>>&, int, int, int, int);
std::vector<double> sample_convolution_single(std::vector<std::vector<double>>&, int, int, std::vector<double>&, int, int);

#endif