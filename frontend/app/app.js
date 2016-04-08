var angular = require('angular');
var moment = require('moment');

var gps = angular.module('gps', [
        require('angular-ui-router'),
        require('angular-resource'),
        require('angular-animate'),
        require('angular-messages')
    ]);

gps
    .controller('HomeViewController', HomeViewController)
    .controller('LoginFormController', LoginFormController)
    .controller('RegisterFormController', RegisterFormController)
    .controller('AppViewController', AppViewController)
    .controller('FeedViewController', FeedViewController)
    .controllerAs('ConversationViewController', ConversationViewController)

    .service('AuthenticationService', AuthenticationService)
    .service('CurrentUserService', CurrentUserService)
    .service('PostResource', PostResource)
    .service('ConversationResource', ConversationResource)

    .directive('httpLoadingIndicator', HTTPLoadingIndicator)
    .directive('feedPostCard', FeedPostCard);

gps.config(function($httpProvider, $stateProvider, $urlRouterProvider) {

    $httpProvider.interceptors.push(function() {
        var apiUrl = 'http://localhost:5000';
        return {
            request: function(config) {
                if (config.url.startsWith('/api')) {
                    config.url = apiUrl + config.url;
                }
                return config;
            }
        };
    });

    $urlRouterProvider.otherwise("/home");
    $stateProvider
        .state('home', {
            url: '/home',
            templateUrl: 'templates/home.html',
            controller: 'HomeViewController',
            controllerAs: 'Home'
        })
        .state('home.login', {
            url: '/login',
            templateUrl: 'templates/login.html',
        })
        .state('home.register', {
            url: '/register',
            templateUrl: 'templates/register.html',
        })
        .state('app', {
            url: '/app',
            templateUrl: 'templates/app.html'
        })
        .state('app.feed', {
            url: '/feed',
            templateUrl: 'templates/feed.html',
            controller: 'FeedViewController',
            controllerAs: 'FeedView'
        })
        .state('app.conversations', {
            url:'/conversations',
            templateUrl: 'templates/conversations.html',
            controller: 'ConversationViewController',
            controller: 'ConversationView'
        })
        .state('app.settings', {
            url: '/settings',
            templateUrl: '/templates/settings.html'
        });
});


HomeViewController.$inject = ['$state'];
function HomeViewController($state) {

}

LoginFormController.$inject = ['$state', 'AuthenticationService'];
function LoginFormController($state, AuthenticationService) {

    this.login = function() {
        if (this.Form.$valid) {
            AuthenticationService.login(this.Form.email, this.Form.password)
            .then(function(response) {
                $state.go('app.feed');
            }.bind(this), function(error) {
                this.Form.$error.authentication = true;
                this.Form.message = error.message;
            }.bind(this));
        }
    };

}

RegisterFormController.$inject = ['$state', 'AuthenticationService'];
function RegisterFormController($state, AuthenticationService) {
    this.register = function() {
        if (this.Form.$valid) {
            AuthenticationService.register(this.Form.email, this.Form.password)
                .then(function(response) {
                this.Form.$success = {authentication: true};
                $state.go('app.feed');
            }.bind(this), function(error) {
                this.Form.$error.authentication = true;
                this.Form.errorMessage = error.message;
            }.bind(this));
        }
    };
}

AppViewController.$inject = ['$state'];
function AppViewController($state) {

}

FeedViewController.$inject = ['$state', 'PostResource'];
function FeedViewController($state, PostResource) {
    this.posts = PostResource.query();
}

ConversationViewController.$inject = ['$state', 'PostResource'];
function ConversationViewController($state, PostResource) {
    this.posts = PostResource.query();
}

function CurrentUserService() {
    var currentUser = null;

    this.getCurrentUser = function() {
        return currentUser;
    };

    this.setCurrentUser = function(user) {
        this.currentUser = user;
    };
}


AuthenticationService.$inject = ['$http', '$q', 'CurrentUserService'];
function AuthenticationService($http, $q, CurrentUserService) {

    this.login = function(email, password) {
        var deferred = $q.defer();
        var params =   {email: email, password: password};
        $http.post('/api/login', params).then(function(response) {
            CurrentUserService.setCurrentUser(response.data);
            deferred.resolve(response.data);
        }, function(error) {
            deferred.reject(error.data);
        });
        return deferred.promise;
    };

    this.logout = function() {
        CurrentUserService.setCurrentUser(null);
    };

    this.register = function(email, password) {
        var deferred = $q.defer();
        var params = {email: email, password: password};
        $http.post('/api/register', params).then(function(response) {
            CurrentUserService.setCurrentUser(response.data);
            deferred.resolve(response.data);
        }, function(error) {
            deferred.reject(error.data);
        });
        return deferred.promise;
    };
}

HTTPLoadingIndicator.$inject = ['$http']
function HTTPLoadingIndicator($http) {
    return  {
        restrict: 'AE',
        templateUrl: 'templates/http-loading-indicator.html',

        link: function($scope, $element, $attrs) {
            $scope.isLoading = isLoading;
            $scope.$watch($scope.isLoading, toggleElement);


            function toggleElement(loading) {
                if (loading) {
                    $element.show();
              } else {
                    $element.hide();
              }
            }

            function isLoading() {
              return $http.pendingRequests.length > 0;
            }
        }
    }
}


FeedPostCard.$inject = ['$state', 'ConversationResource', 'CurrentUserService'];
function FeedPostCard($state, ConversationResource, CurrentUserService) {
    return {
        scope: {
            post: '='
        },
        restrict: 'AE',
        templateUrl: 'templates/feedpostcard.html',
        link: function($scope, $element, $attrs) {
            var currentUser = CurrentUserService.getCurrentUser();
            var textLimit = 500;
            var showMoreText = 'show more';
            var showLessText = 'show less';


            $scope.vm = {};
            $scope.vm.date = moment($scope.post.created.$date)
                .format("dddd, MMMM Do, h:mm a");
            $scope.textLimit = textLimit;
            $scope.textPrompt = showMoreText;
            $scope.shouldShowButton = $scope.post.content.length > textLimit;

            $scope.messages = {
                discard: false,
                success: false,
                error: false
            };

            $scope.showMessage = function(type) {
                // $scope.message.visible =  !$scope.message.visible;
                $scope.messages[type]= true;
            };

            $scope.hideMessage = function(type) {
                $scope.messages[type] = false;
            };


            $scope.show = function() {
                var fn = $scope.textPrompt == showMoreText ? showMore : showLess;
                fn();
                return;
            };

            $scope.discard = function() {
                $scope.post.$delete().then(function(response) {
                    $scope.$destroy();
                }, function(error) {

                })
            };

            $scope.reply = function() {
                $state.go('main.reply', {_id: $scope.post._id, post: $scope.post});
                return;
            };

            $scope.accept = function() {
                var conversation = new ConversationResource({r_id: $scope.post._id,
                    user_id: null});
                conversation.$save().then(function(response) {

                }, function(error) {
                    $scope.showMessage('error');
                });
            };
        }
    }
}

PostResource.$inject = ['$resource'];
function PostResource($resource) {
    return $resource('/api/post/:_id', {_id: '@_id'}, {
        query: {
            method: 'GET',
            isArray: true
        }
    });
}

ConversationResource.$inject = ['$resource'];
function ConversationResource($resource) {
    return $resource('/api/conversation/:r_id/:user_id',
        {r_id: '@r_id', user_id: '@user_id'},
        { query: {
            method: 'GET',
            isArray: true
        }
    });
}