import { signIn } from '@/lib/api';

class AuthHandler {
    private async handleSignIn(): Promise<void> {
        try {
            const user = await signIn();

            if (!user) {
                throw new Error('User not returned by sign-in');
            }

            console.log('AUTH2.e');
            console.log(auth2); // Ensure auth2 is defined before this line
            const id_token = user.getAuthResponse()?.id_token;
            const email = user.getBasicProfile()?.getEmail();
            const name = user.getBasicProfile()?.getGivenName();
            const lastName = user.getBasicProfile()?.getFamilyName();

            if (!id_token || !email || !name || !lastName) {
                throw new Error('Incomplete user information');
            }

            console.log({ idToken: id_token, email, name, lastName });
        } catch (error) {
            console.error('Error during sign-in:', error);
        }
    }
}

// Usage
const authHandler = new AuthHandler();
authHandler.handleSignIn().then(() => console.log('Sign-in process completed')).catch(console.error);