'use strict';

/*Controllers*/

var flaskAngularControllers = angular.module('flaskAngularControllers', []);

flaskAngularControllers.controller('HomeController', 
    ['$scope', '$location', 'User', 'UserManager',
    function($scope, $location, User, UserManager) {
        $scope.login_email = "";
        $scope.new_user_email = "";
        $scope.new_user_first_name = "";
        $scope.new_user_last_name = "";

        $scope.login_user = function(){
            var user = User.getByEmail({userEmail: $scope.login_email}, function(){
                console.log(user);
                UserManager.saveUserId(user.uid);
                $location.path('/user/' + user.uid);
            }, function(res){
                if (res.status === 404){
                    alert("No such user");
                }
            })
        }

        $scope.create_user = function(){
            var data = {}
            data.email = $scope.new_user_email;
            data.first_name = $scope.new_user_first_name;
            data.last_name = $scope.new_user_last_name;
            var new_user = User.create(data, function(){
                console.log(new_user);
                UserManager.saveUserId(new_user.uid);
                $location.path('/user/' + user.uid);
            })
        }
        
    }
]);

flaskAngularControllers.controller('UserController', 
    ['$scope', '$location', '$routeParams', 'User', 'UserManager',
    function($scope, $location, $routeParams, User, UserManager) {
        $scope.current_user_id = UserManager.getUserId();
        var user_id = $routeParams.userId;
        var user = User.get({userId: user_id}, function(){
            $scope.user = user;
            var units = User.getUnits({userId: user_id}, function(){
                $scope.units = units.data;
            }); 
        }, function(res){
            if (res.status === 404){
                alert("No such user");
            }
            $location.path('/');
        });
        $scope.delete = function(){
            var res = User.remove({userId: user_id}, function(){
                $location.path('/');
            });
        }
        $scope.update = function(){
            user.$save(function(){
                //Really hacky fix since API doesnt return object on save
                user.$get({userId: user_id});
            });
        }
    }
]);

flaskAngularControllers.controller('UnitController', ['$scope', '$routeParams',
    function($scope, $routeParams) {
        //
    }
]);
