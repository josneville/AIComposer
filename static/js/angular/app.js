var app = angular.module('composer', []);
app.controller('main', function($scope, $http, $window, $timeout) {
	$scope.tab = null;
	notes = {"A#1" : 58.2705, "B1" : 61.7354, "C2" : 65.4064,
	"C#2" : 69.2957, "D2" : 73.4162, "D#2" : 77.7817, "E2" : 82.4069,
	"F2" : 87.3071, "F#2" : 92.4986, "G2" : 97.9989, "G#2" : 103.826,
	"A2" : 110, "A#2" : 116.542, "B2" : 123.471, "C3" : 130.813,
	"C#3" : 138.591, "D3" : 146.832, "D#3" : 155.563, "E3" : 164.814,
	"F3" : 174.614, "F#3" : 184.997, "G3" : 195.998, "G#3" : 207.652,
	"A3" : 220, "A#3" : 233.082, "B3" : 246.942, "C4" : 261.626,
	"C#4" : 277.183, "D4" : 293.665, "D#4" : 311.127, "E4" : 329.628,
	"F4" : 349.228, "F#4" : 369.994, "G4" : 391.995, "G#4" : 415.305,
	"A4" : 440, "A#4" : 466.164, "B4" : 493.883, "C5" : 523.251,
	"C#5" : 554.365, "D5" : 587.330, "D#5" : 622.254, "E5" : 659.255,
	"F5" : 698.456, "F#5" : 739.989, "G5" : 783.991, "G#5" : 830.609,
	"A5" : 880, "A#5" : 932.328, "B5" : 987.767, "C6" : 1046.5,
	"C#6" : 1108.73, "D6" : 1174.66, "D#6" : 1244.51, "E6" : 1318.51,
	"F6" : 1396.91, "F#6" : 1479.98, "G6" : 1567.98, "G#6" : 1661.22,
	"A6" : 1760, "A#6" : 1864.66, "B6" : 1975.53, "C7" : 2093,
	"C#7" : 2217.46, "D7" : 2349.32, "D#7" : 2489.02, "E7" : 2637.02,
	"F7" : 2793.83, "F#7" : 2959.96, "G7" : 3135.96, "G#7" : 3322.44,
	"A7" : 3520, "A#7" : 3729.31, "B7" : 3951.07, "C8" : 4186.01};
	function matchNote(freq){
		var closest = "A#1"; // Default closest note
		var closestFreq = 58.2705;
		for (var key in notes) { // Iterates through note look-up table
			// If the current note in the table is closer to the given
			// frequency than the current "closest" note, replace the
			// "closest" note.
			 if (Math.abs(notes[key] - freq) <= Math.abs(notes[closest] -
				freq)) {
					closest = key;
					closestFreq = notes[key];
				}
				// Stop searching once the current note in the table is of higher
				// frequency than the given frequency.
				if (notes[key] > freq) {
					break;
				}
		}
		return [closest, closestFreq];
	}
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
	$scope.arpeggio = function(){
		$http({
			url: "/arpeggio",
			method: "POST"
		})
		.success(function(data, status, headers, config){
			$scope.tab = data.vex
		})
	}
	var mic = new Microphone();
	mic.initialize();
	var listening = false;

	var poll = function() {
		$timeout(function() {
			if (mic.isInitialized()) {
				if (!listening) {
					mic.startListening();
					listening = true;
				}
				var freq = mic.getFreq(1);
				if (freq > 250 && freq < 1600) {
					console.log(matchNote(freq));
				}
			}
			poll();
		}, 100);
	};

	poll();
});

app.directive('vextab', function($compile, $http, $window){
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
									canvas.toBlob(function(blob){
										var fd = new FormData();
										fd.append('image', blob);
										$http.post("/upload", fd, {
											transformRequest: angular.identity,
											headers: {'Content-Type': undefined}
										})
										.success( function(data, status, headers, config){console.log("ok")} )
										.error( function(data, status, headers, config){console.log("nah")}  );
									})
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
						console.log('hi');
						canvas.toBlob(function(blob){
							var fd = new FormData();
							fd.append('image', blob);
							$http.post("/upload", fd, {
								transformRequest: angular.identity,
								headers: {'Content-Type': undefined}
							})
							.success( function(data, status, headers, config){console.log("ok")} )
							.error( function(data, status, headers, config){console.log("nah")}  );
						})
						element.replaceWith(canvas);
					});
        }
    }
});
