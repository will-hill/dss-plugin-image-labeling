var app = angular.module('labelling.setup.module', []);

app.controller('FoobarController', function($scope) {
    var updateChoices = function() {
        // the parameter to callPythonDo() is passed to the do() method as the payload
        // the return value of the do() method comes back as the data parameter of the fist function()
        $scope.callPythonDo({}).then(function(data) {
            // success
            $scope.choices = data.choices;
        }, function(data) {
            // failure
            $scope.choices = [];
        });
    };
    updateChoices();
    $scope.$watch('config.filterColumn', updateChoices);
});