var presidenciaveisApp = angular.module('presidenciaveisApp', []);

presidenciaveisApp.controller('PresidenciaveisController', function PresidenciaveisController($scope, $http) {
  $http.get("/listar-propostas")
    .then(function(response) {
       console.log(response.data);
    });
  $scope.propostas = [
    {
      texto: 'Nexus S',
      candidato: 'Fast just got faster with Nexus S.',
      area: 'Saúde'
    }
  ];
});

