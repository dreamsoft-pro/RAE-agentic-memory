javascript
if (/* condition */) {
    // [BACKEND_ADVICE] Handle the logic for this specific condition.
    googleAuthClient.grantOfflineAccess({ scope: 'email' }).then(response => {
        const data = {
            service: 'google',
            email: response.email,
            name: response.name.split(' ')[0],
            lastName: response.name.split(' ')[1]
        };
        AuthService.loginWithGoogle(data).then(
            () => {
                $rootScope.$emit('CreditLimit:reload', true);
                $state.go('home');
            },
            error => {}
        );
    });
} else {
    FB.api('/me?fields=name,email', (response) => {
        const data = {
            service: 'facebook',
            email: response.email,
            name: response.name.split(' ')[0],
            lastName: response.name.split(' ')[1]
        };
        AuthService.loginWithFacebook(data).then(
            () => {
                $rootScope.$emit('CreditLimit:reload', true);
                $state.go('home');
            },
            error => {}
        );
    }, { scope: 'email' });
}
