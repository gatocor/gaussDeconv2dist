#define _USE_MATH_DEFINES
#include <cmath>
#include <random>

double
gamma_pdf(double x, double theta, double k, double bias){
    return -(x+bias)/theta+(k-1)*std::log(x+bias)-k*std::log(theta)-std::lgamma(k);
}

double
gamma_sum_pdf(double x, double theta1, double k1, double theta2, double k2, double bias, int precission = 1){
    double aux;
    //Exchange if necessary theta1 = min(theta_i)
    if(theta1 > theta2){
        aux = theta1;
        theta1 = theta2;
        theta2 = aux;

        aux = k1;
        k1 = k2;
        k2 = aux;
    }
    //Make C
    double C = std::pow(theta1/theta2,k2);
    //Make gamma_k vector
    std::vector<double> gammas(precission,0);
    for (int i = 0; i < precission; i++){
        gammas[i] = k2*std::pow(1-theta1/theta2,i)/i;
    }
    //Make rho
    double rho = k1+k2;
    //Make delta_k vector
    std::vector<double> deltas(precission,0);
    deltas[0] = 1;
    for (int i = 1; i < precission; i++){
        deltas[i] = i*gammas[i]*deltas[i-1]/i;
    }
    //Make sum
    std::vector<double> exponent(precission,0);
    double max = -INFINITY;
    for( int i = 0; i < precission; i++){
        exponent[i] = -(x+bias)/theta1+(rho+i-1)*std::log(x+bias)-(rho+i)*std::log(theta1)-std::lgamma(rho+i)+std::log(deltas[i]);
        if(exponent[i]>max){
            max = exponent[i];
        }
    }

    double likelihood = 0;
    for(int i = 0; i < precission; i++){
        likelihood += std::exp(exponent[i]-max);
    }

    likelihood = std::log(likelihood) + max + std::log(C);

    return likelihood;
}

double
gaussian_pdf(double x, double mu, double sigma){
    return  - std::pow( x - mu , 2 ) / ( 2 * std::pow( sigma , 2 ) )  - std::log( std::sqrt( 2 * M_PI) * sigma );
}

void
multinomial_1(std::mt19937 &r, std::vector<double> & p, std::vector<int> & x){
    double cum = 0;
    double tot = 0;
    int pos = 0;
    int l = p.size();
    std::uniform_real_distribution<double> distribution(0.0,1.0);

    //Normalize
    for ( int i = 0 ; i < l ; i++ ){
        tot += p[i];
    }
    //Sample
    double v = tot * distribution(r);
    for ( int i = 0 ; i < l ; i++){
        cum += p[i];
        if ( cum > v ){
            x[i] = 1;
            pos = i;
            break;
        }else{
            x[i] = 0;
        }
    }
    for ( int i = pos + 1 ; i < l ; i++){
        x[i] = 0;
    }

    return;
}

void
dirichlet(std::mt19937 & r, std::vector<double> & a, std::vector<double> & x){
    int l = a.size();
    double tot = 0;

    //Sample gamma
    for ( int i = 0; i < l; i++ ){
        std::gamma_distribution<double> gamma(a[i],1);
        x[i] = gamma(r);
        tot += x[i];
    }
    //Normalize
    for ( int i = 0; i < l; i++ ){
        x[i] /= tot;
    }

    return;
}
