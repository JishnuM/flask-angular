'use strict';

/*Services*/

var flaskAngularServices = angular.module('flaskAngularServices', ['ngResource']);

flaskAngularServices.factory('User', ['$resource',
    function($resource){
        return $resource('/api/user/:userId', {'userId': '@uid'}, {
            create: {method:'POST', url:'/api/createuser'},
            get: {method:'GET'},
            update: {method:'POST'},
            remove: {method:'DELETE'},
            getAll: {method:'GET', url:'/api/users'},
            getByEmail: {method:'GET', url:'/api/user-email/:userEmail'},
            getUnits: {method:'GET', url:'/api/user-units/:userId'}
        });
    }
]);

flaskAngularServices.factory('Unit', ['$resource',
    function($resource){
        return $resource('/api/unit/:unitId', {}, {
            create: {method:'POST', url:'/api/createunit'},
            get: {method:'GET'},
            update: {method:'POST'},
            remove: {method:'DELETE'},
        });
    }
]);

flaskAngularServices.factory('UserManager',
    function(){
        return {
            saveUserId: function(id){
                window.localStorage['flask-angular-user'] = id;
            },
            
            getUserId: function(){
                if (window.localStorage['flask-angular-user']){
                    return window.localStorage['flask-angular-user']
                } else {
                    return null;
                }
            },
            
            clearUserId: function(){
                window.localStorage['flask-angular-user'] = null;
            }
        }
    }
);
