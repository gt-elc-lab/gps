var angular = require('angular');
var moment = require('moment');

var admin = angular.module('admin', [
        require('angular-ui-router'),
        require('angular-resource'),
        require('angular-animate'),
        require('angular-messages')
    ]);
admin
    .controller('LabelingViewController', LabelingViewController)

    .service('SampleResource', SampleResource)

    .directive('sampleCard', SampleCard);

admin.config(function($httpProvider, $stateProvider, $urlRouterProvider) {

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

    $urlRouterProvider.otherwise("/labeling");
    $stateProvider
        .state('labeling', {
            url: '/labeling?page',
            templateUrl: 'templates/labeling.view.html',
            controller: 'LabelingViewController',
            controllerAs: 'LabelingView',
            params: {
                page: '0'
            }
        });
});

LabelingViewController.$inject = ['$http', '$state', 'SampleResource'];
function LabelingViewController($http, $state, SampleResource) {
    this.samples = SampleResource.query({page: +$state.params.page});
    this.page = $state.params.page;

    $http.get('/api/label/count').then(function(response) {
        this.count = response.data.count;
    }.bind(this));

    this.next = function() {
        $state.go('labeling', {page: +$state.params.page + 1})
    };

    this.previous = function() {
        if ($state.params.page == 0) {
            return;
        }
        $state.go('labeling', {page: +$state.params.page - 1})
    };
}

SampleResource.$inject = ['$resource'];
function SampleResource($resource) {
    return $resource('/api/label/:_id', {_id: '@_id'}, {
        query: {
            method: 'GET',
            isArray: true
        }
    });
}


function SampleCard() {
    return {
        scope: {
            sample: '='
        },
        restrict: 'AE',
        templateUrl: 'templates/samplecard.html',
        link: function($scope, $element, $attr) {
            var $container = $element.children();
            if ($scope.sample.label) {
                $container.addClass('panel-success')
            } else if ($scope.sample.label == false) {
                $container.addClass('panel-danger')
            } else {
                $container.addClass('panel-default');
            }

            $scope.label = function(value) {
                $scope.sample.$save({label: value ? 1 : 0});
            };

        },
    };
}





