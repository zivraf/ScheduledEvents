var redisApp = angular.module('redis', ['ui.bootstrap']);

/**
 * Constructor
 */
function RedisController() {}
redisApp.controller('RedisDemandCtrl', function ($scope, $http, $location) {
        $scope.controller = new RedisController();
        $scope.controller.scope_ = $scope;
        $scope.controller.location_ = $location;
        $scope.controller.http_ = $http;

        $scope.controller.http_.get("index.php?cmd=get&key=topology")
            .success(function(data) {
                console.log(data);
                //$scope.events = data.data.split("@");
                $scope.element=data
            });
})
;
