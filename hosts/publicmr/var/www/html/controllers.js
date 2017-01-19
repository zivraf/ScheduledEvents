var redisApp = angular.module('redis', ['ui.bootstrap']);

/**
 * Constructor
 */
function RedisController() {}
/*
RedisController.prototype.onRedisDemand = function($scope, $http, $location) {
    $scope.controller = new RedisController();
    $scope.controller.scope_ = $scope;
    $scope.controller.location_ = $location;
    $scope.controller.http_ = $http;
    $scope.controller.http_.get("map.php?cmd=get&key=events")
            .success(function(data) {
                console.log(data);
                $scope.events = data.data.split(",");
            });

};
*/
redisApp.controller('RedisDemandCtrl', function ($scope, $http, $location) {
        $scope.controller = new RedisController();
        $scope.controller.scope_ = $scope;
        $scope.controller.location_ = $location;
        $scope.controller.http_ = $http;

        $scope.controller.http_.get("map.php?cmd=get&key=events")
            .success(function(data) {
                console.log(data);
                $scope.events = data.data.split("@");
            });
})
;
