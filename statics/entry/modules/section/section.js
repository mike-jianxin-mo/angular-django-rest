'use strict';

var sectionModule = angular.module('sectionModule', ['ui.bootstrap']);

sectionModule.controller('sectionCtrl', ['$scope', 'runTimeParam', '$location', 'sectionFactory', 
    'notificationFactory', 'settings', '$modal', '$state', '$sce',
    function($scope, runTimeParam, $location, sectionFactory, notificationFactory, settings, $modal, $state, $sce){

  var viewStates = {list:'/section-list.html', form: '/section-form.html' };

  // section CRUD return
  var getSiteSectionSuccess = function(data){
    $scope.sections = {vo:data, vs:viewStates};
    $scope.crudView = $scope.sections.vs.list;

  };

  function serverError(err) {
    notificationFactory.error(); 
  }; 

  // popup window 
  $scope.showForm = function(section){

    var sectionModalInstance = $modal.open({
      templateUrl: 'section-form.html',
      controller: editSectionCtrl,
      backdrop: 'static',
      resolve:{
        editSection: function(){
            return section;
          },
      },
    });

    sectionModalInstance.result.then(function(confirm){
        $state.go($state.$current, null, { reload: true });
      }, function(){
        console.log('cancel update!');
      }
    );

  };

  var editSectionCtrl = function($scope, $modalInstance, editSection){
    $scope.editSection = editSection;

    var successCallback = function(data){
      $modalInstance.close('yes');
    };

    $scope.update = function(){
      sectionFactory.updateSection(editSection).success(successCallback).error(serverError);
    };

    $scope.cancel = function(){
      $modalInstance.dismiss('cancel')
    };
  };

  (function(){
    sectionFactory.setSectionURI(settings.SECTION_URI);
    sectionFactory.getSiteSections(runTimeParam.curSite.sections).success(getSiteSectionSuccess).error(serverError);
  })();

}]);

// section layer
sectionModule.factory('sectionFactory', ['$http', function($http){
    var _URL_ = '';
    // remove view state and setup post data 
    var sectionId ='0';

    var setSectionId = function(sectionId){
      sectionId = sectionId;
    };

    var getSectionId = function(sectionId){
      return sectionId;
    };

    return {
      setSectionId: setSectionId,
      getSectionId: getSectionId,
      setSectionURI : function(uri){
        _URL_ = uri;
      },
      getSiteSections: function(uri){
        return $http.get(uri);
      },
      saveSection: function(sectionData){
        return $http.post( _URL_ , sectionData);
      },
      getSectionById: function(){
        return $http.get(_URL_ + sectionId);
      },
      updateSection: function(sectionData){
        return $http.put(_URL_ + sectionData.id, sectionData);
      },
    }
  }]);

sectionModule.directive('ckEditor', function() {
    return {
        require : '?ngModel',
        link : function($scope, elm, attr, ngModel) {

            var ck = CKEDITOR.replace(elm[0]);

            ck.on('instanceReady', function() {
                ck.setData(ngModel.$viewValue);
            });

            ck.on('pasteState', function() {
                $scope.$apply(function() {
                    ngModel.$setViewValue(ck.getData());
                });
            });

            ngModel.$render = function(value) {
                ck.setData(ngModel.$modelValue);
            };
        }
    };
});
