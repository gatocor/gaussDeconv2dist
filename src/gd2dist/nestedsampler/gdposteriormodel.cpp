#define _USE_MATH_DEFINES
#include <cmath>
#include <vector>
#include <iostream>
#include "gdposteriormodel.h"

#include "pybind11/pybind11.h"

gdposteriormodel::gdposteriormodel(std::vector<double> datanoise, std::vector<double> dataconvolution, int k, int kc){
    dataNoise = datanoise;
    dataConvolution = dataconvolution;
    K = k;
    Kc = kc;
    x.assign(10000,0);
    normcdf.assign(10000,0);
    for(int i = 0; i < 10000; i++){
        x[i] = i*0.01;
        normcdf[i] = 2*std::exp(-(std::pow(x[i],2)/2))*std::sqrt(1/M_PI/2)*0.01;
    }
    for(int i = 1; i < 10000; i++){
        normcdf[i] += normcdf[i-1];
    }
}

double gdposteriormodel::logLikelihood(std::vector<double>& parameters){
    double likelihood =  0;
    double max = -INFINITY;
    std::vector<double> exponent(K*Kc,0);
    double total = 0;

    for(int i = 0; i < dataNoise.size(); i++){
        //Compute exponents and find the maximum
        max = -INFINITY;
        for(int j = 0; j < K; j++){
            exponent[j] = -std::pow(dataNoise[i]-parameters[K+j],2)/(2*std::pow(parameters[2*K+j],2));
            if (exponent[j] > max){
                max = exponent[j];
            }
        }
        //Compute the
        total = 0;
        for(int j = 0; j < K; j++){
            total += parameters[j]*std::exp(exponent[j]-max)*std::sqrt(1/(2*M_PI*std::pow(parameters[2*K+j],2)));
        }
        likelihood += std::log(total)+max;
    }

    for(int i = 0; i < dataConvolution.size(); i++){
        //Compute exponents and find the maximum
        max = -INFINITY;
        for(int j = 0; j < K; j++){
            for(int k = 0; k < Kc; k++){
                exponent[j*Kc+k] = -std::pow(dataConvolution[i]-parameters[K+j]-parameters[3*K+Kc+k],2)/(2*(std::pow(parameters[2*K+j],2)+std::pow(parameters[3*K+2*Kc+k],2)));
                if (exponent[j*Kc+k] > max){
                    max = exponent[j*Kc+k];
                }
            }
        }
        //Compute the
        total = 0;
        for(int j = 0; j < K; j++){
            for(int k = 0; k < Kc; k++){
                total += parameters[j]*parameters[3*K+k]*std::exp(exponent[j*Kc+k]-max)
                    *std::sqrt(1/(2*M_PI*(std::pow(parameters[2*K+j],2)+std::pow(parameters[3*K+2*Kc+k],2))));
            }
        }
        likelihood += std::log(total)+max;
    }

    return likelihood;
}

std::vector<double> gdposteriormodel::prior(std::vector<double>& uniform){

    std::vector<double> transformed(3*K+3*Kc,0);

    int pos = 0;
    double total = 0;
    //Uniform sphere
    for(int i = 0; i < K; i++){
        pos = 0;
        while(uniform[i] > normcdf[pos] && pos < 9998){
            pos++;
        }
        transformed[i] = abs(x[pos]+x[pos-1])/2;
        total += transformed[i];
    }
    for(int i = 0; i < K; i++){
        transformed[i] /= total;
    }
    //Mean
    transformed[K] = (dataMax-dataMin)*std::pow(uniform[K],1.0/K)+dataMin;
    for(int i = 1; i < K; i++){
        transformed[K+i] = transformed[K+i-1]*std::pow(uniform[K+i],1/(K-i))+dataMin;
    }
    //Std
    for(int i = 0; i < K; i++){
        transformed[2*K+i] = 3*(dataMax-dataMin)*uniform[2*K+i];
    }

    //Uniform sphere
    total = 0;
    for(int i = 0; i < Kc; i++){
        pos = 0;
        while(uniform[3*K+i] > normcdf[pos] && pos < 9998){
            pos++;
        }
        transformed[3*K+i] = abs(x[pos]+x[pos-1])/2;
        total += transformed[3*K+i];
    }
    for(int i = 0; i < Kc; i++){
        transformed[3*K+i] /= total;
    }
    //Mean
    transformed[3*K+Kc] = (dataMax-dataMin)*std::pow(uniform[3*K+Kc],1/K)+dataMin;
    for(int i = 1; i < Kc; i++){
        transformed[3*K+Kc+i] = transformed[3*K+Kc+i-1]*std::pow(uniform[3*K+Kc+i],1/(Kc-i))+dataMin;
    }
    //Std
    for(int i = 0; i < Kc; i++){
        transformed[3*K+2*Kc+i] = 3*(dataMax-dataMin)*uniform[3*K+2*Kc+i];
    }

    return transformed;
}
