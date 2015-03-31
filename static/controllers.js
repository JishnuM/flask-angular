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
    ['$scope', '$location', '$routeParams', 'Unit', 'User', 'UserManager',
    function($scope, $location, $routeParams, Unit, User, UserManager) {
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
    ['$scope', 'User', 'UserManager',
    function($scope, User, UserManager){
        var users = User.getAll({}, function(){ 
            $scope.users = users.data;
        });    
    }
]);

flaskAngularControllers.controller('UnitController', 
    ['$scope', '$location', '$routeParams','Unit', 'UserManager',
    function($scope, $location, $routeParams, Unit, UserManager) {
        var unit_id = $routeParams.unitId;
        $scope.current_user_id = UserManager.getUserId();
        var unit = Unit.get({unitId: unit_id}, function(){
            $scope.unit = unit;
        }, function(res){
            if(res.status === 404){
                alert('No such unit');
                $location.path('/user/' + UserManager.getUserId());
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
                $location.path('/user/' + UserManager.getUserId());
            }); 
        }
    
    }
]);
