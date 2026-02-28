javascript
import { FB, gapi } from '@/lib/api';

const AuthService = {
    logOutWithFacebook: function() {
        const def = $.Deferred();
        
        if (FB) {
            FB.getLoginStatus((response) => {
                if (response.status === 'connected') {
                    FB.logout(() => {
                        def.resolve();
                    });
                } else {
                    def.reject('Nie był zalogowany');
                }
            });
        } else {
            def.reject('FB not exists');
        }

        return def.promise;
    },

    logOutWithGoogle: function() {
        const def = $.Deferred();

        if (gapi) {
            gapi.load('auth2', () => {
                const auth2 = gapi.auth2.init({
                    client_id: '345059472892-1fae8hutprcgcg3gk0i1dvdconjarcr0.apps.googleusercontent.com',
                    fetch_basic_profile: true,
                    scope: 'profile'
                });

                auth2.then(() => {
                    if (auth2.isSignedIn.get()) {
                        auth2.signOut();
                        def.resolve();
                    } else {
                        def.reject('Nie jest zalogowany');
                    }
                });
            });
        } else {
            def.reject('GAPI not exists');
        }

        return def.promise;
    }
};

export default AuthService;
