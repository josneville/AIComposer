var app = angular.module('composer', []);
app.controller('main', function($scope, $http, $window) {
	$scope.tab = null
	$scope.delete = function(){
		if ($scope.deletion) {
			$http({
				url: "/restart",
				method: "POST",
				data: {index: 4, note: 14}
			})
			.success(function(data, status, headers, config){
				$scope.tab = data.vex
			})
		}
	}
});

app.directive('vextab', function($compile, $http){
    var canvas = document.createElement('canvas');
    var renderer = new Vex.Flow.Renderer( canvas, Vex.Flow.Renderer.Backends.CANVAS);
		var artist = new VexTabDiv.Artist(10, 10, 1000, {scale: 1});
    var vextab = new VexTabDiv.VexTab(artist);
    return{
        restrict: 'E',
        link: function(scope, element, attrs){
					if (scope.tab == null){
	          try {
	            vextab.reset();
	            artist.reset();
							$http.get('/compose/17')
								.success(function(data, status, headers, config){
									scope.tab = data.vex;
									vextab.parse(scope.tab);
									artist.render(renderer);
									$compile(canvas)(scope);
									element.replaceWith(canvas);
								})
	          }
	          catch (e) {
	            console.log("Error");
	            console.log(e);
	          }
					}
					scope.$watch('tab', function(tab){
						vextab.reset();
						artist.reset();
						vextab.parse(tab);
						artist.render(renderer);
						$compile(canvas)(scope);
						element.replaceWith(canvas);
					});
        }
    }
});
