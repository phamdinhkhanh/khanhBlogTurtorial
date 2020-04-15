(async () => { 
	// Load model 
	await faceapi.nets.ssdMobilenetv1.loadFromUri("/models"); 
	await faceapi.nets.faceRecognitionNet.loadFromUri("/models"); 
	await faceapi.nets.faceLandmark68Net.loadFromUri("/models");
})();