(function(){
	'use-strict';

	angular
		.module('thinkster.layout.controllers')
		.controller('IndexController', IndexController);

	IndexController.$inject = ['$scope', 'Authentication', 'Posts', 'Snackbar'];

	function IndexController($scope, Authentication, Posts, Snackbar){

		var vm = this;

		vm.posts = []

		vm.isAuthenticated = Authentication.isAuthenticated();

		activate();

		function activate(){



			Posts.all().then(postsSuccessFn, postsErrorFn);


			$scope.$on('post.created', function(event, post){
				vm.posts.unshift(post);
			});

			$scope.$on('post.created.error', function(){
				vm.posts.shift(); 
			});

			function postsSuccessFn(data, status, headers, config){
				vm.posts = data.data;
				console.log(vm.posts);
			}

			function postsErrorFn(data, status, headers, config){
				Snackbar.error(data.error);
			}
		}
	}
})();