import api from '@/lib/api';

interface IAuth2 {
  init: (options: any) => Promise<void>;
  then: (callback: () => void) => void;
  isSignedIn: { get: () => boolean };
  signIn: () => Promise<void>;
}

class SocialWidgetService {

  private auth2: IAuth2 | null = null;

  constructor(private authService: AuthService, private router: any, private rootStore: any) {}

  async loginGoogle() {
    const client_id = '345059472892-1fae8hutprcgcg3gk0i1dvdconjarcr0.apps.googleusercontent.com';
    const scope = 'profile';

    await this.loadGapi('auth2', () => {
      this.auth2 = gapi.auth2.init({
        client_id,
        fetch_basic_profile: true,
        scope
      });

      console.log('AUTH2.a');
      console.log(this.auth2);

      this.auth2.then(() => {
        if (!this.auth2?.isSignedIn.get()) {
          console.log('AUTH2.b');
          console.log(this.auth2);

          this.auth2.signIn().then(() => {
            // Handle successful sign-in
          });
        }
      });
    });
  }

  private async loadGapi(moduleName: string, callback: () => void) {
    await new Promise((resolve) => gapi.load(moduleName, resolve));
    callback();
  }
}

// Example usage in a Next.js component or server-side logic
const socialWidgetService = new SocialWidgetService(authServiceInstance, useRouter(), rootStoreInstance);
socialWidgetService.loginGoogle().catch(console.error);