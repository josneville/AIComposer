var app = angular.module('composer', []);
app.controller('main', function($scope, $http, $window) {

});

app.directive('vextab', function($compile, $http){
    var canvas = document.createElement('canvas');
    var renderer = new Vex.Flow.Renderer( canvas, Vex.Flow.Renderer.Backends.CANVAS);
		var artist = new VexTabDiv.Artist(10, 10, 800, {scale: 1});
    var vextab = new VexTabDiv.VexTab(artist);
    return{
        restrict: 'E',
        link: function(scope, element, attrs){
          try {
            vextab.reset();
            artist.reset();
						$http.get('/rhythm/17')
							.success(function(data, status, headers, config){
								vextab.parse(data);
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
    }
});
