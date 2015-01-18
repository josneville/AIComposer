var app = angular.module('composer', []);
app.controller('main', function($scope, $http, $window, $timeout) {
	$scope.tab = null;
	notes = {"B@1" : 58.2705, "B1" : 61.7354, "C2" : 65.4064,
	"C#2" : 69.2957, "D2" : 73.4162, "E@2" : 77.7817, "E2" : 82.4069,
	"F2" : 87.3071, "F#2" : 92.4986, "G2" : 97.9989, "G#2" : 103.826,
	"A2" : 110, "B@2" : 116.542, "B2" : 123.471, "C3" : 130.813,
	"C#3" : 138.591, "D3" : 146.832, "E@3" : 155.563, "E3" : 164.814,
	"F3" : 174.614, "F#3" : 184.997, "G3" : 195.998, "G#3" : 207.652,
	"A3" : 220, "B@3" : 233.082, "B3" : 246.942, "C4" : 261.626,
	"C#4" : 277.183, "D4" : 293.665, "E@4" : 311.127, "E4" : 329.628,
	"F4" : 349.228, "F#4" : 369.994, "G4" : 391.995, "G#4" : 415.305,
	"A4" : 440, "B@4" : 466.164, "B4" : 493.883, "C5" : 523.251,
	"C#5" : 554.365, "D5" : 587.330, "E@5" : 622.254, "E5" : 659.255,
	"F5" : 698.456, "F#5" : 739.989, "G5" : 783.991, "G#5" : 830.609,
	"A5" : 880, "B@5" : 932.328, "B5" : 987.767, "C6" : 1046.5,
	"C#6" : 1108.73, "D6" : 1174.66, "E@6" : 1244.51, "E6" : 1318.51,
	"F6" : 1396.91, "F#6" : 1479.98, "G6" : 1567.98, "G#6" : 1661.22,
	"A6" : 1760, "B@6" : 1864.66, "B6" : 1975.53, "C7" : 2093,
	"C#7" : 2217.46, "D7" : 2349.32, "E@7" : 2489.02, "E7" : 2637.02,
	"F7" : 2793.83, "F#7" : 2959.96, "G7" : 3135.96, "G#7" : 3322.44,
	"A7" : 3520, "B@7" : 3729.31, "B7" : 3951.07, "C8" : 4186.01};

	function matchNote(freq){
		var closest = "B@1"; // Default closest note
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

	$scope.delete = function(index, note){
		$http({
			url: "/restart",
			method: "POST",
			data: {index: index, note: note}
		})
		.success(function(data, status, headers, config){
			$scope.data = data;
			$scope.tab = data.vex
		})
	}
	$scope.arpeggio = function(){
		$http({
			url: "/arpeggio",
			method: "POST"
		})
		.success(function(data, status, headers, config){
			$scope.data = data;
			$scope.tab = data.vex;
		})
	}

	var mic = new Microphone();
	mic.initialize();
	var listening = false;
	var currentNote = "";
	var counter = 0;
	var currentLocation = 0;
	var none = 0;
	var poll = function() {
		$timeout(function() {
			if (mic.isInitialized()) {
				if (!listening) {
					mic.startListening();
					listening = true;
				}
				var freq = mic.getFreq(1);
				if (freq > 250 && freq < 1600) {
					if (none < 60) {
						var newNote = matchNote(freq)[0];
						if (currentNote == newNote) {
							counter++;
						}
						else {
							counter = 0;
							currentNote = newNote;
						}
						if (counter == 3) {
							none = 0;
							currentLocation = findLocation(currentNote, currentLocation);
						}
						console.log(currentLocation);
					}
					else{
						console.log("Waiting");
						newNote = matchNote(freq)[0]
						if (currentNote == newNote) {
							counter++;
						}
						else {
							counter = 0;
							currentNote = newNote;
						}
						if (counter == 5) {
							var octave = parseInt(currentNote.slice(-1));
							var letter = currentNote.slice(0, -1);
							var correlation = {'C': 0, 'C#': 1, 'D': 2, 'E@': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'B@': 10, 'B': 11};
							var note = correlation[letter] + (12 * (octave - 3));
							console.log("Deleting and restarting");
							$scope.delete(currentLocation, note);
							none = 0;
						}
					}
				}
				none++;
			}
			poll();
		}, 100);
	};

	poll();

	function findLocation(completeNote, loc) {
		var octave = parseInt(completeNote.slice(-1));
		if (octave < 3 || octave > 6) {
			return loc;
		}
		var letter = completeNote.slice(0, -1);
		var correlation = {'C': 0, 'C#': 1, 'D': 2, 'E@': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'B@': 10, 'B': 11};
		var note = correlation[letter] + (12 * (octave - 3));
		var seen = false;
		var prev = note;
		var returnLoc = loc;
		for (var i = loc; i < $scope.data.tab.length; i++) {
			for (var j = 0; j < $scope.data.tab[i].length; j++) {
				currentNote = $scope.data.tab[i][j].note;
				if (note === currentNote) {
					return i;
				}
			}
		}
		return loc;
	}
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
									scope.data = data;
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
