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
        return $resource('/api/unit/:unitId', {'unitId': '@uid'}, {
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
            saveUser: function(id, email){
                window.localStorage['flask-angular-user-id'] = id;
                window.localStorage['flask-angular-user-email'] = email;
            },
            
            getUser: function(){
                if (window.localStorage['flask-angular-user-id']){
                    return [
                        window.localStorage['flask-angular-user-id'],
                        window.localStorage['flask-angular-user-email']
                    ]
                } else {
                    return [null, null];
                }
            },
            
            clearUser: function(){
                delete window.localStorage['flask-angular-user-id'];
                delete window.localStorage['flask-angular-user-email'];
            }
        }
    }
);
