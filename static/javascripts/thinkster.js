

angular
  .module('thinkster', ['thinkster.routes',
  						'thinkster.authentication',
  						'thinkster.config'
  						]);


angular
	.module('thinkster.config', []);

angular
	.module('thinkster.routes', ['ngRoute']);

angular
	.module('thinkster')
	.run(run);

	//run blocks run before anything else is excecuted, used to set initial app settings

run.$inject = ['$http'];

function run($http){
	$http.defaults.xsrfHeaderName = 'X-CSRFToken'; //Header expected by Django
	$http.defaults.xsrfCookieName = 'csrftoken'; 

}

