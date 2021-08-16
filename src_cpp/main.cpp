#include <unordered_map>
#include "parameters.hpp"
#include "feature.hpp"


int main() {
    std::cout << "Hello, World!" << std::endl;
    FeatureMaker::make_train_feature();
    FeatureMaker::make_test_feature();
    return 0;
}
