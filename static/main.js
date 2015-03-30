'use strict';

/*Main*/

var flaskAngularApp = angular.module('flaskAngularApp', [
    'ngRoute',
    'flaskAngularControllers',
    'flaskAngularServices'
]);

flaskAngularApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/partials/home.html',
                controller: 'HomeController'
            }).
            when('/users/:userId', {
                templateUrl: '/static/partial/user.html',
                controller: 'UserController'
            }).
            when('/units/:unitId', {
                templateUrl: '/static/partial/unit.html',
                controller: 'UnitController'
            }).
            otherwise({
                redirectTo: '/'
            });
    }
]);
