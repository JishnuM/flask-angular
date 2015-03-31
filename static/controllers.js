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
                UserManager.saveUser(user.uid, user.email);
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
                UserManager.saveUser(new_user.user_id, data.email);
                $location.path('/user/' + new_user.user_id);
            })
        }
        
    }
]);

flaskAngularControllers.controller('UserController', 
    ['$scope', '$location', '$routeParams', 'Unit', 'User', 'UserManager',
    function($scope, $location, $routeParams, Unit, User, UserManager) {
        var current_user = UserManager.getUser();
        $scope.current_user_id = current_user[0]
        $scope.current_user_email = current_user[1]
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
        $scope.logout = function(){
            UserManager.clearUser();
            $location.path('/');
        }
        $scope.create_unit = function(){
            $scope.show_form = false;
            var data = {}
            data.creator_id = $scope.current_user_id;
            data.num_rooms = $scope.num_rooms;
            data.num_bathrooms = $scope.num_bathrooms;
            data.sqft = $scope.sqft;
            data.address = {}
            data.address.block_number = $scope.block_number;
            data.address.street_name = $scope.street_name;
            data.address.postal_code = $scope.postal_code;
            data.address.city = $scope.city;
            data.address.country = $scope.country;
            data.address.coordinates = [$scope.lat, $scope.lng]
            var new_unit = Unit.create(data, function(){
                var units = User.getUnits({userId: user_id}, function(){
                    $scope.units = units.data;
                }); 
            }) 
        }
    }
]);

flaskAngularControllers.controller('UserListController',
    ['$scope', '$location', 'User', 'UserManager',
    function($scope, $location, User, UserManager){
        var current_user = UserManager.getUser();
        $scope.current_user_id = current_user[0]
        $scope.current_user_email = current_user[1]
        var users = User.getAll({}, function(){ 
            $scope.users = users.data;
        });    
        $scope.logout = function(){
            UserManager.clearUser();
            $location.path('/');
        }
    }
]);

flaskAngularControllers.controller('UnitController', 
    ['$scope', '$location', '$routeParams','Unit', 'UserManager',
    function($scope, $location, $routeParams, Unit, UserManager) {
        var unit_id = $routeParams.unitId;
        var current_user = UserManager.getUser();
        $scope.current_user_id = current_user[0]
        $scope.current_user_email = current_user[1]
        var unit = Unit.get({unitId: unit_id}, function(){
            $scope.unit = unit;
        }, function(res){
            if(res.status === 404){
                alert('No such unit');
                $location.path('/user/' + current_user[0]);
            }
        });
        $scope.update = function(){
            unit.$save(function(){
                //Really hacky fix since API doesnt return object on save
                unit.$get({unitId: unit_id});
            });
        }
        $scope.delete = function(){
            var res = Unit.remove({unitId: unit_id}, function(){
                $location.path('/user/' + current_user[0]);
            }); 
        }
        $scope.logout = function(){
            UserManager.clearUser();
            $location.path('/');
        } 
    }
]);
