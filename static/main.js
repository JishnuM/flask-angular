'use strict';

/*Main*/

var flaskAngularApp = angular.module('flaskAngularApp', [
    'ngRoute',
    'xeditable',
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
            when('/user/:userId', {
                templateUrl: '/static/partials/user.html',
                controller: 'UserController'
            }).
            when('/unit/:unitId', {
                templateUrl: '/static/partials/unit.html',
                controller: 'UnitController'
            }).
            otherwise({
                redirectTo: '/'
            });
    }
]);
