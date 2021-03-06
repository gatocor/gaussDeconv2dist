#ifndef GD_POSTERIOR_MODEL
#define GD_POSTERIOR_MODEL

#include <vector>

class gdposteriormodel{
    public:
        std::vector<double> dataNoise;
        std::vector<double> dataConvolution;
        int K;
        int Kc;
        double dataMin;
        double dataMax;
        gdposteriormodel(std::vector<double>,std::vector<double>,int, int);
        double logLikelihood(std::vector<double>&);
        std::vector<double> prior(std::vector<double>&);
        std::vector<double> x;
        std::vector<double> normcdf;
};

#endif