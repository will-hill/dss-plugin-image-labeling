var app = angular.module('labelling.setup.module', []);

app.controller('LabellingSetupController', function($scope) {
    $scope.checkResult = {};
    $scope.check = function() {
        var hasAuthentication = function(config) {
            return config.useToken ? config.token : (config.login && config.password);
        };
        $scope.checkResult = {
            hasAuthentication : hasAuthentication($scope.config)
        };
    };
    $scope.check();
});