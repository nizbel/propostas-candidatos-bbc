var presidenciaveisApp = angular.module('presidenciaveisApp', []);

presidenciaveisApp.controller('PresidenciaveisController', function PresidenciaveisController($scope, $http) {
  $http.get("/listar-propostas")
    .then(function(response) {
       $scope.propostas = response.data;
       
       for (var i = 0; i < $scope.propostas.length; i++) {
         $scope.propostas[i].selecionado = 'neutro';
       }
    });
});

