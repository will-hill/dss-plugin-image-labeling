var app = angular.module('labelling.setup.module', []);

app.controller('LabellingSetupController', function($scope) {
    $scope.folderParam = {"type":"FOLDER", "name":"folder", "label":"Images", "description":"Folder containing the images to label", "mandatory": true, "canSelectForeign": true};
    $scope.datasetParam = {"type":"DATASET", "name":"dataset", "label":"Labels", "description":"Dataset to save the labels into", "mandatory": true, "canSelectForeign": false};
    $scope.categoriesParam = {"name": "categories", "type": "KEY_VALUE_LIST", "label": "Categories", "description": "Category name → optional description", "mandatory": true}
    var checkDataset = function() {
        // the parameter to callPythonDo() is passed to the do() method as the payload
        // the return value of the do() method comes back as the data parameter of the fist function()
        $scope.callPythonDo({'check_dataset':True}).then(function(data) {
            // success
            $scope.datasetCheckResult = data;
        }, function(data) {
            // failure
            $scope.datasetCheckResult = null;
            $scope.datasetCheckError = data;
        });
    };
    checkDataset();
    $scope.$watch('config.dataset', checkDataset);
});