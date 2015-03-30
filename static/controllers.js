'use strict';

/*Controllers*/

var flaskAngularControllers = angular.module('flaskAngularControllers', []);

flaskAngularControllers.controller('HomeController', ['$scope',
    function($scope) {
        $scope.login_email = "";
        $scope.new_user_email = "";
        $scope.new_user_first_name = "";
        $scope.new_user_last_name = "";

        $scope.login_user = function(){
            console.log($scope.login_email);
        }

        $scope.create_user = function(){
            console.log($scope.new_user_email);
            console.log($scope.new_user_first_name);
            console.log($scope.new_user_last_name);
        }
        
    }
]);

flaskAngularControllers.controller('UserController', ['$scope', '$routeParams',
    function($scope, $routeParams) {
        //
    }
]);

flaskAngularControllers.controller('UnitController', ['$scope', '$routeParams',
    function($scope, $routeParams) {
        //
    }
]);
