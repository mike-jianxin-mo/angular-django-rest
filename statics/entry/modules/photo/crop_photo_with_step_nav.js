'use strict'

if (!('sendAsBinary' in XMLHttpRequest.prototype)) {
  XMLHttpRequest.prototype.sendAsBinary = function(string) {
    var bytes = Array.prototype.map.call(string, function(c) {
      return c.charCodeAt(0) & 0xff;
    });
    this.send(new Uint8Array(bytes).buffer);
  };
};

var cropPhotoModule = angular.module('cropPhotoModule', ['angularFileUpload', 'ngCookies']);

cropPhotoModule.controller('cropPhotoMainCtrl', ['$scope', '$state', 'runTimeParam',
	function($scope, $state, runTimeParam){
		$scope.BackToProductPhotoList = function(){
			$state.go('admin.product.photo.list');
		};
		$scope.product = runTimeParam.curProduct;
		$state.go('admin.product.photo.new.select');

		$scope.$on('$stateChangeSuccess', function(event, viewConfig){ 
			var last = _.str.strRightBack($state.current.name, '.');
			// switch display state 
			switch(last){
				case 'new':
					break;
				case 'select':
					$scope.step1 = 'active';
					$scope.step2 = '';
					$scope.step3 = '';
					break;
				case 'crop':
					$scope.step1 = 'complete';
					$scope.step2 = 'active';
					$scope.step3 = '';
					break;
				case 'upload':
					$scope.step1 = 'complete';
					$scope.step2 = 'complete';
					$scope.step3 = 'active';
					break;
			}
		});

	}]);

cropPhotoModule.controller('selectPhotoCtrl', ['$scope', '$location', 'notificationFactory', 'photoHandler', 'settings', 'runTimeParam', '$state',
	function($scope, $location, notificationFactory, photoHandler, settings, runTimeParam, $state){

		var jPreViewImg = jQuery("<img>", {id:"operImg"});
		
		$scope.onFileSelect = function($files) {
			var promise = photoHandler.showPreviewPhoto($files, jPreViewImg);

			promise.then(function(p){
				// read file completed!
				photoHandler.setOriginalPhoto(p);
				$state.go('admin.product.photo.new.crop');
			}, function(p){
				console.log('read file failure!!', p)
			})
		};

	}]);

cropPhotoModule.controller('cropPhotoCtrl', ['$scope', 'photoHandler', '$state',
	function($scope, photoHandler, $state){
		var jPreViewImg = photoHandler.getOriginalPhoto();

		$scope.cropImg = function(){
			// var img = document.getElementById("previewImgArea");
			photoHandler.cropPhoto(photoHandler.getCropResult(), jPreViewImg.get(0));
			$state.go('admin.product.photo.new.upload');
		};

		var initCropFun = function(){
			photoHandler.initJcropFun();
		};

		$scope.$on('$viewContentLoaded', function(){
			// after finished loading partial view, initiate jquery plugin
			var size = photoHandler.resize();
			jPreViewImg.width(size['width']);
			jPreViewImg.height(size['height']);
			jPreViewImg.appendTo('#previewImgArea');

			var jCanvas = jQuery("<canvas/>");
			photoHandler.setCropResult(jCanvas);

			initCropFun();
		});

	}]);


cropPhotoModule.controller('uploadPhotoCtrl', ['$scope', 'photoHandler', 'settings', 'runTimeParam', '$state',
	function($scope, photoHandler, settings, runTimeParam, $state){

		$scope.upload = function(){
			photoHandler.sendPhoto(	settings.PHOTO_URI,
									runTimeParam.curSite.id,
									runTimeParam.curProduct.id, 
									"uploadFile",
									"test.png",
									photoHandler.getCropResult().get(0),
									"image/png", 
									function(){$state.go('admin.product.photo.list');}, 
									uploadFail );
		};

		function uploadFail(){
			alert("upload failure!");
		};

		$scope.$on('$viewContentLoaded', function(){
			// show crop result
			photoHandler.getCropResult().appendTo("#cropResult");
		});

	}]);
 	
cropPhotoModule.factory('photoHandler', ['$cookies','$q', function($cookies, $q){
		// image data
		var x1=1, y1=1, x2=1, y2=1, w=1, h=1;
		var imgOrgWidth=1, imgOrgHeight=1;
		var MAX_WIDTH = 800, MAX_HEIGHT = 800;
		var realWidth=1, realHeight=1;
		var rate = 1;

		var originalPhoto;
		var cropResult;

		function initJcropFun(){
			jQuery('#previewImgArea').Jcrop({
				// onChange:   setPosition
				onSelect: setPos,
				aspectRatio: 4.5 / 6
			});
		};

		function setPos(p){
			x1 = p.x;
			y1 = p.y;
			x2 = p.x2;
			y2 = p.y2;
			w  = p.w;
			h  = p.h;
			// console.log('set crop position',p ,  x1, y1, x2, y2, w, h);
		};

		function resize(){
			var width = imgOrgWidth;
			var height = imgOrgHeight;
			var widthScaleRate = width / MAX_WIDTH;
			var heightScaleRate= height/ MAX_HEIGHT;

			if (widthScaleRate > heightScaleRate) {
			  if (width > MAX_WIDTH) {
			  	rate = widthScaleRate;
			    height *= MAX_WIDTH / width;
			    width = MAX_WIDTH;			    
			  }
			} else {
			  if (height > MAX_HEIGHT) {
			  	rate = height / MAX_HEIGHT;
			    width *= MAX_HEIGHT / height;
			    height = MAX_HEIGHT;		    
			  }
			}
			realWidth = width;
			realHeight= height;

			return {width: realWidth, height: realHeight, rate: rate};
		}

		/***
		 * @description        Uploads a file via multipart/form-data, via a Canvas elt
		 * @param url  String: Url to post the data
		 * @param name String: name of form element
		 * @param fn   String: Name of file
		 * @param canvas HTMLCanvasElement: The canvas element.
		 * @param type String: Content-Type, eg image/png
		 ***/
		// $scope.postCanvasToURL = function(url, name, fn, canvas, type) {

		/*** consider using form data method to handle the upload file issue
		var fileData = new FormData();
		// fileData.append('uploadFile', jCanvas.get(0).toDataURL('image/jpeg'));
		***/
		function sendPhoto(uploadURI, siteId, productId, name, fn, canvas, type, successCallBackFn, faileCallBackFn) {
		  var url = uploadURI;
		  var data = canvas.toDataURL(type);
		  data = data.replace('data:' + type + ';base64,', '');

		  var xhr = new XMLHttpRequest();

		  xhr.onreadystatechange=function()
		  {
		  if (xhr.readyState==4 && xhr.status==201)
		    {
		    	successCallBackFn();
		    }else if(xhr.readyState==4 && xhr.status!=201)
		    	faileCallBackFn();
		  };

		  xhr.open('POST', url, true);
		  xhr.setRequestHeader('X-CSRFToken', $cookies.csrftoken);
		  var boundary ="---------------------------ajax"+ (new Date).getTime() + 'boundary';
		  xhr.setRequestHeader(
		    'Content-Type', 'multipart/form-data; boundary=' + boundary);
		  xhr.sendAsBinary([
		    '--' + boundary,
			'Content-Disposition: form-data; name="type"',
			"\r\n",
			"product",
		    '--' + boundary,
			'Content-Disposition: form-data; name="name"',
			"\r\n",
			"image name",
		    '--' + boundary,
			'Content-Disposition: form-data; name="siteId"',
			"\r\n",
			siteId,
		    '--' + boundary,
			'Content-Disposition: form-data; name="product"',
			"\r\n",
			productId,
		    '--' + boundary,
		    'Content-Disposition: form-data; name="image"; filename="' + fn + '"',
		    'Content-Type: ' + type,
		    '',
		    atob(data),
		    '--' + boundary + '--'
		  ].join('\r\n'));
		};

		function cropPhoto(jCanvas, img){
			jCanvas.attr("width",w*rate);
			jCanvas.attr("height",h*rate);
			var canvas = jCanvas.get(0);
			var context = canvas.getContext("2d");
			// var targetImg = new Image()
			context.drawImage(img,x1*rate,y1*rate,w*rate,h*rate,0,0,w*rate,h*rate);
		};

		// generate preview image 
		function showPreviewPhoto(inputFiles, jPreViewImg){
			var deferred = $q.defer();

			if(inputFiles && inputFiles[0]){
				var reader = new FileReader();
				reader.onload = function(e) {
					jPreViewImg.attr("src",e.target.result);

					imgOrgWidth = jPreViewImg.get(0).width;
					imgOrgHeight= jPreViewImg.get(0).height;
					deferred.resolve(jPreViewImg);	
				}
				reader.readAsDataURL(inputFiles[0]);
			}else{
				deferred.reject('open file error!!');
			}	

			return deferred.promise;		
		};

		return{
			initJcropFun: initJcropFun,
			resize: resize,
			showPreviewPhoto: showPreviewPhoto,
			cropPhoto: cropPhoto,
			sendPhoto: sendPhoto,
			setsiteId: function(sId){
				siteId = sId;
			},
			setOriginalPhoto: function(p){
				originalPhoto = p;
			},
			getOriginalPhoto: function(){
				return originalPhoto;
			},
			setCropResult: function(e){
				cropResult = e;
			},
			getCropResult: function(){
				return cropResult;
			},
		}
    }]);
