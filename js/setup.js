var app = angular.module('labeling.setup.module', []);

app.controller('LabelingSetupController', function($scope) {
    $scope.folderParam = {"type":"FOLDER", "name":"objects", "label":"Objects", "description":"Folder containing the objects to validate", "mandatory": true, "canSelectForeign": true};
    $scope.folderParam = {"type":"FOLDER", "name":"frames", "label":"Frames", "description":"Folder containing the frames the objects are from", "mandatory": true, "canSelectForeign": true};
    $scope.datasetParam = {"type":"DATASET", "name":"dataset", "label":"Labels", "description":"Dataset to save the labels into", "mandatory": true, "canSelectForeign": false};
    $scope.categoriesParam = {"name": "categories", "type": "KEY_VALUE_LIST", "label": "Categories", "description": "Category name → optional description", "mandatory": true}
    var checkDataset = function() {
        // the parameter to callPythonDo() is passed to the do() method as the payload
        // the return value of the do() method comes back as the data parameter of the fist function()
        $scope.callPythonDo({'check_dataset':true}).then(function(data) {
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