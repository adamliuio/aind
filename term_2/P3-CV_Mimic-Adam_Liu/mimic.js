
var divRoot = $('#camera')[0]
var width = 640, height = 480
var faceMode = affdex.FaceDetectorMode.LARGE_FACES

// Initialize an Affectiva CameraDetector object
var detector = new affdex.CameraDetector(divRoot, width, height, faceMode)

// Enable detection of all Expressions, Emotions and Emojis classifiers.
detector.detectAllEmojis()
detector.detectAllEmotions()
detector.detectAllAppearance()
detector.detectAllExpressions()

// --- Utility values and functions ---

// Unicode values for all emojis Affectiva can detect
var emojis = [ 128528, 9786, 128515, 128524, 128527, 128521, 128535, 128539, 128540, 128542, 128545, 128563, 128561 ]

// Global Vars
var timer = null
var scoreTotal = 0
var scoreCorrect = 0
var targetEmoji = null

// Update target emoji being displayed by supplying a unicode value
function setTargetEmoji(code) {
	$('#target').html('&#' + code + ';')
}

// Convert a special character to its unicode value (can be 1 or 2 units long)
function toUnicode(c) {
	if (c.length == 1) {
		return c.charCodeAt(0)
	}
	return (c.charCodeAt(0) - 0xd800) * 0x400 + (c.charCodeAt(1) - 0xdc00) + 0x10000
}

// Update score being displayed
function setScore(correct, total) {
	$('#score').html('Score: ' + correct + ' / ' + total)
}

// Display log messages and tracking results
function log(node_name, msg) {
	$(node_name).append('<span>' + msg + '</span><br />')
}

// Pick a random emoji and update score
function randomEmoji() {
	var emoji = emojis[Math.floor(Math.random() * emojis.length)]
	targetEmoji = emoji
	setTargetEmoji(emoji)
	scoreTotal += 1
	setScore(scoreCorrect, scoreTotal)
	resetTimer()
}



// --- Callback functions ---

// Start button
function onStart() {
	if (detector && !detector.isRunning) {
		$('#logs').html('')
		detector.start()
	}
	log('#logs', 'Start button pressed')
}

// Stop button
function onStop() {
	log('#logs', 'Stop button pressed')
	if (detector && detector.isRunning) {
		detector.removeEventListener()
		detector.stop()
	}
}

// Reset button
function onReset() {
	log('#logs', 'Reset button pressed')
	if (detector && detector.isRunning) {
		detector.reset()
	}
	$('#results').html('')
	$('#logs').html('')

	resetGame()
}

// Add a callback to notify when camera access is allowed
detector.addEventListener('onWebcamConnectSuccess', function() {
	log('#logs', 'Webcam access allowed')
})

// Add a callback to notify when camera access is denied
detector.addEventListener('onWebcamConnectFailure', function() {
	log('#logs', 'webcam denied')
	console.log('Webcam access denied')
})

// Add a callback to notify when detector is stopped
detector.addEventListener('onStopSuccess', function() {
	log('#logs', 'The detector reports stopped')
	$('#results').html('')
})

// Add a callback to notify when the detector is initialized and ready for running
detector.addEventListener('onInitializeSuccess', function() {
	log('#logs', 'The detector reports initialized')
	//Display canvas instead of video feed because we want to draw the feature points on it
	$('#face_video_canvas').css('display', 'block')
	$('#face_video').css('display', 'none')
})

detector.addEventListener('onImageResultsSuccess', function( faces, image, timestam ) {
	var canvas = $('#face_video_canvas')[0]
	if (!canvas) return

	$('#results').html('')
	log('#results', 'Timestamp: ' + timestamp.toFixed(2))
	log('#results', 'Number of faces found: ' + faces.length)
	
	if (faces.length > 0) {
		// Report desired metrics
		log('#results', 'Appearance: ' + JSON.stringify(faces[0].appearance))
		log('#results', 'Emotions: ' +
			JSON.stringify(faces[0].emotions, function(key, val) {
				return val.toFixed ? Number(val.toFixed(0)) : val
			})
		)
		log('#results', 'Expressions: ' +
			JSON.stringify(faces[0].expressions, function(key, val) {
				return val.toFixed ? Number(val.toFixed(0)) : val
			})
		)
		log('#results', 'Emoji: ' + faces[0].emojis.dominantEmoji)

		drawFeaturePoints(canvas, image, faces[0])
				drawEmoji(canvas, image, faces[0])

		playGame(canvas, image, faces[0])
	}
})



// --- Custom functions ---

function drawFeaturePoints(canvas, img, face) {

	var ctx = canvas.getContext('2d')
	ctx.strokeStyle = '#FFFFFF'

	for (var id in face.featurePoints) {
		var featurePoint = face.featurePoints[id]
		ctx.beginPath()
		ctx.arc(featurePoint.x, featurePoint.y, 1, 0, 2 * Math.PI)
		ctx.fillStyle = 'white'
		ctx.fill()
		ctx.stroke()
	}
}

function drawEmoji(canvas, img, face) {

	var ctx = canvas.getContext('2d')
	ctx.font = '48px san-serif'
	const anchor = face.featurePoints[4]
	ctx.fillText(face.emojis.dominantEmoji, anchor.x, anchor.y)
}

function playGame(canvas, image, face) {
	if (targetEmoji == null) {
		resetGame()
	}

	var emoji = toUnicode(face.emojis.dominantEmoji)

	if (emoji == targetEmoji) {
		scoreCorrect += 1
		randomEmoji()
	}
}

function resetGame() {
	randomEmoji()
	scoreCorrect = 0
	scoreTotal = 0
	setScore(scoreCorrect, scoreTotal)
}

function resetTimer() {
	clearTimeout(timer)
	timer = null
	timer = setTimeout(randomEmoji, 6000)
}