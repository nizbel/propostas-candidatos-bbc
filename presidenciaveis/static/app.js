var presidenciaveisApp = angular.module('presidenciaveisApp', ['angular.filter']);

presidenciaveisApp.config(['$compileProvider', function( $compileProvider )
    {   
        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|data):/);
    }
]);

presidenciaveisApp.controller('PresidenciaveisController', function PresidenciaveisController($scope, $http) {
	$scope.bloquear = false;
	
	$scope.init = function() {
		$http.get("/listar-propostas").then(function(response) {
	   		$scope.propostas = response.data;
	   		shuffleArray($scope.propostas);
	   
	   		$scope.candidatos = [];
	   		// {area: area, qtdPropostas: [lista de candidatos]}
	   		var qtdPropostasPorArea = {};
	   		
	   		for (var i = 0; i < $scope.propostas.length; i++) {
	     		$scope.propostas[i].selecionado = 'neutro';
	     
	 			if ($scope.candidatos.indexOf($scope.propostas[i].candidato) == -1) {
	     			$scope.candidatos.push($scope.propostas[i].candidato);
	     		}
	     		
	   			var areaExiste = false;
	   			for (var area in qtdPropostasPorArea) {
	   				if (area == $scope.propostas[i].area) {
	   					areaExiste = true;
	   					var candidatoExiste = false;
	   					for (var candidato in qtdPropostasPorArea[area]) {
	   						if (candidato == $scope.propostas[i].candidato) {
	   							candidatoExiste = true;
	   							qtdPropostasPorArea[area][candidato] += 1;
	   							break;
   							}
						}
						if (!candidatoExiste) {
							qtdPropostasPorArea[area][$scope.propostas[i].candidato] = 1;
						}
   					}
	   			}
				if (!areaExiste) {
					qtdPropostasPorArea[$scope.propostas[i].area] = {};
					qtdPropostasPorArea[$scope.propostas[i].area][$scope.propostas[i].candidato] = 1;
				}
	   			
	   		}
			
			for (var i = 0; i < $scope.propostas.length; i++) {
	     		// Definir valor de cada proposta para a nota final
	     		$scope.propostas[i].valorPonderado = 100/qtdPropostasPorArea[$scope.propostas[i].area][$scope.propostas[i].candidato];
     		}
	   		
	   		$scope.notas = [];
	   		$scope.candidatosVisualizar = [];
	   		
	   		for (var i = 0; i < $scope.candidatos.length; i++) {
	   			$scope.notas.push(0);
	   			$scope.candidatosVisualizar.push(i+1);
	   		}
	   		
	   		// Preparar gráfico
	   		var ctx = document.getElementById("myChart");
			$scope.radar = new Chart(ctx, {
			    type: 'radar',
			    data: {
				    labels: $scope.candidatosVisualizar,
				    datasets: [{
				        data: $scope.notas,
				        label: 'Concordância'
				    }]
				},
				options: {}
			});
			
			prepararDownload();
	    });
    }
    
    $scope.alterarPosicionamento = function(proposta, posicionamentoAnterior) {
    	var candidato = proposta.candidato;
    	switch (proposta.selecionado) {
    		case 'contra':
    			for (var i = 0; i < $scope.candidatos.length; i++) {
    				if (candidato == $scope.candidatos[i]) {
		   				$scope.notas[i] -= proposta.valorPonderado;
		   				if (posicionamentoAnterior == 'favor') {
		   					$scope.notas[i] -= proposta.valorPonderado;
		   				}
		   				break;
		   			}
		   		}
    			break;
    			
    		case 'neutro':
    			for (var i = 0; i < $scope.candidatos.length; i++) {
    				if (candidato == $scope.candidatos[i]) {
		   				if (posicionamentoAnterior == 'favor') {
		   					$scope.notas[i] -= proposta.valorPonderado;
		   				}
		   				else if (posicionamentoAnterior == 'contra') {
		   					$scope.notas[i] += proposta.valorPonderado;
		   				}
		   				break;
		   			}
		   		}
    			break;
    			
    		case 'favor':
    			for (var i = 0; i < $scope.candidatos.length; i++) {
    				if (candidato == $scope.candidatos[i]) {
		   				$scope.notas[i] += proposta.valorPonderado;
		   				if (posicionamentoAnterior == 'contra') {
		   					$scope.notas[i] += proposta.valorPonderado;
		   				}
		   				break;
		   			}
		   		}
    			break;
    	}		
		addData($scope.radar, montarData());
		
		prepararDownload();
    }
    
    $scope.verCandidatos = function() {
    	$http.get("/listar-candidatos").then(function(response) {
    		var candidatos = response.data;
    		
    		for (var i = 0; i < $scope.candidatos.length; i++) {
    			for (var j = 0; j < candidatos.length; j++) {
	    			if ($scope.candidatos[i] == candidatos[j].id) {
	    				$scope.candidatosVisualizar[i] = candidatos[j].nome;
	    			}
    			}
    		}
    		
			addData($scope.radar, montarData());
			
			$scope.bloquear = true;
			
			for (var i = 0; i < $scope.propostas.length; i++) {
				for (var j = 0; j < candidatos.length; j++) {
	    			if ($scope.propostas[i].candidato == candidatos[j].id) {
	    				$scope.propostas[i].nomeCandidato = candidatos[j].nome;
	    			}
    			}
			}
		});
    }
    
    function prepararDownload() {
		var csv = '';
        
        for (var i = 0; i < $scope.propostas.length; i++) {
        	var concordancia = '0';
        	if ($scope.propostas[i].selecionado == 'favor') {
        		concordancia = '1';
        	}
        	else if ($scope.propostas[i].selecionado == 'contra') {
        		concordancia = '-1';
        	}
        	csv += ($scope.propostas[i].id + ':' + concordancia + ';');
        }
        csv = csv.slice(0, -1);

        csv = 'data:text/csv;charset=utf-8,' + csv;
        data = encodeURI(csv);

        $scope.csv = data;
    }
    
    $scope.teste = function() {
    	for (var i = 0; i < $scope.propostas.length; i++) {
    		$scope.propostas[i].selecionado = 'favor';
    		$scope.alterarPosicionamento($scope.propostas[i], 'neutro');
    	}
    	$scope.verCandidatos();
    }
    
    function montarData() {
    	var notas = [];
    	for (var i = 0; i < $scope.notas.length; i++) {
			notas.push(Math.round($scope.notas[i]));
		}
		    	
    	var data = {
		    labels: $scope.candidatosVisualizar,
		    datasets: [{
		        data: notas,
		        label: 'Concordância'
		    }]
		};
		
		return data;
    }
    
    function addData(chart, data) {
	    chart.data = data;
	    chart.update();
	}
	
	function shuffleArray(array) {
	    for (var i = array.length - 1; i > 0; i--) {
	        var j = Math.floor(Math.random() * (i + 1));
	        var temp = array[i];
	        array[i] = array[j];
	        array[j] = temp;
	    }
	}
});

